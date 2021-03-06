import simplegui
import math
import random
#Canvas Constants
CV_WD = 600
CV_HT = 500

#Canvas Object constants
SCL = 20
ARROW_SEP = 60
USER_TEXT_PADDING = 10
USER_TEXT_SIZE = 22 
UNDERBOX_TEXT_SIZE = 20
COLOR_TEXT_SIZE = 36
MAIN_PANEL_POS  = (CV_WD/2, CV_HT/2) #main panel contains box with text color and box with meaning;
#main panel also contains check or x that appears after each time user makes selection (presses either left
#or right arrow key)
BOX_SEP = 60
BOX_WD = 200
BOX_HT = 80
COLORS = ['Purple', 'Green', 'Orange', 'Red', 'Yellow', 'Blue', 'White']
MEANING = 'Meaning'
TEXT_COLOR = 'Text Color'
SCORE_POS = (CV_WD/2, 40)
SCORE_TEXT_SIZE = 20
TIME_STATUS_POS = (CV_WD - 120, 40)
TIME_STATUS_SIZE = 20
GAME_OVER_SCREEN_POS = (CV_WD/2 - 100, CV_HT/2)

#program variables
started = False
answer_correct = False
answer_status_visible = False
timed = False
keyHandlersDisabled = False
gameOverScreen = False

#For telling user which keys correspond to which selections
class UserHelp:
    def __init__(self, pos, size):
        self.noTextColor = 'White'
        self.yesTextColor = 'White'
        self.arrow1 = Arrow((pos[0] - ARROW_SEP/2, pos[1]), size, 'left')
        self.arrow2 = Arrow((pos[0] + ARROW_SEP/2, pos[1]), size, 'right')
        self.no_pos = (self.arrow1.t_tip[0] - frame.get_canvas_textwidth('No', USER_TEXT_SIZE) - USER_TEXT_PADDING,
                 self.arrow1.t_tip[1]+10)
        self.yes_pos = (self.arrow2.t_tip[0] + USER_TEXT_PADDING,
                 self.arrow2.t_tip[1]+10)
        
    def changeNoTextColor(self, color):
        self.noTextColor = color
    
    def changeYesTextColor(self, color):
        self.yesTextColor = color
    
    def draw(self, canvas):
        self.arrow1.draw(canvas)  
        canvas.draw_text('No', self.no_pos, USER_TEXT_SIZE, self.noTextColor)
        self.arrow2.draw(canvas)
        canvas.draw_text('Yes', self.yes_pos, USER_TEXT_SIZE, self.yesTextColor)
class Arrow:
    #PRECONDITION: pass a size only between 1 and 3 (inclusive of both)
    #Parameters:
    #pos (position)- a tuple- of arrow is the middle of its tail;
    #size- an int;
    #direction- a string- must be either 'left' or 'right'
    #Comments:
    #Rectangular part of arrow will have pixel height of SCL*size
    #and a pixel width of 2*SCL*size;
    #Triangular part of arrow will be isoceles triangle with a base
    #of 2*SCL*size and a height of SCL*size
    
    def __init__(self, pos, size, direction):
        self.pos = pos
        self.size = size
        self.direction = direction
        x = self.pos[0]
        y = self.pos[1]
        s = self.size
        sc = SCL
        if self.direction == 'left':
            self.rtr = (x, y - 0.5*sc*s)
            self.rtl = (x - 2*sc*s, y - 0.5*sc*s)
            self.rbl = (x - 2*sc*s, y + 0.5*sc*s)
            self.rbr = (x, y + 0.5*sc*s)
            self.t_base_top = (x - 2*sc*s, y - sc*s)
            self.t_tip = (x - 3*sc*s, y)
            self.t_base_bottom = (x - 2*sc*s, y + sc*s)
        elif self.direction == 'right':
            self.rtr = (x + 2*sc*s, y - 0.5*sc*s)
            self.rtl = (x, y - 0.5*sc*s)
            self.rbl = (x, y + 0.5*sc*s)
            self.rbr = (x + 2*sc*s, y + 0.5*sc*s)
            self.t_base_top = (x + 2*sc*s, y - sc*s)
            self.t_tip = (x + 3*sc*s, y)
            self.t_base_bottom = (x + 2*sc*s, y + sc*s)
        else:
            print 'invalid direction'
            
    def draw(self, canvas):        
        rtr = self.rtr
        rtl = self.rtl
        rbl = self.rbl
        rbr = self.rbr
        t_base_top = self.t_base_top
        t_tip = self.t_tip
        t_base_bottom = self.t_base_bottom
        
        canvas.draw_polygon([rtr, rtl, rbl, rbr], 1,
                            'White', 'White')
        canvas.draw_polygon([t_base_top, t_tip, t_base_bottom], 1, 'White', 'White')
        
