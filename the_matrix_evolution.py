import os
from random import randint
from socket import *
import collections
import random
import operator


m = {
    "SUCCESS": "0",
    "ACK": "1",
    "STATE_QUERY": "2",
    "IMPROVEMENT": "3"
}

###############################
#    Final Static Variables   #
###############################

MAX_RECV_LINE = 2048
TIMEOUT = 2
NETWORK_DOWN = False
PATH_STRING_SOLUTION = os.getcwd()+'/textfiles/'
PATH_STRING_IMPROVEMENTS = os.getcwd() + '/improvements/'


THRESHOLD_1 = 5
THRESHOLD_2 = 15
THRESHOLD_3 = 50
GREEDY_THRESHOLD = 1
GREEDY_DOUBLE_THRESHOLD = 3
GREEDY_MAX_THRESHOLD = 10
THOUSAND = 1000
MILLION = 1000000
INF = 100000000000
WIDE_PERCENTAGE_THRESHOLD = 0.15
TIGHT_PERCENTAGE_THRESHOLD = 0.1
STATISTICS_FILENAME = "clique_distribution.txt"

HASHTAGS = "#######################"
IMPROVEMENT = "IMPROVEMENT"


###############################
#        Visualization        # 
###############################

def matrix_print(matrix):  # Prints the matrix, not feasible for sizes bigger than ish 20
    delimitter = " | "
    line = delimitter
    for i in range(len(matrix[0])):
        for j in range(len(matrix[0])):
            line += str(matrix[i][j]) + delimitter
        print(delimitter + str(i) + "- " + line + "\n")
        line = delimitter

def print_dictionary(dictionary):
    for key in dictionary:
        print "%d: %s" %(key, str(dictionary[key]))

def print_tupled_dictionary(dictionary):
    for key in dictionary:
        print "Node: %d, count: %d" %(key[0], key[1])

def print_nodes(blue_counter_dict, red_counter_dict):
    sorted_blue = sorted(blue_counter_dict.items(), key=operator.itemgetter(1))   
    sorted_red = sorted(red_counter_dict.items(), key=operator.itemgetter(1))
    sorted_blue.reverse()
    sorted_red.reverse()   
    print "\nBlue"
    print_tupled_dictionary(sorted_blue)
    print "\nRed"
    print_tupled_dictionary(sorted_red)
    print "\n"

def print_hollywood_sign(dim):
    print "\n"
    print HASHTAGS
    print("#    Working on %d   #") %(dim)
    print HASHTAGS
    print "\n"

def print_temperary_lowest_10_clique_count(current_state):
    print("%d. lowest 10-clique count: %d") %(current_state[8], current_state[1])# legg til antall bla og rode noder

#####################################
#     Trivial Matrix Operations     #
#####################################

def make_matrix(dimension):  #ln Creates and returns a matrix with zeroes of size "dimension"
    return [[0 for col in range(dimension)] for row in range(dimension)]

def expand_matrix(matrix):# Expands the matrix with one additional node, with randomly colored edges
    prev_size = len(matrix[0])
    new_matrix = make_matrix(prev_size + 1)
    for i in range(prev_size):
        for j in range(prev_size):
            new_matrix[i][j] = matrix[i][j]

    for k in range(prev_size):
        a = randint(0, 1)
        new_matrix[prev_size][k] = a
        new_matrix[k][prev_size] = a
    return new_matrix

def matrix_to_array(matrix):#Converts a matrix to a one dimensional array
    dim = len(matrix[0])
    out_array = [0] * (dim ** 2)
    for i in range(dim):
        for j in range(dim):
            out_array[i * dim + j] = matrix[i][j]
    return out_array

def flip_one_bit(matrix, x, y):
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

def bit_flipper(matrix):  # flips random place in the matrix
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


