
import simplegui
import math
import random

#canvas constants
c_width = 800
c_height = 700

#big circle constants: TODO: CHANGE LOWERCASE CONSTANTS TO UPPERCASE
big_rad = 250
big_circle_pos = (c_width/2 , c_height/2)
big_circle_color = 'White'
big_circle_line_width = 2
big_circle_visible = False


#small constants
SMALL_CIRCLE_LINE_WIDTH = 1

#text position constants for in-game questions and game status
QUESTION_POS = (220,40)
ANSWER_STATUS_POS = (20, 40)
SCORE_POS = (700, 40)
TIME_LEFT_POS = (650, 80)
FINAL_SCORE_POS = (c_width/2 - 100, c_height/2 - 30)

#game status constants
WRONG = 'Wrong'
CORRECT = 'Correct!'

#other program constants
MAX_RD_CT = 5

#program variables
refTheta = 0
num_circles = 8
small_circle_rad = 30
small_circle_color = 'Orange'
direction = '+'
question = ''
last_state = None
answer_status = ''
respondToKeys = False
score = 0
gameOver = False
directionsScreen = True
gameStarted = False

def reg_questions():
    q1 = 'size: smaller(left)? same(up)? bigger(right)?'
    q2 = 'number: less(left)? same(up)? more(right)?'
    q3 = 'color: different(left)? same(up)?'
    q4 = 'direction: different(left)? same(up)?'
    return {'size':q1,'number':q2,'color':q3,'direction':q4}

#Regular Mode questions
REG_Qs =  reg_questions()


# computes constants for regular mode of game
def reg_constants():
    numCircs = range(5,11)
    colors = 'Blue Purple Orange Red Yellow Green'.split()
    sizes = range(10,60,10)
    direc = '+ -'.split() #'+' denotes counterclockwise and
    #'-' denotes clockwise
    return { 'NumberCircles':numCircs, 'colors':colors,
            'sizes':sizes, 'directions':direc}

#Regular Mode constants
REG_MODE_VALS = reg_constants()

def nxt_state():
    global last_state
    global num_circles
    global small_circle_rad
    global small_circle_color
    global direction
    last_state = {'num_circles':num_circles, 'small_circle_rad':small_circle_rad,
                  'small_circle_color':small_circle_color, 'direction':direction}
    num_circles = random.choice(REG_MODE_VALS['NumberCircles'])
    small_circle_rad = random.choice(REG_MODE_VALS['sizes'])
    small_circle_color = random.choice(REG_MODE_VALS['colors'])
    direction = random.choice(REG_MODE_VALS['directions'])
    global question
    question = REG_Qs[random.choice(REG_Qs.keys())]    
    global curr_state 
    curr_state = {'num_circles':num_circles, 'small_circle_rad':small_circle_rad,
                  'small_circle_color':small_circle_color, 'direction':direction}
    
def draw_small_circles(canvas):
    global refTheta
    if direction == '+':
        refTheta = refTheta + 0.01
    else:
        refTheta = refTheta - 0.01
    dTheta = 2*math.pi/num_circles
    for i in range(num_circles):
        circlePosX = big_circle_pos[0]+big_rad*math.cos(refTheta + i*dTheta)
        circlePosY = big_circle_pos[1]-big_rad*math.sin(refTheta + i*dTheta)
        canvas.draw_circle((circlePosX,circlePosY), small_circle_rad, SMALL_CIRCLE_LINE_WIDTH, small_circle_color, small_circle_color)

def disp_question(canvas):
    canvas.draw_text(question, QUESTION_POS, 20, 'White')

# Handler for timer; should only fire between first
# and second displays
def handleTimer():
    nxt_state()
    global initialScreenTimer
    initialScreenTimer.stop()
    global respondToKeys
    respondToKeys = True
    global clock
    clock.start()
def disp_answer_status(canvas):
    canvas.draw_text(answer_status, ANSWER_STATUS_POS, 20, 'White') 
        
def disp_score(canvas):
    canvas.draw_text('Score:'+str(score), SCORE_POS, 20, 'White')

def gameDirectionsScreen(canvas):
    l1 = 'You will be presented with a series of sets of moving circles'
    l2 = 'and be asked to compare any set of circles with the set before'
    l3 = 'it on the bases of circle size, number of circles, color,'
    l4 = 'and direction. Respond using the arrow keys. The questions will'
    l5 = 'be stated at the top of the screen. During the game, you may'
    l6 = 'click anywhere on screen to pause the game and these directions'
    l7 = 'will be redisplayed. Click anywhere on the screen to start.'
    
    lines = list((l1, l2, l3, l4, l5,l6,l7))
    startPos = (180, 190)
    for i in range(len(lines)):
        canvas.draw_text(lines[i], (startPos[0], startPos[1]+40*i), 18, 'White')

