# CodeSkulptor runs Python programs in your browser.
# Click the upper left button to run this simple demo.

# CodeSkulptor runs in Chrome 18+, Firefox 11+, and Safari 6+.
# Some features may work in other browsers, but do not expect
# full functionality.  It does NOT run in Internet Explorer.

import simplegui
import random
import math

#program constants
CV_WD = 600
CV_HT = 500
NUM_BALLS = 10
PCT_RED = 30.0
MARGIN = 30
COORD_DIRECTIONS = [-5,-4,-3,-2,-1,1,2,3,4,5]
STEP = 1
BALL_RADIUS = 15
CLICK_MAX = 3

#program variables
balls = []
rds = 0
occupied_posns = []
clicks = 0
showCorrect= False
num_correct = 0

def make_balls():
    #Note: after balls are made, the Red balls will be at the beginning of the list
    global balls
    for i in range(NUM_BALLS):
        balls.append(Ball(BALL_RADIUS))
    random.shuffle(balls)
    numRed = int(PCT_RED/100 * NUM_BALLS)
    for i in range(numRed):
        balls[i].set_color('Red')
        balls[i].set_wasRed(True)
    for i in range(numRed, NUM_BALLS):
        balls[i].set_color('Blue')
        balls[i].set_wasRed(False)
class Ball:
    def __init__(self, radius):
        self.radius = radius
        self.pos = self.gen_random_pos()
        self.direction = [0,0]
        self.clicked = False
    def set_color(self, color):
        self.color = color
    
    def set_wasRed(self, wasRed):
        self.wasRed = wasRed
    
    def set_direction(self, direction):
        self.direction = direction
    def gen_random_pos(self):
        #initiaze random position. Include margin so that ball doesn't end up on edge of canvas.
        #If it ends up on edge of canvas with direction vector of [0, 0], it'll be stuck there- 
        #even when flipping its direction. Also make sure that the position generated
        #for the ball doesn't overlap with that of any other ball
        global occupied_posns
        while True:
            x = random.randint(self.radius+MARGIN, CV_WD-self.radius-MARGIN)
            y = random.randint(self.radius+MARGIN, CV_HT-self.radius-MARGIN)
            for posn in occupied_posns:
                if ((posn[0] - x)**2 + (posn[1] - y)**2) < 4*BALL_RADIUS**2: #balls
                    #overlap if their centers are less than 2 BALL_RADII apart
                    break
            else: #break out of outer while loop if inner for loop did not terminate early
                break
           
        occupied_posns.append([x,y])
        return [x,y]
    def move(self):
        if self.pos[0] < self.radius or self.pos[0] > CV_WD - self.radius:
            self.set_direction([-self.direction[0], self.direction[1]])
            if self.pos[0] < self.radius:
                self.pos = [self.radius, self.pos[1]]
            else: # self.pos[0] > CV_WD - self.radius:
                self.pos = [CV_WD - self.radius, self.pos[1]]
        if self.pos[1] < self.radius or self.pos[1] > CV_HT - self.radius:
            self.set_direction([self.direction[0], -self.direction[1]])
            if self.pos[1] < self.radius:
                self.pos = [self.pos[0], self.radius]
            else: #self.pos[1] > CV_HT - self.radius
                self.pos = [self.pos[0], CV_HT - self.radius]
        self.pos[0] += (self.direction[0]*STEP)
        self.pos[1] += (self.direction[1]*STEP)
    def stop(self):
        self.set_direction([0,0])
    
    def isWithin(self, pos):
        posX = pos[0]
        posY = pos[1]
        return (posX - self.pos[0])**2 + (posY - self.pos[1])**2 < self.radius**2
            
    def draw(self, canvas):
        if showCorrect and self.wasRed and not self.color=='Red':
            canvas.draw_circle(self.pos, self.radius, 1, 'Yellow', 'Red')
        else:
            canvas.draw_circle(self.pos, self.radius, 1, self.color, self.color)
        
    def changeDirection(self):
        xDir = random.choice(COORD_DIRECTIONS)
        yDir = random.choice(COORD_DIRECTIONS)
        norm = math.sqrt(xDir**2 + yDir**2)
        self.set_direction([xDir/norm,yDir/norm])
        assert abs(1- ((self.direction[0]**2) + (self.direction[1]**2))) <0.01
    def __str__(self):
        return 'Ball('+'pos:'+str(self.pos)+', direction:'+str(self.direction)+', color:'+str(self.color)
def draw(canvas):
    global balls
    for ball in balls:
        ball.draw(canvas)
    for ball in balls:
        ball.move()
    canvas.draw_text('clicks:'+str(clicks), (20, 40), 20, 'White')
    if showCorrect and num_correct == CLICK_MAX:
        canvas.draw_text('ALL CORRECT!', (CV_WD/2 - 200, CV_HT/2), 35, 'White')
def hideReds():
#    print 'in hideReds'
    numRed = int(PCT_RED/100 * NUM_BALLS)
    global balls, hide_reds_timer, ball_direction_timer
    for i in range(numRed):
       balls[i].set_color('Blue')
    hide_reds_timer.stop()
    ball_direction_timer.start()

def displayResults():
    global showCorrect
    showCorrect = True
    global results_timer
    results_timer.stop()
    
def handleClick(pos):
    global clicks, num_correct
    if clicks == CLICK_MAX:
        return
    #you're limited to 3 (=CLICKS_MAX) clicks;
    #a click is only counted if it is within a ball
    #that has not been clicked yet;
    #when balls overlap, be sure to only click on the 
    #section of the ball that doesn't overlap with another;
    #it's almost certain that you'll have a non-overlapping
    #section of any given ball that's big enough to click on
    for ball in balls:
        if ball.isWithin(pos) and not ball.clicked:
            ball.clicked = True
            clicks += 1
            if ball.wasRed:
                ball.set_color('Red')
                num_correct += 1
            break
    if clicks == CLICK_MAX:
        global results_timer
        results_timer = simplegui.create_timer(800, displayResults)
        results_timer.start()
def startEval():
    global frame, mouse_handler
    mouse_handler = frame.set_mouseclick_handler(handleClick)
    
    
def changeBallDirection():
    global rds, ball_direction_timer
    #print 'in changeBallDirection'
    for ball in balls:
        ball.changeDirection()
    rds += 1
    if rds>=10:
        ball_direction_timer.stop()
        for ball in balls:
            ball.stop()
            startEval()
def start():
    global showCorrect
    showCorrect = False
    make_balls()
    global hide_reds_timer, ball_direction_timer
    hide_reds_timer.start()
frame = simplegui.create_frame('Remember the Reds', CV_WD,
                               CV_HT)
def medium():
    start()

def hard():
    global STEP
    STEP = 1.4
    start()
hide_reds_timer = simplegui.create_timer(1000, hideReds)
ball_direction_timer = simplegui.create_timer(1000, changeBallDirection)
frame.set_draw_handler(draw)
frame.add_button('Medium', medium, 150)
frame.add_button('Hard', hard, 150)
frame.start()

#start()