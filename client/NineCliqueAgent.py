
from Static import Static
from FileManager import FileManager
from MatrixManager import MatrixManager
from NetworkManager import NetworkManager
from MatrixIterator import MatrixIterator
from Visualizer import Visualizer
from TenCliqueManager import TenCliqueManager
from random import randint
import collections
import operator

class NineCliqueAgent:

	def __init__(self, network_manager):
		self.static = Static()
		self.file_manager = FileManager()
		self.matrix_manager = MatrixManager()
		self.network_manager = network_manager
		self.matrix_iterator = MatrixIterator()
		self.visualizer = Visualizer()
		self.ten_clique_manager = TenCliqueManager()


	def reduce(self, matrix,cover_set_log):
		print "Reduce\n"
		c5,c6,c7,c8,c9,c10, nine_clique_double_array,ten_clique_double_array = self.matrix_iterator.clique_counter_c(matrix)
		self.visualizer.print_double_array(ten_clique_double_array)
		if c10 ==0:
			print "Found counter example"
			return matrix, True, 0, 0, [], []
		else:
			flipped_matrix = matrix
			blue_clique_count, red_clique_count = self.count_number_of_cliques(ten_clique_double_array)
			self.visualizer.print_color_clique_counts(blue_clique_count, red_clique_count)
			self.visualizer.print_clique_counts(self.static.CLIQUE_TYPE_LIST, [c9,c10])
			#cover_set, dirty_cover_set = self.generate_coverset_based_on_nine_cliques(nine_clique_double_array, all_ten_clique_tuples,color_map)
			cover_set, dirty_set = self.ten_clique_manager.choose_tuple_for_all_ten_cliques(ten_clique_double_array, nine_clique_double_array) 
			#self.visualizer.print_cover_and_dirty_set(cover_set, dirty_set)
			flipped_matrix = self.flip_edges_from_nine_clique_cover_set(matrix, cover_set, dirty_set)
			return flipped_matrix, False, blue_clique_count, red_clique_count,cover_set, dirty_set

####################################
#        Complements reduce()      # 
####################################
	def count_number_of_cliques(self,double_array):
		blue_count = 0
		red_count = 0
		for elem in double_array:
			if elem[0] == 0:
				blue_count += 1
			else: red_count += 1
		return blue_count, red_count


#####################################################################
#        Complements generate_coverset_based_on_nine_cliques()      # 
#####################################################################

	def flip_edges_from_nine_clique_cover_set(self, matrix, cover_set, dirty_set):
		flipped_matrix = matrix
		clean_string = '\nClean: Chose to Flip:\n '
		dirty_string = '\nDirty: Chose to Flip:\n '
		for elem in cover_set:
			x = elem[0]
			y = elem[1]
			clean_string += str(elem)
			flipped_matrix = self.matrix_manager.flip_one_bit(flipped_matrix, x, y)
		for elem in dirty_set:
			x = elem[0]
			y = elem[1]
			dirty_string += str(elem)
			flipped_matrix = self.matrix_manager.flip_one_bit(flipped_matrix, x,y)
		print clean_string
		print dirty_string
		return flipped_matrix




if __name__ == '__main__':
	n_m = NetworkManager()
	agent = NineCliqueAgent(n_m)
	t = [[0,1,2,3,4,5,6,7,8,9,10]]
	n = [[0,2,3,4,5,6,7,8,9,10],[0,1,3,4,5,6,7,8,9,10]]

	b_n, r_n  = agent.generate_nine_clique_set(n)
	"\nBlue nine clique set"
	print b_n
	"\nRed nine clique set"
	print r_n