class X:
    def __init__(self, pos, size):
        self.pos = pos #pos member of X instance is center of X (where lines cross)
        self.size = size
        
    def __str__(self):
        pos = self.pos
        size = self.size
        return 'X(pos:'+ str(pos) + ', size:' + str(size) +')'
    def draw(self, canvas):
        pos = self.pos
        size = self.size
        canvas.draw_line((pos[0] - 0.5*SCL*size, pos[1] - 0.5*SCL*size), (pos[0] + 0.5*SCL*size, pos[1] + 0.5*SCL*size), 2, 'Red')
        canvas.draw_line((pos[0] - 0.5*SCL*size, pos[1] + 0.5*SCL*size), (pos[0] + 0.5*SCL*size, pos[1] - 0.5*SCL*size), 2, 'Red')
    
class Check:
    def __init__(self, pos,size):
        self.pos = pos #pos member of Check instance is where lines of checkmark meet
        self.size = size
        
    def __str__(self):
        pos = self.pos
        size = self.size
        return 'Check(pos:'+str(pos)+', size:'+str(size)+')'
    def draw(self, canvas):
        pos = self.pos
        canvas.draw_line(pos, (pos[0] - 0.5*SCL*self.size, pos[1] - 0.5*SCL*self.size), 2, 'Green')
        canvas.draw_line(pos, (pos[0] + SCL*self.size, pos[1] - SCL*self.size), 2, 'Green')        