def disp_time_left(canvas):
    canvas.draw_text('Time Left:'+str(timeLeft//60)+':'+pad(timeLeft%60),
                     TIME_LEFT_POS, 20, 'White')
def pad(x):
    if x>=10:
        return str(x)
    else:
        return '0'+str(x)

# Handler to draw on canvas
def draw(canvas):
    if directionsScreen:
        gameDirectionsScreen(canvas)
    else:
        if not gameOver:
            if big_circle_visible:
                canvas.draw_circle(big_circle_pos, big_rad, big_circle_line_width, big_circle_color)
            draw_small_circles(canvas)
            disp_question(canvas)
            disp_answer_status(canvas)
            disp_score(canvas)
            disp_time_left(canvas)
        else:
            canvas.draw_text('Final Score: '+str(score), FINAL_SCORE_POS, 40, 'White')
#compares number of circles in this screen with
#the number in the last screen; takes into account
#the player's response and sets answer_status
#accordingly
def cmpCircles(key):
    global answer_status
    answer_status = WRONG
    lastOne = last_state['num_circles']
    thisOne = curr_state['num_circles']
    if thisOne < lastOne:
        if key == simplegui.KEY_MAP['left']:
            answer_status = CORRECT
    elif thisOne == lastOne:
        if key == simplegui.KEY_MAP['up']:
            answer_status = CORRECT
    else: #thisOne > lastOne
        if key == simplegui.KEY_MAP['right']:
            answer_status = CORRECT
    if answer_status == CORRECT:
        global score
        score += 10
    else:
        score -= 5
        
def cmpSizes(key):
    global answer_status
    answer_status = WRONG
    lastOne = last_state['small_circle_rad']
    thisOne = curr_state['small_circle_rad']
    if thisOne < lastOne:
        if key == simplegui.KEY_MAP['left']:
            answer_status = CORRECT
    elif thisOne == lastOne:
        if key == simplegui.KEY_MAP['up']:
            answer_status = CORRECT
    else: #thisOne > lastOne
        if key == simplegui.KEY_MAP['right']:
            answer_status = CORRECT
    if answer_status == CORRECT:
        global score
        score += 10
    else:
        score -= 5
def cmpColors(key):
    global answer_status
    answer_status = WRONG
    lastOne = last_state['small_circle_color']
    thisOne = curr_state['small_circle_color']
    if thisOne != lastOne:
        if key == simplegui.KEY_MAP['left']:
            answer_status = CORRECT
    else: #thisOne == lastOne
        if key == simplegui.KEY_MAP['up']:
            answer_status = CORRECT
    if answer_status == CORRECT:
        global score
        score += 10
    else:
        score -= 5
def cmpDirections(key):
    global answer_status
    answer_status = WRONG
    lastOne = last_state['direction']
    thisOne = curr_state['direction']
    if thisOne != lastOne:
        if key == simplegui.KEY_MAP['left']:
            answer_status = CORRECT
    else: #thisOne == lastOne
        if key == simplegui.KEY_MAP['up']:
            answer_status = CORRECT
    if answer_status == CORRECT:
        global score
        score += 10
    else:
        score -= 5
        
def handleAnswerStatusTimer():
    global answer_status_timer
    answer_status_timer.stop()
    global answer_status
    answer_status=''

    
##QUESTION: how come the 2000 millisecond delay for this handler
##specified in the run function doesn't seem to transpire if I
##stop the timer inside of this handler?
def handleGameoverScreenTimer():
    global gameOver
    gameOver = True
    #global gameover_screen_timer
    #gameover_screen_timer.stop()
    
##TODO: change if-else clause to use switch
def handleKeyPress(key):
    if directionsScreen or gameOver or (not respondToKeys):
        return
    if key not in [simplegui.KEY_MAP['left'], simplegui.KEY_MAP['up'],
                   simplegui.KEY_MAP['right']]: #ignore if not up, down or right
        #arrows
        return 
    if question in [REG_Qs['color'], REG_Qs['direction']]:
        if key not in [simplegui.KEY_MAP['left'], simplegui.KEY_MAP['up']]:
            return
#below lines useful for debugging   
    print last_state 
    print curr_state
    print '------------------------------------'
     
    if question == REG_Qs['number']:
        cmpCircles(key)
    elif question == REG_Qs['size']:
        cmpSizes(key)
    elif question == REG_Qs['color']:
        cmpColors(key)
    elif question == REG_Qs['direction']:
        cmpDirections(key)
    else: #code should never reach here
        print 'invalid question:'+question
    global answer_status_timer
    answer_status_timer.start()
    nxt_state()

def tick():
    global timeLeft, respondToKeys
    if not directionsScreen and timeLeft>0:
        timeLeft -= 1
    elif directionsScreen:
        pass
    else:
        respondToKeys = False
        global gameover_screen_timer
        gameover_screen_timer.start()
##starts the game
def start():
    global frame
    frame.set_keydown_handler(handleKeyPress)
    global initialScreenTimer
    initialScreenTimer = simplegui.create_timer(4000,handleTimer)
    initialScreenTimer.start()
    global answer_status_timer
    answer_status_timer = simplegui.create_timer(800, handleAnswerStatusTimer)
    global gameover_screen_timer 
    gameover_screen_timer = simplegui.create_timer(2000, handleGameoverScreenTimer)
    global timeLeft
    timeLeft = 60
    global clock
    clock = simplegui.create_timer(1000, tick)
    
def handleClick(x):
    global directionsScreen
    directionsScreen = not directionsScreen
    global gameStarted
    if not gameStarted:
        gameStarted = True
        start()

#displays screen with directions. This screen is the entry point into the game    
def run():
    global frame
    frame = simplegui.create_frame("Working Memory Game 1", c_width, c_height)
    frame.set_draw_handler(draw)
    frame.set_mouseclick_handler(handleClick)
    frame.start()


run()

