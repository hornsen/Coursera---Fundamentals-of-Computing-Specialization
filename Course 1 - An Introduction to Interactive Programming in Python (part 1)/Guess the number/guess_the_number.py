try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

#import simplegui
import random
import math

#initialize global variables used in your code
secret_number=str(random.randrange(0,100))
guess_left=7
num_range = 100

# helper function to start and restart the game
def new_game():
	# initialize global variables used in your code here
	print(secret_number)
	print('New game. Range is from 0 to %s' % num_range)
	print('Number of remaning guesses is %s' % guess_left)
	print('\n')
	f.start()

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
	global num_range, guess_left, secret_number
	num_range = 100
	guess_left = 7
	secret_number=str(random.randrange(0,100))
	new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
	global num_range, guess_left, secret_number
	num_range = 1000
	guess_left = 10
	secret_number=str(random.randrange(0,1000))
	new_game()
    
def get_input(guess):
	# main game logic goes here	
	global operand, guess_left
	guess_left -= 1
	operand = str(guess)
	
	if(guess_left>=0):
		print('Guess was %s:' % operand)
		print('Number of remaning guesses is %s' % guess_left)
		if(guess>secret_number):
			print('Lower! \n')
		elif(guess<secret_number):
			print('Higher! \n')
			
		else:
			print('Correct! \n')
			if(num_range==100):
				range100()
			else:
				range1000()
	else:
		print('You have lost!')
		print('The secret number was: %s \n' % secret_number)
		if(num_range==100):
				range100()
		else:
			range1000()

# create frame
f = simplegui.create_frame("Guess the number",300,300)

# register event handlers for control elements and start frame
f.add_button('Range is [0, 100]', range100, 200)
f.add_button('Range is [0, 1000]', range1000, 200)
f.add_input('Enter a guess', get_input, 200)

# call new_game 
new_game()
