
from FileManager import FileManager
from NetworkManager import NetworkManager
from MatrixManager import MatrixManager
from Visualizer import Visualizer
from MatrixIterator import MatrixIterator
import time
from random import randint
import random
class NewMatrixAgent:

	def __init__(self, network_manager):
		#self.static = Static()
		self.file_manager = FileManager()
		self.matrix_manager = MatrixManager()
		self.network_manager = network_manager
		self.matrix_iterator = MatrixIterator()
		self.visualizer = Visualizer()
		self.previous_dirty_set = []



	def mini_matrix_reduction(self, matrix):
		print "New MAtrix Agent\n"
		c5,c6,c7,c8,c9,c10,ten_clique_double_array = self.matrix_iterator.clique_counter_c(matrix)
		if c10 ==0:
			print "Found counter example"
			self.previous_dirty_set = []
			return matrix, True, 0, 0#, [], []
		else:
			flipped_matrix = matrix
			blue_clique_count, red_clique_count = self.count_number_of_cliques(ten_clique_double_array)
			
			print "Number of ten cliques in graph: %d" %c10
			print "\nBLUE: %d" %blue_clique_count
			print "\nRED %d\n" %red_clique_count
			
			clean_set, dirty_set = self.manage_ten_cliques(matrix, ten_clique_double_array)
			

			self.add_dirty_tuples_to_previous_dirty_set(dirty_set)
			print "Clean: %s" %str(clean_set)
			print "Dirty: %s" %str(dirty_set)
			flipped_matrix = self.flip_edges_from_clean_and_dirty_cover_set(matrix, clean_set, dirty_set)
			return flipped_matrix, False, blue_clique_count, red_clique_count#,smart_cover_set,backup_sets

	def count_number_of_cliques(self,double_array):
		blue_count = 0
		red_count = 0
		for elem in double_array:
			if elem[0] == 0:
				blue_count += 1
			else: 
				red_count += 1
		return blue_count, red_count

	def add_dirty_tuples_to_previous_dirty_set(self, dirty_set):
		for elem in dirty_set:
			self.previous_dirty_set.append(elem)

	def generate_ten_clique_tuples(self, ten_clique_array):
		clique_array_length = len(ten_clique_array)
		tuple_list = []
		color = ten_clique_array[0]
		for j in range(1, clique_array_length+1):
			for k in range(j + 1, clique_array_length):
				tuple_list.append((ten_clique_array[j],ten_clique_array[k]))
		return tuple_list, color


	def manage_ten_cliques(self,matrix,ten_clique_double_array):
		clean_tuple_set = []
		dirty_set = []
		counter = 0
		print "Number of ten cliques: %d\n" %len(ten_clique_double_array)
		for ten_clique in ten_clique_double_array:
			fourty_five_tuples, color = self.generate_ten_clique_tuples(ten_clique)
			if self.is_resolved(fourty_five_tuples, clean_tuple_set, dirty_set):
				continue
			inv_color = self.invert_color(color)
			if counter % 10 == 0:
				print "%d / %d" %(counter,len(ten_clique_double_array))
			counter += 1
			best_cost = 10000
			best_dirty_tuple = []
			for k in range(45):
				clean_tuples_for_current_ten_clique = []
				tup = fourty_five_tuples[k]
				node_one = tup[0]
				node_two = tup[1]
				mini_matrix, sub_set = self.generate_sub_set_matrix(matrix, tup, color)
				c5,c6,c7,c8,c9,c10,mini_ten_clique_double_array = self.matrix_iterator.clique_counter_c(mini_matrix)
				temp_cost = len(mini_ten_clique_double_array)
				if temp_cost == 0:
					if tup not in clean_tuple_set:
						clean_tuple_set.append(tup)
					break
				else:
					if temp_cost == best_cost:
						best_dirty_tuple.append(tup)
					elif temp_cost < best_cost:
						best_cost = temp_cost
						best_dirty_tuple = [tup]
				if k == 44 and len(best_dirty_tuple) >= 1:
					a = best_dirty_tuple[random.randint(0,len(best_dirty_tuple)-1)]
					while a in self.previous_dirty_set:
						a = fourty_five_tuples[random.randint(0,44)]
					dirty_set.append(a)					

		return clean_tuple_set, dirty_set

	def is_resolved(self, fourty_five_tuples, clean_set, dirty_set):
		for elem in fourty_five_tuples:
			if elem in clean_set or elem in dirty_set:
				return True
		return False


	def generate_sub_set_matrix(self, matrix, tup, color):
		node_one = tup[0]
		node_two = tup[1]
		inv_color = self.invert_color(color)

		dim = len(matrix[0])
		sub_set = [node_one,node_two]
		for i in range(dim):
			if matrix[i][node_one] == matrix[i][node_two] and matrix[i][node_one] == inv_color:
				sub_set.append(i)
		sub_set_length = len(sub_set)
		mini_matrix = self.matrix_manager.make_matrix(sub_set_length)
		for j in range(len(sub_set)-1):
			for k in range(j+1,len(sub_set)):
				mini_matrix[j][k] = matrix[sub_set[j]][sub_set[k]]
				mini_matrix[k][j] = matrix[sub_set[j]][sub_set[k]]
		mini_matrix[0][1] = inv_color
		mini_matrix[1][0] = inv_color
		return mini_matrix, sub_set


	def flip_edges_from_clean_and_dirty_cover_set(self, matrix, clean_cover_set, dirty_set):
		clean_string = "chose to flip from clean"
		flipped_matrix = matrix
		for elem in clean_cover_set:
			clean_string += str(elem)
			x = elem[0]
			y = elem[1]
			flipped_matrix = self.matrix_manager.flip_one_bit(flipped_matrix, x, y)
		print clean_string
		print "\n"
		dirty_string = 'chose to flip from dirty: '
		for elem in dirty_set:
			dirty_string += str(elem)
			x = elem[0]
			y = elem[1]
			flipped_matrix = self.matrix_manager.flip_one_bit(flipped_matrix, x, y)
		print dirty_string
		return flipped_matrix


	def invert_color(self, color):
		return (color + 1)%2


