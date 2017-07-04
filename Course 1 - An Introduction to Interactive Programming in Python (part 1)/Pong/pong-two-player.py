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
direction = 'RIGHT'

score1 = 0
score2 = 0

BALL_ACC = 1
PADDLE_ACC=10

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
	global ball_pos, ball_vel # these are vectors stored as lists
	ball_pos=[WIDTH/2,HEIGHT/2]

	if(direction=='LEFT'):
		ball_vel=[-random.randrange(120, 240)/50, -random.randrange(60, 180)/50]
	elif(direction=='RIGHT'):
		ball_vel=[random.randrange(120, 240)/50, -random.randrange(60, 180)/50]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    
    spawn_ball(direction) 
    
    paddle1_pos=[0,PAD_HEIGHT]
    paddle2_pos=[0,PAD_HEIGHT]
    
    paddle1_vel=[0,0]
    paddle2_vel=[0,0]
    
def restart():
	global score1, score2
	score1 = 0
	score2 = 0
	new_game()

def draw(canvas):
	global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, direction

	# draw mid line and gutters
	canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White") # Middle line
	canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White") # Player left line
	canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White") # Player right line
		
	# update ball
	ball_pos[0] += ball_vel[0]
	ball_pos[1] += ball_vel[1] 
	
	# rules for ball bounce against walls
	if ball_pos[1] <= (BALL_RADIUS): # Y-top
		ball_vel[1] = - ball_vel[1]	
	elif ball_pos[1] >= (HEIGHT - BALL_RADIUS): # Y-bottom
		ball_vel[1] = - ball_vel[1]

	# draw ball
	canvas.draw_circle([ball_pos[0],ball_pos[1]], BALL_RADIUS, 2, "White", "White") 

	# update paddle's vertical position, keep paddle on the screen
	paddle1_pos[0] += paddle1_vel[0]
	paddle1_pos[1] += paddle1_vel[1]
	
	paddle2_pos[0] += paddle2_vel[0]
	paddle2_pos[1] += paddle2_vel[1]
	
	if(paddle1_pos[0] <= 0):
		paddle1_pos[0] = 0
		paddle1_pos[1] = PAD_HEIGHT
		
	elif(paddle1_pos[1] >= HEIGHT):
		paddle1_pos[0] = HEIGHT	- PAD_HEIGHT	
		paddle1_pos[1] = HEIGHT

	if(paddle2_pos[0] <= 0): 
		paddle2_pos[0] = 0
		paddle2_pos[1] = PAD_HEIGHT		
	elif(paddle2_pos[1] >= HEIGHT):
		paddle2_pos[0] = HEIGHT	- PAD_HEIGHT
		paddle2_pos[1] = HEIGHT
	
	# draw paddles
	canvas.draw_line([ HALF_PAD_WIDTH, paddle1_pos[0] ],[HALF_PAD_WIDTH, paddle1_pos[1]], PAD_WIDTH, "White") 
	canvas.draw_line([WIDTH - HALF_PAD_WIDTH, paddle2_pos[0] ],[WIDTH - HALF_PAD_WIDTH, paddle2_pos[1] ], PAD_WIDTH, "White")     

	# determine whether paddle and ball collide  	
	if(ball_pos[0] <= 30 and paddle1_pos[0] <= ball_pos[1] <= paddle1_pos[1]):
		ball_vel[0] = - ball_vel[0] + BALL_ACC
	elif(ball_pos[0] <= 30 and (paddle1_pos[0] > ball_pos[1] or  ball_pos[1] > paddle1_pos[1]) ):
		score2 += 1
		direction = 'RIGHT'
		new_game()

	if(ball_pos[0] >= WIDTH - 30 and paddle2_pos[0] <= ball_pos[1] <= paddle2_pos[1]):
		ball_vel[0] = - ball_vel[0] - BALL_ACC
	elif(ball_pos[0] >= WIDTH - 30 and (paddle2_pos[0] > ball_pos[1] or  ball_pos[1] > paddle2_pos[1]) ):
		score1 += 1
		direction = 'LEFT'
		new_game()
	
	# draw scores
	canvas.draw_text(str(score1), (WIDTH/4, HEIGHT/4), HEIGHT/10, 'White')
	canvas.draw_text(str(score2), (WIDTH - WIDTH/4, HEIGHT/4), HEIGHT/10, 'White')
		
def keydown(key):
	global paddle1_vel, paddle2_vel
	
	if(key==simplegui.KEY_MAP["w"]):
		paddle1_vel[0] -= PADDLE_ACC
		paddle1_vel[1] -= PADDLE_ACC
	elif(key==simplegui.KEY_MAP["s"]):
		paddle1_vel[0] += PADDLE_ACC
		paddle1_vel[1] += PADDLE_ACC
   
	elif(key==simplegui.KEY_MAP["up"]):
		paddle2_vel[0] -= PADDLE_ACC
		paddle2_vel[1] -= PADDLE_ACC
	elif(key==simplegui.KEY_MAP["down"]):
		paddle2_vel[0] += PADDLE_ACC
		paddle2_vel[1] += PADDLE_ACC
		
def keyup(key):
	global paddle1_vel, paddle2_vel
	if(key==simplegui.KEY_MAP["w"]):
		paddle1_vel[0] = 0
		paddle1_vel[1] = 0
	elif(key==simplegui.KEY_MAP["s"]):
		paddle1_vel[0] = 0
		paddle1_vel[1] = 0
		
	elif(key==simplegui.KEY_MAP["up"]):
		paddle2_vel[0] = 0
		paddle2_vel[1] = 0
	elif(key==simplegui.KEY_MAP["down"]):
		paddle2_vel[0] = 0
		paddle2_vel[1] = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', restart, 150)

# start frame
new_game()
frame.start()
