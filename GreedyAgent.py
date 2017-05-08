
from Static import Static
from FileManager import FileManager
from MatrixManager import MatrixManager
from NetworkManager import NetworkManager
from MatrixIterator import MatrixIterator
from Visualizer import Visualizer
from random import randint
import collections
import operator

class GreedyAgent:

	def __init__(self):
		self.static = Static()
		self.file_manager = FileManager()
		self.matrix_manager = MatrixManager()
		self.network_manager = NetworkManager()
		self.matrix_iterator = MatrixIterator()
		self.visualizer = Visualizer()

#################################
#      Reduction Algorithms     # 
#################################

	#Swaps the edge participating in most cliques until nodes only participate in "threshold" amounts of cliques, and returns the matrix
	def greedy_reduction(self,matrix):
	    print "GREEDY" 
	    c5,c6,c7,c8,c9,c10,ten_clique_double_array = self.matrix_iterator.clique_counter(self.matrix_manager.matrix_to_array(matrix), len(matrix[0]))
	    if c10 ==0:
	        print "Found counter example"
	        return matrix, True, 0, 0
	    else:
	        #blue_counter_dict, red_counter_dict = self.participation_count(ten_clique_double_array)
	        blue_clique_count, red_clique_count = self.count_number_of_cliques(ten_clique_double_array)
	        color_to_optimize = self.choose_color_to_optimize(ten_clique_double_array)
	        sorted_blue, sorted_red = self.generate_sorted_dictionary_from_double_array(ten_clique_double_array)
	        x, y = self.choose_nodes_to_flip_greedy(color_to_optimize, sorted_blue, sorted_red)      
	        print "\nChose to flip %d and %d" %(x,y)
	        flipped_matrix = self.matrix_manager.flip_one_bit(matrix, x, y)
	        return flipped_matrix, False, blue_clique_count, red_clique_count

	def k_greedy_reduction(self, matrix):
		c5,c6,c7,c8,c9,c10,ten_clique_double_array = self.matrix_iterator.clique_counter(self.matrix_manager.matrix_to_array(matrix), len(matrix[0]))
		if c10 ==0:
			print "Found counter example"
			return matrix, True, 0, 0
		else:
			blue_clique_count, red_clique_count = self.count_number_of_cliques(ten_clique_double_array)
			sorted_blue, sorted_red = self.generate_sorted_dictionary_from_double_array(ten_clique_double_array)
			blue_k = self.determine_k(sorted_blue)
			red_k = self.determine_k(sorted_red)
			print "\nGREEDY - Blue k: %d , Red k: %d" %(blue_k, red_k)
			blue_nodes_to_flip = self.determine_nodes_to_flip_by_k_and_threshold(blue_k,sorted_blue)
			red_nodes_to_flip = self.determine_nodes_to_flip_by_k_and_threshold(red_k,sorted_red)
			flipped_matrix = self.flip_nodes_by_next(matrix, blue_nodes_to_flip)
			flipped_matrix = self.flip_nodes_by_next(flipped_matrix, red_nodes_to_flip)
			return flipped_matrix, False, blue_clique_count, red_clique_count


####################################
#   Complements Greedy Methods     # 
####################################

	#Array Argument
	def choose_color_to_optimize(self,double_array): #Choses the color that creates the most cliques
	    blue_counter = 0
	    red_counter = 0
	    for elem in double_array:
	        if elem[0] == 0:
	            blue_counter += 1
	        else:
	            red_counter += 1
	    if blue_counter > red_counter:
	        return 0
	    else:
	        return 1

	#returns two dictionar, one for each color, containing nodes that participate in cliques and the number of cliques they paricipate in
	def participation_count(self, double_array):
	    blue_counter_dict = {}
	    red_counter_dict = {}
	    for elem in double_array:
	        color = elem[0]
	        if color == 0:
	            for i in range(1, len(elem)):
	                temp_key = elem[i]
	                if not self.is_in_dictionary(blue_counter_dict, temp_key):
	                    blue_counter_dict[temp_key] = 1
	                else:
	                    blue_counter_dict[temp_key] += 1
	        else:
	            for i in range(1, len(elem)):
	                temp_key = elem[i]
	                if not self.is_in_dictionary(red_counter_dict, temp_key):
	                    red_counter_dict[temp_key] = 1
	                else:
	                    red_counter_dict[temp_key] += 1
	    return blue_counter_dict, red_counter_dict

	def count_number_of_cliques(self, double_array):
	    blue_count = 0
	    red_count = 0
	    for elem in double_array:
	        if elem[0] == 0:
	            blue_count += 1
	        else: red_count += 1
	    return blue_count, red_count

	def generate_sorted_dictionary_from_double_array(self, double_array):
	    blue_counter_dict, red_counter_dict = self.participation_count(double_array)
	    sorted_blue = self.sort_dictionary(blue_counter_dict)
	    sorted_red = self.sort_dictionary(red_counter_dict)
	    print "BLUE"
	    self.visualizer.print_tupled_dictionary(sorted_blue)
	    print "\nRED"
	    self.visualizer.print_tupled_dictionary(sorted_red)
	    return sorted_blue, sorted_red

	#Dictionary Argument
	#Returns the edge participating in most cliques
	def choose_nodes_to_flip_greedy(self, color_to_optimize, sorted_blue, sorted_red):
	    if color_to_optimize == 0:
	            return sorted_blue[0][0], sorted_blue[1][0]
	    else:
	        return sorted_red[0][0], sorted_red[1][0]

	def sort_dictionary(self,dictionary):
	    sorted_dictionary = sorted(dictionary.items(), key=operator.itemgetter(1))
	    sorted_dictionary.reverse()
	    return sorted_dictionary

	def is_empty_dictionary(self,dictionary):
		return not bool(dictionary)

	def is_in_dictionary(self, dictionary, test_key):
		for key in dictionary:
			if test_key == key:
				return True
		return False

	def determine_k(self, sorted_dictionary):
		k = 0
		for key in sorted_dictionary:
			k = key[1]
			break
		return k


	def determine_nodes_to_flip_by_k_and_threshold(self, k, sorted_dict):
		nodes_to_flip = []
		sub_k = 2*k
		for key in sorted_dict:
			if sub_k > 0:
				nodes_to_flip.append(key[0])
				sub_k -= 1
		if not self.is_even(len(nodes_to_flip)):
			del nodes_to_flip[-1]
		return nodes_to_flip

	def flip_nodes_by_next(self, matrix, nodes_to_flip_by_next):
		flipped_matrix = matrix
		for i in range(0,len(nodes_to_flip_by_next), 2):
			print "flipping %d and %d" %(nodes_to_flip_by_next[i], nodes_to_flip_by_next[i+1])
			flipped_matrix = self.matrix_manager.flip_one_bit(matrix, nodes_to_flip_by_next[i], nodes_to_flip_by_next[i+1])
		return flipped_matrix

	def is_even(self, number):
		return number%2 == 0







