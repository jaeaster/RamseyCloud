
import random
from random import randint

class MatrixManager:

	def __init__(self):
		pass

#####################################
#     Trivial Matrix Operations     #
#####################################
	def make_matrix(self,dimension):  #ln Creates and returns a matrix with zeroes of size "dimension"
		return [[0 for col in range(dimension)] for row in range(dimension)]

	def make_random_matrix(self,dimension):
	    return [[randint(0,1) for col in range(dimension)] for row in range(dimension)]

	def expand_matrix(self, matrix):# Expands the matrix with one additional node, with randomly colored edges
	    prev_size = len(matrix[0])
	    new_matrix = self.make_matrix(prev_size +	 1)
	    for i in range(prev_size):
	        for j in range(prev_size):
	            new_matrix[i][j] = matrix[i][j]

	    for k in range(prev_size):
	        a = randint(0, 1)
	        new_matrix[prev_size][k] = a
	        new_matrix[k][prev_size] = a
	    return new_matrix

	def expand_matrix_k_times(self, matrix, k):
	    for i in range(k):
	        matrix = self.expand_matrix(matrix)
	    return matrix

	def matrix_to_array(self, matrix):#Converts a matrix to a one dimensional array
	    dim = len(matrix[0])
	    out_array = [0] * (dim ** 2)
	    for i in range(dim):
	        for j in range(dim):
	            out_array[i * dim + j] = matrix[i][j]
	    return out_array

	def flip_one_bit(self, matrix, x, y):
		if x == y:
			print "OMG You flipped the diagonal"
			return matrix
		value = matrix[x][y]
		if value == 1:
			matrix[x][y] = 0
			matrix[y][x] = 0
		else:
			matrix[x][y] = 1
			matrix[y][x] = 1
		return matrix


#################################
#       Matrix Algorithms       # 
#################################
	def bit_flipper(self, matrix):  #flips random place in the matrix
		dim = len(matrix[0])
		a = randint(0, dim - 1)
		b = randint(0, dim - 1)
		while a == b:
			a = randint(0, dim - 1)
			b = randint(0, dim - 1)
		if matrix[a][b] == 0:
			matrix[a][b] = 1
			matrix[b][a] = 1
		else:
			matrix[a][b] = 0
			matrix[b][a] = 0
		return matrix


	def bit_flipper_edge(self, matrix):  # flips random bit on the edge of the matrix
	    a = len(matrix[0])
	    b = randint(0, a - 1)
	    if matrix[b][a - 1] == 0:
	        matrix[a - 1][b] = 1
	        matrix[b][a - 1] = 1
	    else:
	        matrix[a - 1][b] = 0
	        matrix[b][a - 1] = 0
	    return matrix


	def re_shuffle_edge(self, matrix): #reshuffles the edges in the new expanded layer
	    size = len(matrix[0])
	    for i in range(size - 1):
	        a = randint(0, 1)
	        matrix[size - 1][i] = a
	        matrix[i][size - 1] = a
	    return matrix
