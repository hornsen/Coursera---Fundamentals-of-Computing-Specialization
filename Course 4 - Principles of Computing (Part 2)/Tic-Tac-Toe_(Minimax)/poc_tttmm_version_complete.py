"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

import sys
sys.dont_write_bytecode = True

# Set timeout, as mini-max can take a long time
try:
	import codeskulptor
except ImportError:
	import SimpleGUICS2Pygame.codeskulptor as codeskulptor
#import codeskulptor 

codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
		  provided.DRAW: 0,
		  provided.PLAYERO: -1}


def mm_move(board, player):
	"""
	Make a move on the board.
	
	Returns a tuple with two elements.  The first element is the score
	of the given board and the second element is the desired move as a
	tuple, (row, col).
	"""

	if(board.check_win() != None):
		return [ SCORES[ board.check_win() ] ]

	else:
		best_move=None
		best_score=None

		if(player == provided.PLAYERX):
			opponent = provided.PLAYERO
			factor = SCORES[ provided.PLAYERX ]
		else:
			opponent = provided.PLAYERX
			factor = SCORES[ provided.PLAYERO ]

		for possible_move in board.get_empty_squares():
			board_temp = board.clone()
			board_temp.move(possible_move[0], possible_move[1], player)
			score = mm_move(board_temp, opponent)[0]

			if(score * factor == 1):
				best_score = score 
				best_move = possible_move
	
				return best_score , best_move

			elif(score * factor > best_score):
				best_score = score * factor
				best_move = possible_move

				# print("score", score)
				# print("best_score", best_score)
				# print("best_score* factor", best_score* factor)
				# print("")
		print(board)
		print(best_score, best_move)
		return best_score * factor, best_move

def move_wrapper(board, player, trials):
	"""
	Wrapper to allow the use of the same infrastructure that was used
	for Monte Carlo Tic-Tac-Toe.
	"""
	
	move = mm_move(board, player)
	assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
	print('Move_wrapper', move)
	print(board)
	return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

def testing():	
	""" 
	Testing the program
	"""	
	mm_move(provided.TTTBoard(3, False, [[provided.EMPTY, provided.EMPTY, provided.PLAYERX], [provided.EMPTY, provided.EMPTY, provided.EMPTY], [provided.EMPTY, provided.EMPTY, provided.EMPTY]]), provided.PLAYERO) 
	#expected score 0 but received (-1, (0, 0))

		
testing()


#provided.play_game(move_wrapper, 1, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