# Handler to draw on canvas
def draw(canvas):
    global started, timed
    if gameOverScreen:
        started = False
        timed = False
        canvas.draw_text(str(num_correct)+' correct out of '+str(num_answered),
                         GAME_OVER_SCREEN_POS, 30, 'White')
    if started:
        u.draw(canvas)
        leftBoxTR = (MAIN_PANEL_POS[0] - BOX_SEP/2, MAIN_PANEL_POS[1] - BOX_HT/2)
        canvas.draw_polygon([leftBoxTR,
                             (leftBoxTR[0] - BOX_WD, leftBoxTR[1]), 
                             (leftBoxTR[0] - BOX_WD, leftBoxTR[1] + BOX_HT),
                             (leftBoxTR[0], leftBoxTR[1] + BOX_HT)], 
                            1, 'White') #left box coords listed in order: top-right, top-left, bottom-left, bottom-right
        rightBoxTL = (MAIN_PANEL_POS[0] + BOX_SEP/2, MAIN_PANEL_POS[1] - BOX_HT/2)
        canvas.draw_polygon([rightBoxTL, (rightBoxTL[0]+ BOX_WD, rightBoxTL[1]), 
                             (rightBoxTL[0] + BOX_WD, rightBoxTL[1] + BOX_HT),
                             (rightBoxTL[0], rightBoxTL[1] + BOX_HT)], 1, 'White') #right box coordsd listed in order:
                             #top-left, top-right, bottom-right, bottom-left
        if answer_status_visible:
            if answer_correct:
                check.draw(canvas)
            else:
                x.draw(canvas)
        draw_colors(canvas)
        draw_score(canvas)
    if timed:
        canvas.draw_text('Time Left:'+str(time_remaining//60)+':'+pad(time_remaining%60),
                        TIME_STATUS_POS, TIME_STATUS_SIZE, 'White')

def pad(x):
    if x>=10:
        return str(x)
    else:
        return '0'+str(x)

def handleColorSwitch():
    calc_color_vars()
def draw_colors(canvas):
    canvas.draw_text(textLabel, meaningPos, COLOR_TEXT_SIZE, 'White')
    canvas.draw_text(MEANING, meaningLabelPos, UNDERBOX_TEXT_SIZE, 'White')
    canvas.draw_text(textColorText, textColorPos, COLOR_TEXT_SIZE, textColorColor)
    canvas.draw_text(TEXT_COLOR, textColorLabelPos, UNDERBOX_TEXT_SIZE, 'White')

def draw_score(canvas):
    canvas.draw_text(str(num_correct)+'/'+str(num_answered), SCORE_POS, SCORE_TEXT_SIZE, 'White')
def calc_color_vars():
    global textLabel
    textLabel = random.choice(COLORS)
    textLabelLen = frame.get_canvas_textwidth(textLabel, COLOR_TEXT_SIZE)
    global meaningPos
    global textColorPos
    global textColorColor
    global textColorText
    global meaningLabelPos
    global textColorLabelPos
        
    if random.random() < 0.5: #meaning box on left
        meaningPos = (MAIN_PANEL_POS[0] - BOX_SEP/2 - BOX_WD/2 - textLabelLen/2,
                           MAIN_PANEL_POS[1]+10)
        
        
        textColorPos = (MAIN_PANEL_POS[0] + BOX_SEP/2 + BOX_WD/2 - textLabelLen/2,
                        MAIN_PANEL_POS[1]+10)
                
    else: #meaning box on right
        meaningPos = (MAIN_PANEL_POS[0] + BOX_SEP/2 + BOX_WD/2 - textLabelLen/2,
                        MAIN_PANEL_POS[1]+10)
        textColorPos = (MAIN_PANEL_POS[0] - BOX_SEP/2 - BOX_WD/2 - textLabelLen/2,
                           MAIN_PANEL_POS[1]+10)
        
    meaningLabelPos = (meaningPos[0], meaningPos[1] + BOX_HT/2 + 20)
    textColorLabelPos = (textColorPos[0], textColorPos[1] + BOX_HT/2 +20)
        
    if random.random() < 0.5:
        textColorColor = textLabel
    else:
        textColorColor = random.choice(list(set(COLORS).difference(textLabel)))
    
    if random.random() < 0.3:
        textColorText = textColorColor
    else:
        textColorText = random.choice(list(set(COLORS).difference(textColorColor)))

def changeAnswerStatusVisibility():
    global answer_status_timer, answer_status_visible
    answer_status_visible = False
    answer_status_timer.stop()


    
def handleKeyUp(key):
    if not started or keyHandlersDisabled:
        return 
    if key not in [simplegui.KEY_MAP['left'], simplegui.KEY_MAP['right']]:
        return
    global num_answered
    global answer_correct
    global num_correct
    global answer_status_visible
    global answer_status_timer
    global u
    num_answered += 1
    
    
    if key == simplegui.KEY_MAP['left']:
        u.changeNoTextColor('White')
        if textLabel != textColorColor:
            answer_correct = True
        else:
            answer_correct = False
    else : #key == simplegui.KEY_MAP['right']
        u.changeYesTextColor('White')
        if textLabel == textColorColor:
            answer_correct = True
        else:
            answer_correct = False
    
    if answer_correct:
        num_correct += 1
        
    answer_status_visible = True    
    answer_status_timer.start()
    calc_color_vars()
    
def changeUserTextColor(key):
    if not started or keyHandlersDisabled:
        return
    global u
    if key  == simplegui.KEY_MAP['left']:
        u.changeNoTextColor('Yellow')
    elif key == simplegui.KEY_MAP['right']:
        u.changeYesTextColor('Yellow')
    else:
        return
    
def practice():
    global started, num_correct, num_answered, gameOverScreen, timed
    global keyHandlersDisabled
    keyHandlersDisabled = False
    gameOverScreen = False
    timed = False
    num_correct = 0
    num_answered = 0
    started = True
    calc_color_vars()

    
def directions():
    pass

def updateTime():
    if not timed:
        return
    global time_remaining, game_over_timer
    if time_remaining > 0:
        time_remaining -= 1
    else:
        global keyHandlersDisabled, u
        keyHandlersDisabled = True
        u.changeNoTextColor('White')
        u.changeYesTextColor('White')
        game_over_timer.start()
        
def gameOverTimer():
    global game_over_timer
    global gameOverScreen
    gameOverScreen = True
    game_over_timer.stop()
    
def start():
    global game_timer, started, time_remaining, timed, num_correct, num_answered, gameOverScreen
    global keyHandlersDisabled
    keyHandlersDisabled = False
    gameOverScreen = False
    num_correct = 0
    num_answered = 0
    timed = True
    time_remaining = 60
    started = True
    game_timer.start()
    calc_color_vars()
    


#initialize ui
frame = simplegui.create_frame("Color Matching Game", CV_WD, CV_HT)
frame.add_button('Directions', directions, 100)
frame.add_button('Practice', practice, 100)
frame.add_button('(Re)Start', start, 100)

#key and draw handlers
frame.set_draw_handler(draw)
frame.set_keyup_handler(handleKeyUp)
frame.set_keydown_handler(changeUserTextColor)

frame.start()

#timers
answer_status_timer = simplegui.create_timer(500, changeAnswerStatusVisibility)
game_timer = simplegui.create_timer(1000, updateTime)
game_over_timer = simplegui.create_timer(4000, gameOverTimer)

#create global instance vars
u = UserHelp((CV_WD/2, CV_HT-100), 1)
x = X(MAIN_PANEL_POS, 1)
check = Check(MAIN_PANEL_POS, 1)

