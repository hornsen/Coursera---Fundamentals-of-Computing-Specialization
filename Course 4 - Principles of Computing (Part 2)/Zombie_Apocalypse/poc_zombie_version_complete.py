"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7

class Apocalypse(poc_grid.Grid):
	"""
	Class for simulating zombie pursuit of human on grid with
	obstacles
	"""

	def __init__(self, grid_height, grid_width, obstacle_list = None, 
				 zombie_list = None, human_list = None):
		"""
		Create a simulation of given size with given obstacles,
		humans, and zombies
		"""
		poc_grid.Grid.__init__(self, grid_height, grid_width)
		if obstacle_list != None:
			for cell in obstacle_list:
				self.set_full(cell[0], cell[1])
		if zombie_list != None:
			self._zombie_list = list(zombie_list)
		else:
			self._zombie_list = []
		if human_list != None:
			self._human_list = list(human_list)  
		else:
			self._human_list = []


	def clear(self):
		"""
		Set cells in obstacle grid to be empty
		Reset zombie and human lists to be empty
		"""
		poc_grid.Grid.clear(self)
		self._human_list = []
		self._zombie_list = []
		
	def add_zombie(self, row, col):
		"""
		Add zombie to the zombie list
		"""
		self._zombie_list.append((row,col))
				
	def num_zombies(self):
		"""
		Return number of zombies
		"""
		return len( self._zombie_list )
		  
	def zombies(self):
		"""
		Generator that yields the zombies in the order they were
		added.
		"""
		for item in self._zombie_list:
			yield item

	def add_human(self, row, col):
		"""
		Add human to the human list
		"""
		self._human_list.append((row,col))
		
	def num_humans(self):
		"""
		Return number of humans
		"""
		return len( self._human_list )
	
	def humans(self):
		"""
		Generator that yields the humans in the order they were added.
		"""
		for item in self._human_list:
			yield item

	def compute_distance_field(self, entity_type):
		"""
		Function computes and returns a 2D distance field
		Distance at member of entity_list is zero
		Shortest paths avoid obstacles and use four-way distances
		"""

		visited = poc_grid.Grid(self._grid_height, self._grid_width)
		distance_field = [[self._grid_width * self._grid_height for col in range(self._grid_width)] for row in range(self._grid_height)]

		boundary = poc_queue.Queue()

		if(entity_type == HUMAN):
			for idx in self.humans():
				boundary.enqueue(idx)
		elif(entity_type == ZOMBIE):
			for idx in self.zombies():
				boundary.enqueue(idx)
		
		for row, col in boundary:
			visited.set_full(row, col)
			distance_field[row][col] = 0

		while boundary.__len__() > 0:
			current_cell = boundary.dequeue()
			neighbors = visited.four_neighbors(current_cell[0], current_cell[1])

			for neighbor in neighbors:
				if visited.is_empty(neighbor[0], neighbor[1]) and self.is_empty(neighbor[0], neighbor[1]):
					visited.set_full(neighbor[0], neighbor[1])
					distance_field[ neighbor[0] ][ neighbor[1] ] = (distance_field[current_cell[0]][current_cell[1]] + 1)
					boundary.enqueue(neighbor)

		return distance_field
	 
	
	def move_humans(self, zombie_distance_field):
		"""
		Function that moves humans away from zombies, diagonal moves
		are allowed
		"""
		new_human_lst=[]
		for human in self.humans():
			move_human=[]
			move_human.append((human[0], human[1]))

			for row, col in self.eight_neighbors(human[0], human[1]):
				if(self.is_empty(row, col) and zombie_distance_field[row][col] > zombie_distance_field[move_human[0][0]][move_human[0][1]]):
					move_human=[]
					move_human.append((row, col))

				elif(self.is_empty(row, col) and zombie_distance_field[row][col] == zombie_distance_field[move_human[0][0]][move_human[0][1]]):
					move_human.append((row, col))

			random.shuffle(move_human)
			new_human_lst.append(move_human.pop())

		self._human_list = new_human_lst
	
	def move_zombies(self, human_distance_field):
		"""
		Function that moves zombies towards humans, no diagonal moves
		are allowed
		"""
		new_zombie_lst=[]
		for zombie in self.zombies():
			move_zombie=[]
			move_zombie.append((zombie[0], zombie[1]))

			for row, col in self.four_neighbors(zombie[0], zombie[1]):
				if(self.is_empty(row, col) and human_distance_field[row][col] < human_distance_field[move_zombie[0][0]][move_zombie[0][1]]):
					move_zombie=[]
					move_zombie.append((row, col))

				elif(self.is_empty(row, col) and human_distance_field[row][col] == human_distance_field[move_zombie[0][0]][move_zombie[0][1]]):
					move_zombie.append((row, col))
			random.shuffle(move_zombie)
			new_zombie_lst.append(move_zombie.pop())

		self._zombie_list = new_zombie_lst


# Start up gui for simulation 
poc_zombie_gui.run_gui(Apocalypse(30, 40))
