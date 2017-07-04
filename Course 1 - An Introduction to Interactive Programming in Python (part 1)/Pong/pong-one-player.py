# Implementation of classic arcade game Pong


try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui



#import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 100
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

count = 0
maxCount = 0

def spawn_ball():
	global ball_pos, ball_vel # these are vectors stored as lists
	ball_pos=[WIDTH/2,HEIGHT/2]
	
	factor=1 # Plus for downward and minus for upward # FIX!!!
	ball_vel=[random.randrange(120, 240)/50, factor*random.randrange(70, 180)/50]

# define event handlers
def new_game():
    global paddle_pos, paddle_vel  # these are numbers
    global count, maxCount  # these are ints
    
    spawn_ball() 
    
    paddle_pos=[(HEIGHT - PAD_HEIGHT) / 2, (HEIGHT + PAD_HEIGHT) / 2]   
    paddle_vel=[0,0]
    
def restart():
	global count, maxCount
	count = 0
	maxCount = 0
	new_game()

def draw(canvas):
	global count, maxCount, paddle_pos, ball_pos, ball_vel

	# draw mid line and gutters
	canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White") # Middle line
	canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White") # Player left line
		
	# update ball
	ball_pos[0] += ball_vel[0]
	ball_pos[1] += ball_vel[1] 
	
	# rules for ball bounce against walls
	if ball_pos[1] <= (BALL_RADIUS): # Y-top
		ball_vel[1] = - ball_vel[1]	
	elif ball_pos[1] >= (HEIGHT - BALL_RADIUS): # Y-bottom
		ball_vel[1] = - ball_vel[1]
	elif ball_pos[0] >= (WIDTH - BALL_RADIUS): # X-right
		ball_vel[0] = - ball_vel[0]

	# draw ball
	canvas.draw_circle([ball_pos[0],ball_pos[1]], BALL_RADIUS, 2, "White", "White") 

	# update paddle's vertical position, keep paddle on the screen
	paddle_pos[0] += paddle_vel[0]
	paddle_pos[1] += paddle_vel[1]
	
	if(paddle_pos[0] <= 0):
		paddle_pos[0] = 0
		paddle_pos[1] = PAD_HEIGHT
		
	elif(paddle_pos[1] >= HEIGHT):
		paddle_pos[0] = HEIGHT	- PAD_HEIGHT	
		paddle_pos[1] = HEIGHT
	
	# draw paddles
	canvas.draw_line([ HALF_PAD_WIDTH, paddle_pos[0] ],[HALF_PAD_WIDTH, paddle_pos[1]], PAD_WIDTH, "White") 

	# determine whether paddle and ball collide  
	acc=2
	
	if(ball_pos[0] <= 30 and paddle_pos[0] <= ball_pos[1] <= paddle_pos[1]):
		ball_vel[0] = - ball_vel[0]+acc
		count += 1
	elif(ball_pos[0] <= 30 and (paddle_pos[0] > ball_pos[1] or  ball_pos[1] > paddle_pos[1]) ):
		if(count > maxCount):
			maxCount = count
		count = 0
		new_game()
	
	# draw scores
	canvas.draw_text(str(count), (WIDTH/4, HEIGHT/4), HEIGHT/10, 'White')
	canvas.draw_text(str(maxCount), (WIDTH - WIDTH/4, HEIGHT/4), HEIGHT/10, 'White')
		
def keydown(key):
	global paddle_vel
	acc=10
	if(key==simplegui.KEY_MAP["up"]):
		paddle_vel[0] -= acc
		paddle_vel[1] -= acc
	elif(key==simplegui.KEY_MAP["down"]):
		paddle_vel[0] += acc
		paddle_vel[1] += acc
		
def keyup(key):
	global paddle_vel
	if(key==simplegui.KEY_MAP["up"]):
		paddle_vel[0] = 0
		paddle_vel[1] = 0
	elif(key==simplegui.KEY_MAP["down"]):
		paddle_vel[0] = 0
		paddle_vel[1] = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', restart, 150)

# start frame
new_game()
frame.start()