def bit_flipper_edge(matrix):  # flips random bit on the edge of the matrix
    a = len(matrix[0])
    b = randint(0, a - 1)
    if matrix[b][a - 1] == 0:
        matrix[a - 1][b] = 1
        matrix[b][a - 1] = 1
    else:
        matrix[a - 1][b] = 0
        matrix[b][a - 1] = 0
    return matrix


def re_shuffle_edge(matrix): #reshuffles the edges in the new expanded layer
    size = len(matrix[0])
    for i in range(size - 1):
        a = randint(0, 1)
        matrix[size - 1][i] = a
        matrix[i][size - 1] = a
    return matrix

############################
#       File Handling      #
############################

def filenamestring(size):#Returns the filename of the counter example of size "size"
    return str("ramsey-" + str(size) + ".txt")

def highest_ramsey_dir(): #Searches for and returns the filename of the highest counter example in your directory
    highest = 0
    for fil in os.listdir(PATH_STRING_SOLUTION):
        if fil.startswith("ramsey-"):
            a = str(fil)
            a = a[7:-4]
            if int(a) > highest:
                highest = int(a)
    return filenamestring(highest)

def write_matrix_to_file(matrix, directory, filename):
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

def read_highest_from_file(): #Return highest available matrix
    filename = highest_ramsey_dir()
    dim = int(filename.replace("ramsey-", "").replace(".txt", ""))
    return read_matrix_from_file(filename, dim)

def read_matrix_from_file(filename, dimension):  #Reads a matrix from file
    path = PATH_STRING_SOLUTION + filename
    delimitter = "-"
    matrix = make_matrix(dimension)
    lineattributes = [0] * dimension
    with open(path, "r") as read_file:
        for i in range(dimension):
            line = read_file.readline().replace("\n", "").replace(delimitter, "")
            for j in range(len(line)):
                lineattributes[j] = line[j]
            for j in range(dimension):
                matrix[i][j] = int(lineattributes[j])
    return matrix

def append_to_file(string_to_write,file_name):
    path = PATH_STRING_SOLUTION + file_name
    f = open(path, 'a')
    f.write(string_to_write)
    f.close()

def generate_string_to_append(values):
    string = ''
    delimitter = "|"
    for elem in values:
        temp_string = "%d%s" %(elem, delimitter)
        string += temp_string
    return string

def generate_solution_filename(matrix):
    dim = len(matrix[0])
    filename = filenamestring(dim)
    for fil in os.listdir(PATH_STRING_SOLUTION):
        if fil.endswith(filename):
            return
    delimitter = "-"
    return filename

###################################
#       Statistical Methods       # 
###################################

def clique_counter(g, gsize):
    sgsize = 10
    count5 = 0
    count6 = 0
    count7 = 0
    count8 = 0
    count9 = 0
    count10 = 0
    sgsize = 10
    double_array = []
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
                                                                    for r in range(q+1,gsize-sgsize+10):
                                                                        if (g[i*gsize+j] == g[i*gsize+r]) and (g[i*gsize+j] == g[j*gsize+r]) and (g[i*gsize+j] == g[k*gsize+r]) and (g[i*gsize+j] == g[l*gsize+r]) and (g[i*gsize+j] == g[m*gsize+r]) and (g[i*gsize+j] == g[n*gsize+r]) and (g[i*gsize+j] == g[o*gsize+r]) and (g[i*gsize+j] == g[p*gsize+r]) and (g[i*gsize+j] == g[q*gsize+r]):
                                                                            count10 += 1
                                                                            color = g[i * gsize + j]
                                                                            double_array.append([color,i,j,k,l,m,n,o,p,q,r]) 

    return count5, count6, count7, count8, count9, count10, double_array

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

def edge_counter(matrix): #returns an array with the number of "red" edges for each node
    dim = len(matrix[0])
    edgearray = [0] * dim
    for i in range(dim):
        for j in range(dim):
            if matrix[i][j] == 1:
                edgearray[i] += 1
    return edgearray


################################
#        Boolean Helpers       # 
################################

