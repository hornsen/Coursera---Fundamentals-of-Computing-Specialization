"""
Clone of 2048 game.
"""

# GUI
import poc_2048_gui, random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
			DOWN: (-1, 0),
			LEFT: (0, 1),
			RIGHT: (0, -1)}

def merge(line):
	"""
	Helper function that merges a single row or column in 2048
	"""
	old_lst=line
	new_lst=[0]*len(old_lst)
	
	if(len(old_lst) == 1):
		new_lst[0] = old_lst[0]
	
	else:
		merge_allowed = True
		counter=0
		
		if(old_lst[0] == 0): 
			first_num_is_zero = True
			
		elif(old_lst[0] >= 0):
			new_lst[0] = old_lst[0]
			first_num_is_zero = False
		
							
		for num in range(1, len(old_lst), 1):
			
			if(old_lst[num] != 0):
				
				
				if(first_num_is_zero == True and old_lst[num] >0):
					new_lst[0] = old_lst[num]
					first_num_is_zero = False	
					
				elif(first_num_is_zero == False):
					
					
					if(old_lst[num] == new_lst[counter] and merge_allowed == True):
						new_lst[counter] = old_lst[num] * 2
						merge_allowed = False

					elif(old_lst[num] != new_lst[counter] or merge_allowed == False):
						counter += 1
						new_lst[counter] = old_lst[num]
						merge_allowed = True
						
	return new_lst

class TwentyFortyEight:
	"""
	Class to run the game logic.
	"""

	def __init__(self, grid_height, grid_width):

		self._grid_height = grid_height
		self._grid_width = grid_width
		
		self.reset()

	def reset(self):
		"""
		Reset the game so the grid is empty except for two
		initial tiles.
		"""
		self._grid = [[0 for _ in range(self._grid_width)]
						for _ in range(self._grid_height)]
	
		self.new_tile()
		self.new_tile()

	def __str__(self):
		"""
		Return a string representation of the grid for debugging.
		"""
		show_grid=""
		for idx in range(len(self._grid)):
			show_grid += str(self._grid[idx]) + "\n"
		
		return show_grid
		
	def get_grid_height(self):
		"""
		Get the height of the board.
		"""
		return self._grid_height

	def get_grid_width(self):
		"""
		Get the width of the board.
		"""
		return self._grid_width

	def move(self, direction):
		"""
		Move all tiles in the given direction and add
		a new tile if any tiles moved.
		"""
		temp_grid = str(self._grid)
		
		if(direction == LEFT):
			num_steps = self.get_grid_width()
			start_cell = [0,0]
		elif(direction == RIGHT):
			num_steps = self.get_grid_width()
			start_cell = [0, self.get_grid_width() - 1]

		elif(direction == UP):
			num_steps = self.get_grid_height()
			start_cell = [0, 0]
		elif(direction == DOWN):
			num_steps = self.get_grid_height()
			start_cell = [self.get_grid_height() - 1, 0]
		
		
		while True:	
			temp_lst=[]		
			for step in range(num_steps):
				row = start_cell[0] + step * OFFSETS[direction][0]
				col = start_cell[1] + step * OFFSETS[direction][1]
				print "Processing cell", (row, col)
				print "with value", self.get_tile(row, col)
				temp_lst.append( self.get_tile(row, col)  )
			print("")
			
			for step in range(num_steps):
				if(direction == RIGHT):
					self.set_tile(start_cell[0], step, merge(temp_lst)[self.get_grid_width() - step - 1] )
				elif(direction == LEFT):
					self.set_tile(start_cell[0], step, merge(temp_lst)[step] )
					
				elif(direction == UP):
					self.set_tile(step, start_cell[1], merge(temp_lst)[step] )
				elif(direction == DOWN):
					self.set_tile(step, start_cell[1], merge(temp_lst)[self.get_grid_height() - step - 1] )
			
			if(direction == LEFT and start_cell[0] < self.get_grid_height() - 1):
				start_cell[0] += 1
			elif(direction == RIGHT and start_cell[0] < self.get_grid_height() - 1):
				start_cell[0] += 1
			elif(direction == UP and start_cell[1] < self.get_grid_width() - 1):
				start_cell[1] += 1
			elif(direction == DOWN and start_cell[1] < self.get_grid_width() - 1):
				start_cell[1] += 1
			else:
				break
			
		if( str(temp_grid) != str(self._grid) ):
			self.new_tile()
		
		for row in self._grid:
			print(row)
		print("")

	def new_tile(self):
		"""
		Create a new tile in a randomly selected empty
		square.  The tile should be 2 90% of the time and
		4 10% of the time.
		"""
		empty_coordinate = []
		
		for col in range( self.get_grid_width() ):
			for row in range( self.get_grid_height() ):
				if( int(self._grid[row][col]) == 0):			
					empty_coordinate.append( [row, col] )

		random.shuffle( empty_coordinate )
		
		random_number_lst=[2,2,2,2,2,2,2,2,2,4]
		random.shuffle( random_number_lst )
		random_number = random_number_lst[ int(random.random()*10) ]
				
		for num in range(len(empty_coordinate)):
			self.set_tile(empty_coordinate[num][0], empty_coordinate[num][1], random_number)
			break


	def set_tile(self, row, col, value):
		"""
		Set the tile at position row, col to have the given value.
		"""
		self._grid[row][col] = value

	def get_tile(self, row, col):
		"""
		Return the value of the tile at position row, col.
		"""
		return self._grid[row][col]


def testing(game_class):
	"""
	Some informal testing code
	"""

	# create a game
	obj = game_class

	# TESTING LEFT/RIGHT
	#~ obj.set_tile(0, 0, 2)
	#~ obj.set_tile(0, 1, 4)
	#~ obj.set_tile(0, 2, 8)
	#~ obj.set_tile(0, 3, 16)
	#~ obj.set_tile(1, 0, 16)
	#~ obj.set_tile(1, 1, 8)
	#~ obj.set_tile(1, 2, 4)
	#~ obj.set_tile(1, 3, 2)
	#~ obj.set_tile(2, 0, 0)
	#~ obj.set_tile(2, 1, 0)
	#~ obj.set_tile(2, 2, 8)
	#~ obj.set_tile(2, 3, 16)
	#~ obj.set_tile(3, 0, 0)
	#~ obj.set_tile(3, 1, 0)
	#~ obj.set_tile(3, 2, 4)
	#~ obj.set_tile(3, 3, 2)
	
	print(obj)

	# Run gui
	poc_2048_gui.run_gui(game_class)


testing( TwentyFortyEight(4,4) )



