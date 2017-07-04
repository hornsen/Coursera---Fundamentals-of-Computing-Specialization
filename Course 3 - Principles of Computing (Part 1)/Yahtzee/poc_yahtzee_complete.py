"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

try:
    import codeskulptor
except ImportError:
    import SimpleGUICS2Pygame.codeskulptor as codeskulptor

#import codeskulptor 
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
	"""
	Iterative function that enumerates the set of all sequences of
	outcomes of given length.
	"""

	answer_set = set([()])
	for dummy_idx in range(length):
		temp_set = set()
		for partial_sequence in answer_set:
			for item in outcomes:
				new_sequence = list(partial_sequence)
				new_sequence.append(item)
				temp_set.add(tuple(new_sequence))
		answer_set = temp_set
	return answer_set


def score(hand):
	"""
	Compute the maximal score for a Yahtzee hand according to the
	upper section of the Yahtzee score card.

	hand: full yahtzee hand

	Returns an integer score 
	"""
	hand_value=dict()
	if(len(hand) == 0):
		return 0
	else:
		for num in hand:
			if(num in hand_value):
				hand_value[num] += num
			elif(num not in hand_value):
				hand_value[num] = num

		max_score = None	
		for idx in hand_value:
			if(max_score <= hand_value[idx]):
				max_score = hand_value[idx]
		
		return max_score



def expected_value(held_dice, num_die_sides, num_free_dice):
	"""
	Compute the expected value based on held_dice given that there
	are num_free_dice to be rolled, each with num_die_sides.

	held_dice: dice that you will hold
	num_die_sides: number of sides on each die
	num_free_dice: number of dice to be rolled

	Returns a floating point expected value
	"""

	sequence = [num for num in range(1, num_die_sides +1)]
	
	total_score=0
	for idx in gen_all_sequences(sequence, num_free_dice):
		total_score += score(idx + held_dice)

	return float(total_score) / len(gen_all_sequences(sequence, num_free_dice))

def gen_all_holds(hand):
	"""
	Generate all possible choices of dice from hand to hold.

	hand: full yahtzee hand

	Returns a set of tuples, where each tuple is dice to hold
	"""
	
	possible_choices=[()]

	for value in hand:
		for item in possible_choices:
			possible_choices = possible_choices + [tuple(item) + (value, )]

	return set(possible_choices)



def strategy(hand, num_die_sides):
	"""
	Compute the hold that maximizes the expected value when the
	discarded dice are rolled.

	hand: full yahtzee hand
	num_die_sides: number of sides on each die

	Returns a tuple where the first element is the expected score and
	the second element is a tuple of the dice to hold
	"""

	best_hand=()
	num_free_dice = len(hand) - len(best_hand)
	best_hand_ev = expected_value(best_hand, num_die_sides, num_free_dice)

	for hold in gen_all_holds(hand):
		if(hold != ()):
			if( best_hand_ev < expected_value(hold, num_die_sides, len(hand) - len(hold)) ):
				best_hand_ev = expected_value(hold, num_die_sides, len(hand) - len(hold))
				best_hand=hold
	
	return (best_hand_ev, best_hand)
	

def run_example():
	""" 
	Compute the dice to hold and expected score for an example hand
	"""
	num_die_sides = 6
	hand = (5, 1, 1, 3, 6, 3, 1, 6)
	hand_score, hold = strategy(hand, num_die_sides)
	print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
	
    
run_example()


import poc_holds_testsuite
poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    
    