def exists_higher_counter_example(current):  # Returns True if the input number is lower than highest available
    currentfile = highest_ramsey_dir()
    if int(currentfile[7:-4]) >= current:
        return True

def is_worth_checking(clique_count_five, dim):
    orange_threshold = 5000*dim
    #return clique_count_five > orange_threshold
    return True

def is_empty_dictionary(dictionary):
    return not bool(dictionary)

def is_in_dictionary(dictionary, test_key):
    for key in dictionary:
        if test_key == key:
            return True
    return False


#################################
#       Complements Main()      # 
#################################

def probe_better_solution(current_matrix):
    if NETWORK_DOWN:
        dim = len(current_matrix[0])
        if exists_higher_counter_example(dim):
            current_matrix = expand_matrix(read_highest_from_file())
            new_dim = dim+1
            print("Found better matrix from other program, now working on %d") %(new_dim)
    else:
        new_matrix = recv_matrix(server_socket, 0)
        if new_matrix:
            current_matrix = expand_matrix(new_matrix)
            dim = len(current_matrix[0])
            print ("Received better matrix from server, now working on %d") %dim
    return current_matrix

def fetch_and_expand_matrix():
    if NETWORK_DOWN:
        current_matrix = expand_matrix(read_highest_from_file())
    else:
        current_matrix = expand_matrix(query_server_for_highest())
    return current_matrix


##############################
#           Main()           # 
##############################

def main1():

    current_matrix = fetch_and_expand_matrix()
    while True:
        dim = len(current_matrix[0])
        print_hollywood_sign(dim)
        current_matrix, is_ce, blue_clique_count, red_clique_count = smart_reduction(current_matrix)
        print("bluecount = "+ str(blue_clique_count) + "     red count = "+ str(red_clique_count))
        if is_ce:
            current_matrix = process_new_counter_example(current_matrix)
        current_matrix = probe_better_solution(current_matrix)

def main2():
    current_matrix = fetch_and_expand_matrix()
    while True:
        dim = len(current_matrix[0])
        print_hollywood_sign(dim)
        current_matrix, is_ce,  = iterative_reduce(current_matrix, 5)
        if is_ce:
            current_matrix = process_new_counter_example(current_matrix)
        current_matrix = probe_better_solution(current_matrix)


        #current_matrix, current_state = handle_state_cases(current_matrix, temp_matrix, current_state)

##############################
#           Other            # 
##############################

def validation(start, stopp):                                                                
    for i in range(start, stopp + 1):                                                        
        matrise = matrix_to_array(read_matrix_from_file(filenamestring(i), i))                
        print(filenamestring(i) + "   " + str(i))                                            
        counter_ex,count  = is_counter_example(matrise, i)                                    
        if counter_ex is False:                                                              
            print(" Matrix " + str(i) + " is not a counter example")                          
            print("count "+ str(count))                                                      
        else:                                                                                
            print("count "+ str(count))                                                      
            print(str(i) + "  OK")

def save_clicke_distribution(blue_sorted, red_sorted, blue_count, red_count):
    string = ''
    string += '0|%d' %blue_count
    for key in blue_sorted:
        key_value_pair = '%d:%d|'%(key[0], key[1])
        string += key_value_pair
    string += '1|%d' %red_count
    for key in sorted_red:
        key_value_pair = '%d:%d|'%(key[0], key[1])
        string += key_value_pair
    #edge_add_on = "%d:%d$"%(edge_x,edge_y)
    #string += edge_add_on
    return string

def save_edge_pick(string, egde_x, edge_y):
    edge_add_on = '%d:%d$'%(edge_x, edge_y)
    new_string += string
    return new_string      


################################
#        Ben Zhao Methods      # 
################################
def process_new_counter_example(matrix):
    #print("Counterexample found of size %d") %(current_state[0])
    #print ("Number of cycles in total = %d") %(current_state[8])
    if NETWORK_DOWN:
        write_matrix_to_file(matrix, PATH_STRING_SOLUTION, generate_solution_filename(matrix))
    else:
        matrix = send_matrix_to_server(matrix, m["SUCCESS"])
    new_matrix = expand_matrix(matrix)
    #update_current_state(current_state, [0,1,3] , [current_state[0]+1, THOUSAND, MILLION])
    return new_matrix#, current_state

