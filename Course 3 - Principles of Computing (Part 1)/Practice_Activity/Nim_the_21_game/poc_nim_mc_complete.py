"""
A simple Monte Carlo solver for Nim
http://en.wikipedia.org/wiki/Nim#The_21_game
"""

try:
    import codeskulptor
except ImportError:
    import SimpleGUICS2Pygame.codeskulptor as codeskulptor

#import codeskulptor
import random

codeskulptor.set_timeout(20)

MAX_REMOVE = 3
TRIALS = 10000

def evaluate_position(num_items):
	"""
	Monte Carlo evalation method for Nim
	"""
	sucessful_events_counter = [0,0,0]
	events_counter = [0,0,0]
	
	for _ in range(TRIALS):
		initial_move=random.randrange(1, MAX_REMOVE + 1) 

		num_items_copy = num_items
		num_items_copy -= initial_move
		
		events_counter[initial_move-1] += 1
		player_counter=0
		
		while num_items_copy > 0: 
			player_counter += 1
			move = random.randrange(1, MAX_REMOVE + 1) 
			num_items_copy -= move
			
			# Even numbers are computer and uneven numbers are player
		if player_counter % 2 == 0:
			sucessful_events_counter[initial_move-1] += 1
				
	best_move=1
	if(float( sucessful_events_counter[0] ) / float( events_counter[0] ) < float( sucessful_events_counter[1] ) / float( events_counter[1] ) ):
		best_move=2
	if(float( sucessful_events_counter[1] ) / float( events_counter[1] ) < float( sucessful_events_counter[2] ) / float( events_counter[2] ) ):
		best_move=3
	
	return best_move


def play_game(start_items):
	"""
	Play game of Nim against Monte Carlo bot
	"""

	current_items = start_items
	print("Starting game with value %s" % current_items)
	comp_move = evaluate_position(current_items)
	current_items -= comp_move
	print ("Computer choose %s, current value is %s" % (comp_move, current_items) )
		
	while True:
		player_move = int(input("\nEnter your current move: "))
		
		if(1 < player_move > MAX_REMOVE):
			print("Please choose a number between 1 and 3.")
		else:
			current_items -= player_move
			print("Player choose %s, current value is %s" % (player_move, current_items) )
			if current_items <= 0:
				print "\n*** Player wins ***"
				break
			
			comp_move = evaluate_position(current_items)
			current_items -= comp_move
			print ("Computer choose %s, current value is %s" % (comp_move, current_items) )
			if current_items <= 0:
				print("\n*** Computer wins ***")
				break

play_game(21)



