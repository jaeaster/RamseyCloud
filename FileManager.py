

from Static import Static
from MatrixManager import MatrixManager
import os

class FileManager:

	def __init__(self):
		self.static = Static()
		self.matrix_handler = MatrixManager()

	def generate_filename_string(self, dimension):#Returns the filename of the counter example of size "size"
		return str("ramsey-" + str(dimension) + ".txt")

	def highest_ramsey_dir(self): #Searches for and returns the filename of the highest counter example in your directory
	    highest = 0
	    for fil in os.listdir(self.static.PATH_STRING_SOLUTION):
	        if fil.startswith("ramsey-"):
	            a = str(fil)
	            a = a[7:-4]
	            if int(a) > highest:
	                highest = int(a)
	    return self.generate_filename_string(highest)

	def exists_higher_counter_example(self,current):  # Returns True if the input number is lower than highest available
		currentfile = self.highest_ramsey_dir()
		if int(currentfile[7:-4]) >= current:
			return True

	def write_matrix_to_file(self, matrix, directory, filename):
	    dim = len(matrix[0])
	    path = directory + filename
	    string = ''
	    for i in range(dim):
	        for j in range(dim):
	            string += str(matrix[i][j])
	        string += "\n"
	    string_to_write = string[:-1]
	    with open(path, "w") as out:
	        out.write(string_to_write)

	def read_highest_from_file(self): #Return highest available matrix
	    filename = self.highest_ramsey_dir()
	    dim = int(filename.replace("ramsey-", "").replace(".txt", ""))
	    return self.read_matrix_from_file(self.static.PATH_STRING_SOLUTION,filename, dim)

	def read_matrix_from_file(self,directory, filename, dimension):  #Reads a matrix from file
	    path = directory + filename
	    delimitter = "-"
	    matrix = self.matrix_handler.make_matrix(dimension)
	    lineattributes = [0] * dimension
	    with open(path, "r") as read_file:
	        for i in range(dimension):
	            line = read_file.readline().replace("\n", "").replace(delimitter, "")
	            for j in range(len(line)):
	                lineattributes[j] = line[j]
	            for j in range(dimension):
	                matrix[i][j] = int(lineattributes[j])
	    return matrix

	def append_to_file(self, string_to_write,file_name):
	    path = self.static.PATH_STRING_SOLUTION + file_name
	    f = open(path, 'a')
	    f.write(string_to_write)
	    f.close()

	def generate_string_to_append(self,values):
	    string = ''
	    delimitter = "|"
	    for elem in values:
	        temp_string = "%d%s" %(elem, delimitter)
	        string += temp_string
	    return string

	def generate_solution_filename(self,matrix):
	    dim = len(matrix[0])
	    return self.generate_filename_string(dim)

	def generate_improvement_filename(self,matrix, blue_count, red_count):
	    dim = len(matrix[0])
	    filename = '%s-%d-%d-%d-.txt' %("improvement", dim, blue_count, red_count)
	    return filename