def send_matrix_to_server(matrix, message_type, num_cliques=0):
    dim = len(matrix[0])
    line = ""
    for i in range(dim):
        for j in range(dim):
            line += str(matrix[i][j])
        line += "\n"
    if message_type == "SUCCESS":
        msg = "{0}\n{1}\n{2}END\n".format(m[message_type], dim, line)
    elif message_type == "IMPROVEMENT":
        msg = "{0}\n{1}\n{2}\n{3}END\n".format(m[message_type], num_cliques, dim, line)
    server_socket.send(str.encode(msg))
    ret_matrix = recv_matrix(server_socket)
    if ret_matrix:
        return ret_matrix
    else:
        return matrix

def recv_matrix(conn, timeout=TIMEOUT):
    resp = recv_payload(conn, timeout).split("\n", 2)
    if len(resp) < 3:
        return False
    message_type, n, new_matrix = resp[0], int(resp[1]), resp[2]
    if message_type == m["ACK"]:
        ret_matrix = make_matrix(n)
        new_matrix = new_matrix.split("\n")
        for i, line in enumerate(new_matrix):
            for j, entry in enumerate(line):
                ret_matrix[i][j] = int(entry)
        return ret_matrix
    else:
        return False

def recv_payload(conn, timeout=TIMEOUT):
    payload = ""
    conn.settimeout(timeout)
    while (1):
        try:
            partial_load = conn.recv(MAX_RECV_LINE)
            partial_load = bytes.decode(partial_load)
            if not partial_load:
                return payload
            else:
                payload += partial_load
                if "END" in partial_load:
                    return payload[:-4]
        except:
            return payload

def query_server_for_highest():
    msg = "{0}\nEND\n".format(m["STATE_QUERY"])
    server_socket.send(str.encode(msg))
    ret_matrix = recv_matrix(server_socket)
    return ret_matrix
# Network functions end here

serverPort = 57339
serverName = "128.111.43.14"
if not NETWORK_DOWN:
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.connect((serverName, serverPort))


################################
#       Under Construction     # 
################################


#Swaps the edge participating in most cliques until nodes only participate in "threshold" amounts of cliques, and returns the matrix
def greedy_reduction(matrix): 
    c5,c6,c7,c8,c9,c10,ten_clique_double_array = clique_counter(matrix_to_array(matrix), len(matrix[0]))
    if c10 ==0:
        print "Found counter example"
        return matrix, True, 0, 0
    else:
        blue_counter_dict, red_counter_dict = participation_count(ten_clique_double_array)
        blue_clique_count, red_clique_count = count_number_of_cliques(ten_clique_double_array)
        color_to_optimize = choose_color_to_optimize(ten_clique_double_array)
        sorted_blue, sorted_red = generate_sorted_dictionary_from_double_array(ten_clique_double_array)
        x, y = choose_nodes_to_flip_greedy(color_to_optimize, sorted_blue, sorted_red)      
        print "\nChose to flip %d and %d" %(x,y)
        flipped_matrix = flip_one_bit(matrix, x, y)
        return flipped_matrix, False, blue_clique_count, red_clique_count


def smart_reduction(matrix):
    c5,c6,c7,c8,c9,c10,ten_clique_double_array = clique_counter(matrix_to_array(matrix), len(matrix[0]))
    print_double_array(ten_clique_double_array)
    if c10 ==0:
        print "Found counter example"
        return matrix, True, 0, 0
    else:
        blue_clique_count, red_clique_count = count_number_of_cliques(ten_clique_double_array)
        flipped_matrix = matrix
        smart_cover_set = find_cover_set(ten_clique_double_array)
        string = "chose to flip "
        for elem in smart_cover_set:
            string += str(elem)
            x = elem[0]
            y = elem[1]
            flipped_matrix = flip_one_bit(flipped_matrix, x, y)

        return flipped_matrix, False, blue_clique_count, red_clique_count

