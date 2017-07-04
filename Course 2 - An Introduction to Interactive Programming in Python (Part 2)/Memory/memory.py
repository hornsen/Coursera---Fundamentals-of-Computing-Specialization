# implementation of card game - Memory

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

#import simplegui
import random

# Generate memory numbers
numbers=range(1,6)
numbers=numbers+numbers
tempOpen=[]
remainOpen=[]
counter=0

BOARD_SIZE=[750,120]
CARD_RADIUS = 50

# helper function to initialize globals
def new_game():
	global counter
	random.shuffle(numbers)
	tempOpen[:] = []
	remainOpen[:] = []
	
	counter=0
	label.set_text(str("Counter: %s" % counter))
	
# define event handlers
def mouseclick(pos):
	global counter, tempOpen
	
	if(len(tempOpen) == 2 ):
		counter+=1
		label.set_text(str("Counter: %s" % counter))

		if(numbers[ tempOpen[0] ] == numbers[ tempOpen[1] ]):
			remainOpen.append( tempOpen.pop() )
			remainOpen.append( tempOpen.pop() )
		
		else:
			tempOpen=[]

	if(0<pos[0]<BOARD_SIZE[0]) and 0 < pos[1] < BOARD_SIZE[1] :
		cardNumber=pos[0]/75
		if(cardNumber not in tempOpen and cardNumber not in remainOpen):
			tempOpen.append(cardNumber)  
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
	canvas.draw_line([0, 50], [BOARD_SIZE[0], 50], 140, 'Green')
	for i in range(len(numbers)):
			canvas.draw_line([75*i, 120], [75*i, 0], 1, 'Blue')
	
	if(len(tempOpen) > 0):	
		for i in tempOpen:
			canvas.draw_text(str(numbers[i]), [10+(75)*i, 100], 100, "Red")
    
	if(len(remainOpen) > 0):	
		for i in remainOpen:
			canvas.draw_text(str(numbers[i]), [10+(75)*i, 100], 100, "Red")
    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", BOARD_SIZE[0], BOARD_SIZE[1])
frame.add_button("Reset", new_game)
label = frame.add_label("Counter: %s" % counter)

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
