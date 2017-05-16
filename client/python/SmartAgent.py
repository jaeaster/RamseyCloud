
from Static import Static
from FileManager import FileManager
from MatrixManager import MatrixManager
from NetworkManager import NetworkManager
from MatrixIterator import MatrixIterator
from Visualizer import Visualizer
from random import randint
import collections
import operator

class SmartAgent:

	def __init__(self, network_manager):
		self.static = Static()
		self.file_manager = FileManager()
		self.matrix_manager = MatrixManager()
		self.network_manager = network_manager
		self.matrix_iterator = MatrixIterator()
		self.visualizer = Visualizer()

#################################
#      Reduction Algorithms     # 
#################################

	def smart_reduction(self, matrix,cover_set_log):
		print "SMART REDUCTION\n"
		c5,c6,c7,c8,c9,c10,ten_clique_double_array = self.matrix_iterator.clique_counter_c(matrix)
		#self.visualizer.print_double_array(ten_clique_double_array)
		if c10 ==0:
			print "Found counter example"
			return matrix, True, 0, 0, [], []
		else:
			flipped_matrix = matrix
			blue_clique_count, red_clique_count = self.count_number_of_cliques(ten_clique_double_array)
			all_cover_sets, backup_sets = self.find_multiple_cover_sets(ten_clique_double_array)
			self.visualizer.print_clique_counts(blue_clique_count, red_clique_count)
			smart_cover_set = all_cover_sets[0]
			smart_cover_set = self.handle_cover_set_loop(smart_cover_set, all_cover_sets, cover_set_log, backup_sets)
			flipped_matrix = self.flip_edges_from_smart_cover_set(matrix, smart_cover_set)
			return flipped_matrix, False, blue_clique_count, red_clique_count,smart_cover_set,backup_sets

####################################
#   Complements Smart Reduction    # 
####################################
	def find_multiple_cover_sets(self,double_array):  # fiks slik at valg av tuppel blant de med alternativer er random
		number_of_cliques = len(double_array)  # number of cliques
		clique_set_length = len(double_array[0])
		setlist = []
		backup_sets = []*number_of_cliques
		for i in range(number_of_cliques):
			clique_tuple_set = []
			for j in range(1, clique_set_length+1):
				for k in range(j + 1, clique_set_length):
					a = double_array[i][j]
					b = double_array[i][k]
					d = [a,b]
					if (d[0:2] not in clique_tuple_set):
						clique_tuple_set.append(d[0:2])
						#print(" set nr : " + str(i) + "    appending " + str(d[0:2]))
					for l in range(number_of_cliques):  # if both nodes are in the clique, that edge is a part of that clique
						if (a in double_array[l][1:]) and (b in double_array[l][1:]):  # if a and b are nodes i clique l -> then a,b is an edge i clique l
							d.append(l)
					setlist.append(d)  # format ->  nodeA,nodeB,C1,C2..
			backup_sets.append(clique_tuple_set)
		setlist_sorted = sorted(setlist, key=len,reverse=True)  # sorted list of each edge and its corresponding 10-clique memberships
		coverset_tuples = []
		coverset_cliques = []
		coversets = []
		add_to_cover = False
		for tu in range(len(setlist_sorted)):  # for each edge that is in a 10-clique
			for elem in setlist_sorted[tu][2:]:  # for each of the cliques this edge is a member of
				if elem not in coverset_cliques:  # if this clique is not represented in the coverset, then add this edge to coverset
					add_to_cover = True
					coverset_cliques.append(elem)
			if add_to_cover:
				coverset_tuples.append(setlist_sorted[tu][:2])
			add_to_cover = False
			if len(coverset_cliques) == number_of_cliques:
				if coverset_tuples not in coversets:
					coversets.append(coverset_tuples)
					coverset_tuples = []
					coverset_cliques = []
					continue
		return coversets,backup_sets

	def make_random_coverset(self, backup_sets):
		coverset = []
		for i in range(len(backup_sets)):
			a = randint(0,len(backup_sets[i])-1)
			coverset.append(backup_sets[i][a])
		return coverset

	def count_number_of_cliques(self,double_array):
		blue_count = 0
		red_count = 0
		for elem in double_array:
			if elem[0] == 0:
				blue_count += 1
			else: red_count += 1
		return blue_count, red_count

	def handle_cover_set_loop(self, smart_cover_set, all_cover_sets ,cover_set_log, backup_sets):
		counter = 0
		while smart_cover_set in cover_set_log:
			counter +=1
			if counter < len(all_cover_sets):
				smart_cover_set = all_cover_sets[counter]
			else:
				smart_cover_set = self.make_random_coverset(backup_sets)
				print("hit a loop, changing the coverset")
		return smart_cover_set

	def flip_edges_from_smart_cover_set(self, matrix, smart_cover_set):
		string = "chose to flip\n "
		flipped_matrix = matrix
		for elem in smart_cover_set:
			string += str(elem)
			x = elem[0]
			y = elem[1]
			flipped_matrix = self.matrix_manager.flip_one_bit(flipped_matrix, x, y)
		print string
		print("found an appropriate new coverset")
		return flipped_matrix