def print_double_array(double_array):
    for elem in double_array:
        print elem
        print "\n"





#Swaps the edge participating in most cliques until nodes only participate in "threshold" amoints of cliques, and returns the matrix
def greedy_reduction_double(matrix, state):
    current_matrix = matrix
    current_state = state
    continue_loop = True
    while continue_loop:
        print "Double Greed"
        c5,c6,c7,c8,c9,c10,ten_clique_double_array = clique_counter(matrix_to_array(current_matrix), current_state[0])
        blue_counter_dict, red_counter_dict = participation_count(ten_clique_double_array)
        print is_empty_dictionary(blue_counter_dict)
        if is_empty_dictionary(blue_counter_dict) or is_empty_dictionary(red_counter_dict):
            continue_loop = False
            continue
        x, y = choose_nodes_to_flip_greedy(0, blue_counter_dict, red_counter_dict)
        w, z = choose_nodes_to_flip_greedy(1, blue_counter_dict, red_counter_dict)
        print "Chose to flip Blue: %d and %d\n" %(x,y)
        print "Chose to flip Red: %d and %d\n" %(w,z)
        current_matrix = flip_one_bit(current_matrix, x,y)
        current_matrix = flip_one_bit(current_matrix, w,z)
        continue_loop = continue_greedy_while_loop(blue_counter_dict, red_counter_dict, GREEDY_DOUBLE_THRESHOLD)
    return current_matrix


####################################
#   Complements Greedy Methods     # 
####################################

#Array Argument
def choose_color_to_optimize(double_array): #Choses the color that creates the most cliques
    blue_counter = 0
    red_counter = 0
    for elem in double_array:
        if elem[0] == 0:
            blue_counter += 1
        else:
            red_counter += 1
    if blue_counter > red_counter:
        return 0
    else:
        return 1

#returns two dictionar, one for each color, containing nodes that participate in cliques and the number of cliques they paricipate in
def participation_count(double_array):
    blue_counter_dict = {}
    red_counter_dict = {}
    for elem in double_array:
        color = elem[0]
        if color == 0:
            for i in range(1, len(elem)):
                temp_key = elem[i]
                if not is_in_dictionary(blue_counter_dict, temp_key):
                    blue_counter_dict[temp_key] = 1
                else:
                    blue_counter_dict[temp_key] += 1
        else:
            for i in range(1, len(elem)):
                temp_key = elem[i]
                if not is_in_dictionary(red_counter_dict, temp_key):
                    red_counter_dict[temp_key] = 1
                else:
                    red_counter_dict[temp_key] += 1
    return blue_counter_dict, red_counter_dict

def count_number_of_cliques(double_array):
    blue_count = 0
    red_count = 0
    for elem in double_array:
        if elem[0] == 0:
            blue_count += 1
        else: red_count += 1
    return blue_count, red_count

def generate_sorted_dictionary_from_double_array(double_array):
    blue_counter_dict, red_counter_dict = participation_count(double_array)
    sorted_blue = sort_dictionary(blue_counter_dict)
    sorted_red = sort_dictionary(red_counter_dict)
    return sorted_blue, sorted_red

#Dictionary Argument
#Returns the edge participating in most cliques
def choose_nodes_to_flip_greedy(color_to_optimize, sorted_blue, sorted_red):
    print "BLUE"
    print_tupled_dictionary(sorted_blue)
    print "\nRED"
    print_tupled_dictionary(sorted_red)
    if color_to_optimize == 0:
            return sorted_blue[0][0], sorted_blue[1][0]
    else:
        return sorted_red[0][0], sorted_red[1][0]

