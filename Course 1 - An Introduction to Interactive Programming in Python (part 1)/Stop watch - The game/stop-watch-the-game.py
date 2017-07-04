

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


#import simplegui

# define global variables
time=0
score=0
attempt=0
observe=False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(time):
    global milliseconds
    time=time
    minutes=int(time/600)
    milliseconds=int(time%10)
    seconds=int((time-milliseconds)/10-minutes*60)
    
    if(seconds<10):
        return (str(minutes)+':0'+str(seconds)+'.'+str(milliseconds))
    else:
        return (str(minutes)+':'+str(seconds)+'.'+str(milliseconds))

# Function that keeps track of the score
def scoreSystem():
    global score, attempt, observe
    if(observe==True):
        if(milliseconds==0):
            score+=1
            attempt+=1
        else:
            attempt+=1
    else:
        score=score
        attempt=attempt
    
    observe=False
    return (str(score)+str('/')+str(attempt))

# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global time, observe
    observe=True
    timer.start()
    time+=1
    return format(time)

def stop():
    timer.stop()
    scoreSystem()
    return format(time)

def reset():
    global time, attempt, score
    stop()
    time=0
    attempt=0
    score=0

# define draw handler
def draw(canvas):
    canvas.draw_text(format(time),[100, 100], 24, "White")
    canvas.draw_text(str(score)+str('/')+str(attempt),[240, 24], 24, "Green")
    
# create frame
frame = simplegui.create_frame("Stop watch: The Game!", 300, 200)

# register event handlers
frame.set_draw_handler(draw)
frame.add_button('Start', start, 200)
frame.add_button('Stop', stop, 200)
frame.add_button('Reset', reset, 200)
timer = simplegui.create_timer(100, start) 

# start frame
frame.start()
