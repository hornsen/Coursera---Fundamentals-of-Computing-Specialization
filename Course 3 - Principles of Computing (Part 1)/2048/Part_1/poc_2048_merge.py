"""
This program is a game called 2048
"""

def merge(line):
	"""
	Function that merges a single row or column in 2048.
	"""
	
	old_lst=line
	new_lst=[0]*len(old_lst)
	
	if(len(old_lst) == 1):
		new_lst[0] = old_lst[0]
	
	else:
		merge_allowed = True
		counter=0
		print("\n\n*** Start iteration ***\n")
		
		
		if(old_lst[0] == 0): 
			first_num_is_zero = True
			
		elif(old_lst[0] >= 0):
			new_lst[0] = old_lst[0]
			first_num_is_zero = False
		
							
		for num in range(1, len(old_lst), 1):
			print("\n")
			
			if(old_lst[num] != 0):
				
				
				if(first_num_is_zero == True and old_lst[num] >0):
					print("Iteration %s\n" % num)
					print("Section 1")
					print("Before iteration: %s" % old_lst)
					
					new_lst[0] = old_lst[num]
					first_num_is_zero = False	
					
					print("After iteration: %s" % new_lst)
				
				elif(first_num_is_zero == False):
					
					
					if(old_lst[num] == new_lst[counter] and merge_allowed == True):
						print("Iteration %s\n" % num)
						print("Section 2")
						print("Before iteration: %s" % old_lst)
						
						new_lst[counter] = old_lst[num] * 2
						merge_allowed = False
						
						print("After iteration: %s" % new_lst)

					elif(old_lst[num] != new_lst[counter] or merge_allowed == False):
						print("Iteration %s\n" % num)
						print("Section 3")
						print("Before iteration: %s" % old_lst)
						
						counter += 1
						new_lst[counter] = old_lst[num]
						merge_allowed = True
						
						print("After iteration: %s" % new_lst)

		print("\n")
	return new_lst


print(str( merge([4]) ) + " should return [4]")
print(str( merge([8, 16, 16, 8]) ) + " should return [8, 32, 8, 0]")
print(str( merge([2, 0, 2, 4]) ) + " should return [4, 4, 0, 0]")
print(str( merge([2, 2, 0, 0]) ) + " should return [4, 0, 0, 0]")
print(str( merge([0, 0, 2, 2]) ) + " should return [4, 0, 0, 0]")
print(str( merge([2, 2, 2, 2, 2]) ) + " should return [4, 4, 2, 0, 0]")
print(str( merge([4, 8, 4, 4, 8]) ) + " should return [4, 8, 8, 8, 0]")

