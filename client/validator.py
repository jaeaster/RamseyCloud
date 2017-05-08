#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import sys

def make_matrix(dimension):  ## Creates and returns a matrix with zeroes of size "dimension"
    return [[0 for col in range(dimension)] for row in range(dimension)]

def read_matrix_from_file(filename, dimension):  #Reads a matrix from file
    path = filename
    matrix = make_matrix(dimension)
    lineattributes = [0] * dimension
    with open(path, "r") as read_file:
        for i in range(dimension):
            line = read_file.readline().replace("\n", "")
            for j in range(len(line)):
                lineattributes[j] = line[j]
            for j in range(dimension):
                matrix[i][j] = int(lineattributes[j])
    return matrix

def matrix_to_array(matrix):#Converts a matrix to a one dimensional array
    dim = len(matrix[0])
    out_array = [0] * (dim ** 2)
    for i in range(dim):
        for j in range(dim):
            out_array[i * dim + j] = matrix[i][j]
    return out_array

def is_counter_example(g, gsize):  # returns True if contains 10-Clique, along with the current number of 5 cliques
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

def main():
  filename = sys.argv[1]
  dimension = int(sys.argv[2])
  matrix = read_matrix_from_file(filename, dimension)
  array = matrix_to_array(matrix)
  valid, counter = is_counter_example(array, dimension)
  if(valid):
    print("IS VALID with %d 5-cliques!!\n", counter)
  else:
    print("NOT VALID with %d 5-cliques!!\n", counter)

if __name__ == "__main__":
    main()