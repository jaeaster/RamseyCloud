

from FileManager import FileManager
from MatrixIterator import MatrixIterator
from MatrixManager import MatrixManager
from Static import Static
class Validator:

	def __init__(self):
		self.file_manager = FileManager()
		self.matrix_iterator = MatrixIterator()
		self.matrix_manager = MatrixManager()
		self.static = Static()


	def validate(self, start, stopp):                                                                
		for i in range(start, stopp + 1):
			matrix = self.file_manager.read_matrix_from_file(self.static.PATH_STRING_SOLUTION ,self.file_manager.generate_filename_string(i), i)                                                        
			matrise = self.matrix_manager.matrix_to_array(matrix)                
			print(self.file_manager.generate_filename_string(i) + "   " + str(i))                                            
			self.check_diagonal(matrix)

			counter_ex,count  = self.matrix_iterator.is_counter_example(matrise, i)                                    
			if counter_ex is False:                                                              
				print(" Matrix " + str(i) + " is not a counter example")                          
				print("count "+ str(count))                                                      
			else:                                                                                
				#print("count "+ str(count))                                                      
				print(str(i) + "  OK")
				print "\n"

	def check_diagonal(self, matrix):
		counter = 0
		for i in range(len(matrix)):
			if matrix[counter][counter] == 1:
				print "There is a 1 on the diagonal"
			counter +=1			




