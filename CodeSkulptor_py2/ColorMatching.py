
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

#program variables
answer_correct = False
answer_status_visible = False
num_correct = 0
num_answered = 0

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
    global u
    if key  == simplegui.KEY_MAP['left']:
        u.changeNoTextColor('Yellow')
    elif key == simplegui.KEY_MAP['right']:
        u.changeYesTextColor('Yellow')
    else:
        return
def practice():
    pass
    
def directions():
    pass
    
def start():
    pass




frame = simplegui.create_frame("Color Matching Game", CV_WD, CV_HT)
frame.add_button('Directions', directions, 100)
frame.add_button('Practice', practice, 100)
frame.add_button('(Re)Start', start, 100)

frame.set_draw_handler(draw)
frame.set_keyup_handler(handleKeyUp)
frame.set_keydown_handler(changeUserTextColor)
calc_color_vars()

frame.start()


answer_status_timer = simplegui.create_timer(500, changeAnswerStatusVisibility)

#colorTimer = simplegui.create_timer(1000, handleColorSwitch)
#colorTimer.start()
u = UserHelp((CV_WD/2, CV_HT-100), 1)
x = X(MAIN_PANEL_POS, 1)
check = Check(MAIN_PANEL_POS, 1)

