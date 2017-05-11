from subprocess import Popen, PIPE, call
from MatrixManager import MatrixManager

class MatrixIterator:
	
	def __init__(self):
		self.matrix_manager = MatrixManager()
		pass

	def clique_counter(self, g):
	    count5 = 0
	    count6 = 0
	    count7 = 0
	    count8 = 0
	    count9 = 0
	    count10 = 0
	    sgsize = 10
	    newsize = len(g)-sgsize

	    ten_cliques = []
	    for i in range(newsize + 1):
	        for j in range(i + 1, newsize + 2):
	            for k in range(j + 1, newsize + 3):
	                i_to_j = g[i][j]
	                i_to = g[i]
	                j_to = g[j]
	                if (i_to_j == i_to[k]) and (i_to_j == j_to[k]):
	                    for l in range(k + 1, newsize + 4):
	                        k_to = g[k]
	                        if (i_to_j == i_to[l]) and (
	                                    i_to_j == j_to[l]) and (
	                                    i_to_j == k_to[l]):
	                            l_to = g[l]
	                            #print ([i, j, k, l])
	                            for m in range(l + 1, newsize + 5):
	                                if (i_to_j == i_to[m]) and (
	                                            i_to_j == j_to[m]) and (
	                                            i_to_j == k_to[m]) and (
	                                            i_to_j == l_to[m]):
	                                    m_to = g[m]
	                                    count5 += 1
	                                    #print ([i, j, k, l, m])
	                                    for n in range(m + 1, newsize + 6):
	                                        if (i_to_j == i_to[n]) and (
	                                                    i_to_j == j_to[n]) and (
	                                                    i_to_j == k_to[n]) and (
	                                                    i_to_j == l_to[n]) and (
	                                                    i_to_j == m_to[n]):
	                                            n_to = g[n]
	                                            count6 += 1
	                                            for o in range(n + 1, newsize + 7):
	                                                if (i_to_j == i_to[o]) and (
	                                                            i_to_j == j_to[o]) and (
	                                                            i_to_j == k_to[o]) and (
	                                                            i_to_j == l_to[o]) and (
	                                                            i_to_j == m_to[o]) and (
	                                                            i_to_j == n_to[o]):
	                                                    o_to = g[o]
	                                                    count7 += 1
	                                                    for p in range(o + 1, newsize + 8):
	                                                        if (i_to_j == i_to[p]) and (
	                                                                    i_to_j == j_to[p]) and (
	                                                                    i_to_j == k_to[p]) and (
	                                                                    i_to_j == l_to[p]) and (
	                                                                    i_to_j == m_to[p]) and (
	                                                                    i_to_j == n_to[p]) and (
	                                                                    i_to_j == o_to[p]):
	                                                            p_to = g[p]
	                                                            count8 += 1
	                                                            for q in range(p + 1, newsize + 9):
	                                                                if (i_to_j == i_to[q]) and (
	                                                                            i_to_j == j_to[q]) and (
	                                                                            i_to_j == k_to[q]) and (
	                                                                            i_to_j == l_to[q]) and (
	                                                                            i_to_j == m_to[q]) and (
	                                                                            i_to_j == n_to[q]) and (
	                                                                            i_to_j == o_to[q]) and (
	                                                                            i_to_j == p_to[q]):
	                                                                    q_to = g[q]
	                                                                    count9 += 1
	                                                                    for r in range(q + 1, newsize + 10):
	                                                                        if (i_to_j == i_to[r]) and (
	                                                                                    i_to_j == j_to[r]) and (
	                                                                                    i_to_j == k_to[r]) and (
	                                                                                    i_to_j == l_to[r]) and (
	                                                                                    i_to_j == m_to[r]) and (
	                                                                                    i_to_j == n_to[r]) and (
	                                                                                    i_to_j == o_to[r]) and (
	                                                                                    i_to_j == p_to[r]) and (
	                                                                                    i_to_j == q_to[r]):
	                                                                            count10 += 1
	                                                                            ten_cliques.append(
	                                                                                [i_to_j, i, j, k, l, m, n, o, p, q, r])
	    return count5, count6, count7, count8, count9, count10, ten_cliques

	def is_counter_example(self, g, gsize):  # returns True if contains 10-Clique, along with the current number of 5 cliques                                                                                                                                                                                                                                                                                             
		sgsize = 10                                                                                                                                                                                                                                                                                                                                                                                                 
		count = 0                                                                                                                                                                                                                                                                                                                                                                                                   
		for i in range(gsize-sgsize+1):                                                                                                                                                                                                                                                                                                                                                                             
			for j in range(i+1,gsize-sgsize+2):                                                                                                                                                                                                                                                                                                                                                                     
				for k in range(j+1,gsize-sgsize+3):                                                                                                                                                                                                                                                                                                                                                                 
					if(g[i*gsize+j] == g[i*gsize+k]) and (g[i*gsize+j] == g[j*gsize+k]):                                                                                                                                                                                                                                                                                                                            
						for l in range(k+1,gsize-sgsize+4):                                                                                                                                                                                                                                                                                                                                                         
							if (g[i * gsize + j] == g[i * gsize + l]) and (g[i * gsize + j] == g[j * gsize + l]) and (g[i * gsize + j] == g[k * gsize + l]):                                                                                                                                                                                                                                                        
								for m in range(l+1,gsize-sgsize+5):                                                                                                                                                                                                                                                                                                                                                 
									if (g[i * gsize + j] == g[i * gsize + m]) and (g[i * gsize + j] == g[j * gsize + m]) and (g[i * gsize + j] == g[k * gsize + m]) and (g[i * gsize + j] == g[l * gsize + m]):                                                                                                                                                                                                     
										count += 1                                                                                                                                                                                                                                                                                                                                                                  
										for n in range(m+1,gsize-sgsize+6):                                                                                                                                                                                                                                                                                                                                         
											if(g[i * gsize + j] == g[i * gsize + n]) and (g[i * gsize + j] == g[j * gsize + n]) and (g[i * gsize + j] == g[k * gsize + n]) and (g[i * gsize + j] == g[l * gsize + n]) and (g[i * gsize + j] == g[m * gsize + n]):                                                                                                                                                   
												for o in range(n+1,gsize-sgsize+7):                                                                                                                                                                                                                                                                                                                                 
													if (g[i*gsize+j] == g[i*gsize+o]) and (g[i*gsize+j] == g[j*gsize+o]) and (g[i*gsize+j] == g[k*gsize+o]) and (g[i*gsize+j] == g[l*gsize+o]) and (g[i*gsize+j] == g[m*gsize+o]) and (g[i*gsize+j] == g[n*gsize+o]):                                                                                                                                               
														for p in range(o+1,gsize-sgsize+8):                                                                                                                                                                                                                                                                                                                         
															if(g[i * gsize + j] == g[i * gsize + p]) and (g[i * gsize + j] == g[j * gsize + p]) and (g[i * gsize + j] == g[k * gsize + p]) and (g[i * gsize + j] == g[l * gsize + p]) and (g[i * gsize + j] == g[m * gsize + p]) and (g[i * gsize + j] == g[n * gsize + p]) and (g[i * gsize + j] == g[o * gsize + p]):                                             
																for q in range(p+1,gsize-sgsize+9):                                                                                                                                                                                                                                                                                                                 
																	if (g[i*gsize+j] == g[i*gsize+q]) and (g[i*gsize+j] == g[j*gsize+q]) and (g[i*gsize+j] == g[k*gsize+q]) and (g[i*gsize+j] == g[l*gsize+q]) and (g[i*gsize+j] == g[m*gsize+q]) and (g[i*gsize+j] == g[n*gsize+q]) and (g[i*gsize+j] == g[o*gsize+q]) and (g[i*gsize+j] == g[p*gsize+q]):                                                         
																		for r in range(q+1,gsize-sgsize+10):                                                                                                                                                                                                                                                                                                        
																			if (g[i*gsize+j] == g[i*gsize+r]) and (g[i*gsize+j] == g[j*gsize+r]) and (g[i*gsize+j] == g[k*gsize+r]) and (g[i*gsize+j] == g[l*gsize+r]) and (g[i*gsize+j] == g[m*gsize+r]) and (g[i*gsize+j] == g[n*gsize+r]) and (g[i*gsize+j] == g[o*gsize+r]) and (g[i*gsize+j] == g[p*gsize+r]) and (g[i*gsize+j] == g[q*gsize+r]):                                                                                                                                                                                                                                                                                                                
																				return False,count
		return True,count

	def edge_counter(self, matrix): #returns an array with the number of "red" edges for each node
	    dim = len(matrix[0])
	    edgearray = [0] * dim
	    for i in range(dim):
	        for j in range(dim):
	            if matrix[i][j] == 1:
	                edgearray[i] += 1
	    return edgearray

	def is_counter_example_c(self, g, gsize):
		count = call(["./a.out", str(gsize),"".join(str(x) for x in g)])
		if count == 0:
			return True, count
		else:
			return False, count

	def clique_counter_c(self, g):
		gsize = len(g[0])
		matrix_array = self.matrix_manager.matrix_to_array(g)
		cmd = ["./a.out", str(gsize),"".join(str(x) for x in matrix_array)]

		result = Popen(cmd, stdout=PIPE)
		out = result.stdout.read()
		ten_cliques = []
		counts = []
		for line in out.split("\n"):
			if ":" not in line:
				ten_cliques.append(list())
				for char in line.split(","):
					ten_cliques[-1].append(int(char))
			else:
				row = line[1:].split(",")
				for char in row:
					counts.append(int(char))
		return counts[0], counts[1], counts[2], counts[3], counts[4], counts[5], ten_cliques


