

class MatrixIterator:


	def __init__(self):
		pass

	def clique_counter(self, g, gsize):
	    sgsize = 10
	    count5 = 0
	    count6 = 0
	    count7 = 0
	    count8 = 0
	    count9 = 0
	    count10 = 0
	    sgsize = 10
	    nine_clique_double_array = []
	    ten_clique_double_array = []
	    for i in range(gsize-sgsize+1):
	        for j in range(i+1,gsize-sgsize+2):
	            for k in range(j+1,gsize-sgsize+3):
	                if(g[i*gsize+j] == g[i*gsize+k]) and (g[i*gsize+j] == g[j*gsize+k]):
	                    for l in range(k+1,gsize-sgsize+4):
	                        if (g[i * gsize + j] == g[i * gsize + l]) and (g[i * gsize + j] == g[j * gsize + l]) and (g[i * gsize + j] == g[k * gsize + l]):
	                            for m in range(l+1,gsize-sgsize+5):
	                                if (g[i * gsize + j] == g[i * gsize + m]) and (g[i * gsize + j] == g[j * gsize + m]) and (g[i * gsize + j] == g[k * gsize + m]) and (g[i * gsize + j] == g[l * gsize + m]):
	                                    count5+=1
	                                    for n in range(m+1,gsize-sgsize+6):
	                                        if(g[i * gsize + j] == g[i * gsize + n]) and (g[i * gsize + j] == g[j * gsize + n]) and (g[i * gsize + j] == g[k * gsize + n]) and (g[i * gsize + j] == g[l * gsize + n]) and (g[i * gsize + j] == g[m * gsize + n]):
	                                            count6 += 1
	                                            for o in range(n+1,gsize-sgsize+7):
	                                                if (g[i*gsize+j] == g[i*gsize+o]) and (g[i*gsize+j] == g[j*gsize+o]) and (g[i*gsize+j] == g[k*gsize+o]) and (g[i*gsize+j] == g[l*gsize+o]) and (g[i*gsize+j] == g[m*gsize+o]) and (g[i*gsize+j] == g[n*gsize+o]):
	                                                    count7 += 1
	                                                    for p in range(o+1,gsize-sgsize+8):
	                                                        if(g[i * gsize + j] == g[i * gsize + p]) and (g[i * gsize + j] == g[j * gsize + p]) and (g[i * gsize + j] == g[k * gsize + p]) and (g[i * gsize + j] == g[l * gsize + p]) and (g[i * gsize + j] == g[m * gsize + p]) and (g[i * gsize + j] == g[n * gsize + p]) and (g[i * gsize + j] == g[o * gsize + p]):
	                                                            count8 += 1
	                                                            for q in range(p+1,gsize-sgsize+9):
	                                                                if (g[i*gsize+j] == g[i*gsize+q]) and (g[i*gsize+j] == g[j*gsize+q]) and (g[i*gsize+j] == g[k*gsize+q]) and (g[i*gsize+j] == g[l*gsize+q]) and (g[i*gsize+j] == g[m*gsize+q]) and (g[i*gsize+j] == g[n*gsize+q]) and (g[i*gsize+j] == g[o*gsize+q]) and (g[i*gsize+j] == g[p*gsize+q]):
	                                                                    count9 += 1
	                                                                    temp_color = g[i*gsize+j]

	                                                                    for r in range(q+1,gsize-sgsize+10):
	                                                                        if (g[i*gsize+j] == g[i*gsize+r]) and (g[i*gsize+j] == g[j*gsize+r]) and (g[i*gsize+j] == g[k*gsize+r]) and (g[i*gsize+j] == g[l*gsize+r]) and (g[i*gsize+j] == g[m*gsize+r]) and (g[i*gsize+j] == g[n*gsize+r]) and (g[i*gsize+j] == g[o*gsize+r]) and (g[i*gsize+j] == g[p*gsize+r]) and (g[i*gsize+j] == g[q*gsize+r]):
	                                                                            count10 += 1
	                                                                            color = g[i * gsize + j]
	                                                                            ten_clique_double_array.append([color,i,j,k,l,m,n,o,p,q,r]) 
	    return count5, count6, count7, count8, count9, count10, ten_clique_double_array

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



