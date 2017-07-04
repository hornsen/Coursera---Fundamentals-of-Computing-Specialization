"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 100        # Number of trials to run
SCORE_CURRENT = 1
SCORE_OTHER = 2

PLAYERX = 2 # machine (X)
PLAYERO = 3 # human (O)

GAME_BOARD= provided.TTTBoard(3)

def mc_trial(board, player): 
	"""
	This function takes a current board and the next player to move. 
	The function should play a game starting with the given player 
	by making random moves, alternating between players. 
	The function should return when the game is over. 
	The modified board will contain the state of the game, 
	so the function does not return anything. In other words, 
	the function should modify the board input.
	"""
	while True:
		if( len(board.get_empty_squares()) >= 0 and board.check_win() == None):
			coordinate = (board.get_empty_squares()[random.randrange(len(board.get_empty_squares()))] )
			board.move(coordinate[0], coordinate[1], player)
			
			if(player == 2):
				player += 1
			elif(player == 3):
				player -= 1
		else:
			break

	
def mc_update_scores(scores, board, player): 
	"""
	This function takes a grid of scores (a list of lists) with the 
	same dimensions as the Tic-Tac-Toe board, a board from a completed game, 
	and which player the machine player is. 
	The function should score the completed board and update the scores grid. 
	As the function updates the scores grid directly, it does not return anything,
	"""
	
	if(len(board.get_empty_squares()) != 0):		
		for row in range( board.get_dim() ):
			for col in range( board.get_dim() ):			
				if( board.check_win() == player):
					if( board.square(row, col) ==  1):
						scores[row][col] += 0
					
					elif( board.square(row, col) ==  player):
						scores[row][col] += SCORE_CURRENT 
						
					elif( board.square(row, col) !=  player):
						scores[row][col] -= SCORE_OTHER
				
				elif( board.check_win() != player):
					if( board.square(row, col) ==  1):
						scores[row][col] += 0
					
					elif( board.square(row, col) ==  player):
						scores[row][col] -= SCORE_CURRENT 

					elif( board.square(row, col) !=  player):
						scores[row][col] += SCORE_OTHER

def get_best_move(board, scores): 
	"""
	This function takes a current board and a grid of scores. 
	The function should find all of the empty squares with the maximum 
	score and randomly return one of them as a (row, column) tuple. 
	It is an error to call this function with a board that has no 
	empty squares (there is no possible next move), so your function 
	may do whatever it wants in that case. The case where the board 
	is full will not be tested.
	"""
	best_move_is = []
	dummy = None

	for row in range( board.get_dim() ):
		for col in range( board.get_dim() ):
			if( scores[row][col] > dummy and board.square(row, col) ==  1):
				best_move_is = []
				dummy = scores[row][col]
				best_move_is.append( (row, col) )
			elif( scores[row][col] == dummy and board.square(row, col) ==  1):
				best_move_is.append( (row, col) )
	
	return best_move_is.pop()


def mc_move(board, player, trials): 
	"""
	This function takes a current board, which player the machine 
	player is, and the number of trials to run. 
	The function should use the Monte Carlo simulation described above 
	to return a move for the machine player in the form 
	of a (row, column) tuple. 
	"""	
	
	# THIS DOES NOT WORK:
	#~ scores = []
	#~ scores.append([0] * board.get_dim()) 
	#~ scores = scores * board.get_dim() 
	
	# THIS WORKS:
	scores = []
	while len(scores) < board.get_dim():
		scores.append([0] * board.get_dim() )
	
	for _ in range(trials):
		board_clone = board.clone()
		mc_trial(board_clone, player)		
		mc_update_scores(scores, board_clone, player)
	
	print(get_best_move(board, scores))
	return get_best_move(board, scores)
	


def testing():	
	""" 
	Testing the program
	"""	
	mc_move(provided.TTTBoard(3, False, [[provided.PLAYERX, provided.EMPTY, provided.EMPTY], [provided.PLAYERO, provided.PLAYERO, provided.EMPTY], [provided.EMPTY, provided.PLAYERX, provided.EMPTY]]), provided.PLAYERX, NTRIALS) 
	#returned mostly bad moves: [(2, 2), (2, 0), (2, 2), (2, 0), (2, 2)]

		
testing()

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

for _ in range(1):
	provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
	
