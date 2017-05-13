
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
		c5,c6,c7,c8,c9,c10,n,ten_clique_double_array = self.matrix_iterator.clique_counter_c(matrix)
		if c10 ==0:
			print "Found counter example"
			return matrix, True, 0, 0, [], []
		else:
			flipped_matrix = matrix
			blue_clique_count, red_clique_count = self.count_number_of_cliques(ten_clique_double_array)
			all_cover_sets, backup_sets = self.find_multiple_cover_sets(ten_clique_double_array)
			#self.visualizer.print_clique_counts(blue_clique_count, red_clique_count)
			print "C10: %d" %c10
			print "C9: %d" %c9
			smart_cover_set = all_cover_sets[0]
			smart_cover_set = self.handle_cover_set_loop(smart_cover_set, all_cover_sets, cover_set_log, backup_sets)
			#all_ten_clique_tuples, color_map = self.generate_ten_clique_tuples(ten_clique_double_array)
			#smart_cover_set, dirty_cover_set = self.generate_coverset_based_on_nine_cliques(nine_clique_double_array, all_ten_clique_tuples,color_map)
			flipped_matrix = self.flip_edges_from_smart_cover_set(matrix, smart_cover_set)
			#flipped_matrix = self.flip_edges_from_nine_clique_cover_set(matrix, smart_cover_set, dirty_cover_set)
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


	def generate_ten_clique_tuples(self, double_array):
		number_of_cliques = len(double_array)  # number of cliques
		clique_set_length = len(double_array[0])
		backup_sets = []*number_of_cliques
		color_map = []
		for i in range(number_of_cliques):
			clique_tuple_set = []
			color_map.append(double_array[i][0])
			for j in range(1, clique_set_length+1):
				for k in range(j + 1, clique_set_length):
					a = double_array[i][j]
					b = double_array[i][k]
					d = (a,b)
					clique_tuple_set.append(d)
			backup_sets.append(clique_tuple_set)
		return backup_sets, color_map

	def generate_coverset_based_on_nine_cliques(self, nine_clique_double_array, all_ten_clique_tuples, color_map):
		blue_set_list, red_set_list = self.generate_nine_clique_set(nine_clique_double_array)
		jump = False
		cover_set = []
		log = []
		list_of_dirty_cover_sets = []
		for i in range(len(all_ten_clique_tuples)): #For each of the ten cliques
			dirty_cover_set = []
			print "Done: %d / %d " %(i, len(all_ten_clique_tuples))
			for j in range(len(all_ten_clique_tuples[0])): #for each of the tuples in the ten-clique
				if jump:
					jump = False
					break
				if color_map[i] == 0:
					blue_temp_tup,blue_tup_count  = self.count_added_ten_cliques_by_tuple(all_ten_clique_tuples[i][j], blue_set_list)
					if blue_tup_count == 0:
						if blue_temp_tup not in log:
							cover_set.append((blue_temp_tup,i))
							log.append(blue_temp_tup)
						jump = True
						continue
					else:
						dirty_cover_set.append((blue_temp_tup,blue_tup_count,i))
				else:
					red_temp_tup, red_tup_count = self.count_added_ten_cliques_by_tuple(all_ten_clique_tuples[i][j], red_set_list)
					if red_tup_count == 0:
						if red_temp_tup not in log:
							cover_set.append((red_temp_tup,i))
							log.append(red_temp_tup)
						jump = True
						continue
					else:
						dirty_cover_set.append((red_temp_tup, red_tup_count, i))
			if len(dirty_cover_set) > 0:
				list_of_dirty_cover_sets.append((self.find_least_damaging_tuple(dirty_cover_set),i))
		return cover_set, list_of_dirty_cover_sets
			

	def generate_nine_clique_set(self, nine_clique_double_array):
		blue_set_list = []
		red_set_list = []
		for li in nine_clique_double_array:
			if li[0] == 0:
				blue_set_list.append(set(li[1:]))
			else:
				red_set_list.append(set(li[1:]))
		return blue_set_list, red_set_list


	def count_added_ten_cliques_by_tuple(self, tup, color_set_list):
		color_set_list_length = len(color_set_list)
		counter = 0
		for i in range(color_set_list_length-1):
			for j in range(i+1, color_set_list_length):
				set_i = color_set_list[i]
				set_j = color_set_list[j]
				if self.proceed_check(tup, set_i, set_j):
					diff = set_i.symmetric_difference(set_j)
					if len(diff) == 2 and tup[0] in diff and tup[1] in diff:
						counter += 1
		return tup,counter

	def find_least_damaging_tuple(self, dirty_cover_set):
		best_tup = None
		lowest = 100
		for double_tup in dirty_cover_set:
			if double_tup[1]< lowest:
				best_tup = double_tup[0]
				lowest = double_tup[1]
		return best_tup, lowest

	def proceed_check(self,tup, set_one, set_two):
		a = tup[0]
		b = tup[1]
		if a in set_one and b in set_two:
			if b in set_one or a in set_two:
				return False
			else:
				return True
		elif b in set_one and a in set_two:
			if a in set_one or b in set_two:
				return False
			else:
				return True
		else:
			return False

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

	def flip_edges_from_nine_clique_cover_set(self, matrix, cover_set, dirty_cover_set):
		flipped_matrix = matrix
		if len(cover_set) == 0:
			print "\nCOVER SET EMPTY!!!!!!!\n NEED BETTER WAY TO RECOVER"
			string = '\nChose to flip:\n'
			for elem in dirty_cover_set:
				x = elem[0][0][0]
				y = elem[0][0][1]
				string += (elem[0][0])
				string += ', cost: %d'%(elem[0][1])
			flipped_matrix = self.matrix_manager.flip_one_bit(flipped_matrix, x, y)
			print string
			return flipped_matrix
		string = 'Chose to Flip'
		for elem in cover_set:
			x = elem[0][0]
			y = elem[0][1]
			string += str(elem)
			flipped_matrix = self.matrix_manager.flip_one_bit(flipped_matrix, x, y)
		print string
		return flipped_matrix

	def find_least_damaging_dirty_tuple(self, dirty_cover_set):
		best_tup = None
		lowest = 100
		for elem in dirty_cover_set:
			temp_tup = elem[0][0]
			cost = elem[0][1]
			if cost < lowest:
				best_tup = temp_tup
				lowest 




if __name__ == '__main__':
	n = NetworkManager()
	sa = SmartAgent(n)
	dc = [(((1, 4), 1), 0)]
	#sa.flip_edges_from_nine_clique_cover_set([], dc)
	sa.find_least_damaging_dirty_tuple(dc)
	for elem in dc:
		x = elem[0][0][0]
		y = elem[0][0][1]
		print "%d - %d" %(x,y)






