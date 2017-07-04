"""
Student code for Word Wrangler game
"""

try:
	import codeskulptor
except ImportError:
	import SimpleGUICS2Pygame.codeskulptor as codeskulptor
#import codeskulptor 

import poc_wrangler_provided as provided
import urllib2

codeskulptor.set_timeout(200000)
WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
	"""
	Eliminate duplicates in a sorted list.

	Returns a new sorted list with the same elements in list1, but
	with no duplicates.

	This function can be iterative.
	"""
	no_duplicates_lst=[]

	for idx_1 in range(len(list1)):
		no_duplicates_lst.append(list1[idx_1])
		for idx_2 in range(idx_1+1, len(list1)):
			if(list1[idx_1] == list1[idx_2]):
				no_duplicates_lst.pop()
				break

	return no_duplicates_lst

def intersect(list1, list2):
	"""
	Compute the intersection of two sorted lists.

	Returns a new sorted list containing only elements that are in
	both list1 and list2.

	This function can be iterative.
	"""
	intersected_lst = []
	for word_1 in list1:
		for word_2 in list2:
			if(word_1 == word_2):
				intersected_lst.append(word_1)

	return intersected_lst

# Functions to perform merge sort

def merge(list1, list2):
	"""
	Merge two sorted lists.

	Returns a new sorted list containing those elements that are in
	either list1 or list2.

	This function can be iterative.
	"""   

	merge_list = []
	
	idx_1=0
	idx_2=0
	while True:
		if(idx_1 < len(list1)):
			word_1 = list1[idx_1]
		else:
			merge_list += list2[idx_2:]
			break

		if(idx_2 < len(list2)):
			word_2 = list2[idx_2]
		else:
			merge_list += list1[idx_1:]
			break

		if(word_1 == word_2):
			merge_list.append(word_1)
			merge_list.append(word_2)
			idx_1+=1
			idx_2+=1
		elif(word_1 < word_2):
			merge_list.append(word_1)
			idx_1+=1
		elif(word_1 > word_2):
			merge_list.append(word_2)
			idx_2+=1

		if(len(merge_list) == len(list1) + len(list2)):
			break

	return merge_list
				
def merge_sort(list1):
	"""
	Sort the elements of list1.

	Return a new sorted list with the same elements as list1.

	This function should be recursive.
	"""
	
	if(list1 == []):
		return []
	else:
		first = list1[0]
		smaller_lst = [num for num in list1 if num < first]
		equal_lst = [num for num in list1 if num == first]
		bigger_lst = [num for num in list1 if num > first]

	return merge(merge_sort(smaller_lst) + equal_lst, merge_sort(bigger_lst))		


# Function to generate all strings for the word wrangler game
def gen_all_strings(word):
	"""
	Generate all strings that can be composed from the letters in word
	in any order.

	Returns a list of all strings that can be formed from the letters
	in word.

	This function should be recursive.
	"""
	all_strings = []

	if(word == ""):
		return [""]
	else:
		first = word[0]
		rest = gen_all_strings(word[1:])
		all_strings.append(first)

		for char in rest:
			all_strings.append(char)

			if(char != ""):
				all_strings.append(first+char)
				all_strings.append(char+first)

				for idx in range(1, len(char)):
					all_strings.append(char[idx:] + first + char[:idx])

	return all_strings
	

# Function to load words from a file
def load_words(filename):
	"""
	Load word list from the file named filename.

	Returns a list of strings.
	"""

	url = codeskulptor.file2url(WORDFILE)
	netfile = urllib2.urlopen(url)
	
	word_list=[]
	for line in netfile.readlines():
		word_list.append( line[:-1] )
	return word_list

def run():
	"""
	Run game.
	"""
	words = load_words(WORDFILE)
	wrangler = provided.WordWrangler(words, remove_duplicates, 
									 intersect, merge_sort, 
									 gen_all_strings)
	provided.run_game(wrangler)


# Run the game
run()

