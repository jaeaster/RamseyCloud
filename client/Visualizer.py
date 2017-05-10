
from Static import Static
import sys

class Visualizer:

	def __init__(self):
		self.static = Static()

	def print_clique_counts(self, clique_type_list, clique_type_counts):
		print "\nCLique Counts"
		for i in range(len(clique_type_list)):
			print "%s: %d\n" %(clique_type_list[i], clique_type_counts[i])

	def print_cover_and_dirty_set(self, cover_set, dirty_set):
		print "\nCover set: "
		print cover_set
		print "\nDirty:"
		print dirty_set
		print "\n"


	def print_status_bar(self, status):
		pass



	def print_matrix(self,matrix):  # Prints the matrix, not feasible for sizes bigger than ish 20
	    delimitter = " | "
	    line = delimitter
	    for i in range(len(matrix[0])):
	        for j in range(len(matrix[0])):
	            line += str(matrix[i][j]) + delimitter
	        print(delimitter + str(i) + "- " + line + "\n")
	        line = delimitter

	def print_dictionary(self, dictionary):
	    for key in dictionary:
	        print "%d: %s" %(key, str(dictionary[key]))

	def print_tupled_dictionary(self, dictionary):
		if len(dictionary) == 0:
			print "	Empty"
		for key in dictionary:
			print "Node: %d, count: %d" %(key[0], key[1])

	def print_nodes(self, blue_counter_dict, red_counter_dict):
	    sorted_blue = sorted(blue_counter_dict.items(), key=operator.itemgetter(1))   
	    sorted_red = sorted(red_counter_dict.items(), key=operator.itemgetter(1))
	    sorted_blue.reverse()
	    sorted_red.reverse()   
	    print "\nBlue"
	    print_tupled_dictionary(sorted_blue)
	    print "\nRed"
	    print_tupled_dictionary(sorted_red)
	    print "\n"

	def print_hollywood_sign(self, dim, counter):
	    print "\n"
	    print self.static.HASHTAGS
	    print("#  Working on %d (%d)  #") %(dim, counter)
	    print self.static.HASHTAGS

	def print_double_array(self, double_array):
		for elem in double_array:
			print elem
			print "\n"

	def print_color_clique_counts(self, blue_clique_count, red_clique_count):
		print "BLUE COUNT: %d" %blue_clique_count
		print "RED COUNT: %d" %red_clique_count
		print '\n'