def sort_dictionary(dictionary):
    sorted_dictionary = sorted(dictionary.items(), key=operator.itemgetter(1))
    sorted_dictionary.reverse()
    return sorted_dictionary

def find_cover_set(double_array):
    number_of_cliques = len(double_array)
    clique_set_length = len(double_array[0])
    #print(number_of_cliques)
    #print(double_array)
    setlist =[]
    for i in range(number_of_cliques):
        for j in range(1,clique_set_length+1):
            for k in range(j+1,clique_set_length):
                a = double_array[i][j]
                b = double_array[i][k]
                d = []
                d.append(a)
                d.append(b)
                for l in range(number_of_cliques):#
                    if (a in double_array[l]) and (b in double_array[l]):
                        d.append(l)
                setlist.append(d)
    setlist_sorted = sorted(setlist,key=len,reverse=True)
    coverset_tuples = []
    coverset_cliques =[]
    add_to_cover = False
    for tu in range(len(setlist_sorted)):
        for elem in setlist_sorted[tu][2:]:
            if elem not in coverset_cliques:
                add_to_cover = True
                coverset_cliques.append(elem)
        if add_to_cover:
            coverset_tuples.append(setlist_sorted[tu][:2])
        add_to_cover = False
        if len(coverset_cliques) == number_of_cliques:
            print(coverset_tuples)
            #print(coverset_cliques)
            return coverset_tuples



################################
#      Iterative Reduction     # 
################################

#Swaps the "cover"-edge from the first k ten-cliques
def iterative_reduce(matrix, w):
    double_array = find_w_first_ten_cliques(matrix_to_array(matrix), len(matrix[0]) ,w)
    if double_array:
        #cover_set = find_cover_set(double_array)
        #node_one, node_two = pick_edge_to_flip(cover_set)
        color_to_optimize = choose_color_to_optimize(double_array)
        blue_counter_dict, red_counter_dict = participation_count(double_array)
        x, y = choose_nodes_to_flip_greedy(color_to_optimize, blue_counter_dict, red_counter_dict)
        matrix = flip_one_bit(matrix,x,y)
        return matrix, False
    else:
        return matrix, True
    return matrix

#Finds the first k ten-cliques
def find_w_first_ten_cliques(g, gsize, w):  # returns True if contains 10-Clique, along with the current number of 5 cliques
    print "Finding first %d ten cliques " %w
    sgsize = 10
    count = 0
    double_array = []
    ten_clique_count = 0
    for i in range(gsize-sgsize+1):
        for j in range(i+1,gsize-sgsize+2):
            for k in range(j+1,gsize-sgsize+3):
                if(g[i*gsize+j] == g[i*gsize+k]) and (g[i*gsize+j] == g[j*gsize+k]):
                    for l in range(k+1,gsize-sgsize+4):
                        if (g[i * gsize + j] == g[i * gsize + l]) and (g[i * gsize + j] == g[j * gsize + l]) and (g[i * gsize + j] == g[k * gsize + l]):
                            for m in range(l+1,gsize-sgsize+5):
                                if (g[i * gsize + j] == g[i * gsize + m]) and (g[i * gsize + j] == g[j * gsize + m]) and (g[i * gsize + j] == g[k * gsize + m]) and (g[i * gsize + j] == g[l * gsize + m]):
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
                                                                            ten_clique_count += 1
                                                                            color = g[i*gsize+j]
                                                                            double_array.append([color,i,j,k,l,m,n,o,p,q,r])
                                                                            if ten_clique_count == w: 
                                                                                return double_array
    return double_array

#picks a random egde from a cover set
def pick_random_edge_to_flip(cover_set):
    random_index = random.randint(0, len(cover_set))
    random_edge = cover_set[random_index]
    return random_edge[0], random_edge[1]



#find_cover_set([[1,2,3,4,5,6,7,8,9,10],[2,3,7,10,12,11,13,14,20,30],[3,6,9,12,15,18,21,24,27,30]])
main1()
#validation(90, 100)



