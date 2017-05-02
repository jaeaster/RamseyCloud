import os
from random import randint

from socket import *


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
NETWORK_DOWN = True
PATH_STRING = os.getcwd()+'/textfiles/'

THRESHOLD_1 = 5
THRESHOLD_2 = 15
THRESHOLD_3 = 50
THOUSAND = 1000
MILLION = 1000000
INF = 100000000000

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


def matrix_adjustment(matrix, algorithm):# applies algorithm to matrix
    return algorithm(matrix)


############################
#       File Handling       #
############################

def filenamestring(size):#Returns the filename of the counter example of size "size"
    return str("ramsey-" + str(size) + ".txt")

def highest_ramsey_dir(): #Searches for and returns the filename of the highest counter example in your directory
    highest = 0
    for fil in os.listdir(PATH_STRING):
        if fil.startswith("ramsey-"):
            a = str(fil)
            a = a[7:-4]
            if int(a) > highest:
                highest = int(a)
    return filenamestring(highest)

def write_matrix_to_file(matrix):  # write to file
    size = len(matrix[0])
    filename = filenamestring(size)
    for fil in os.listdir(PATH_STRING):
        if fil.endswith(filename):
            return
    delimitter = "-"
    path = PATH_STRING + filename
    dim = len(matrix[0])
    line = ""
    with open(path, "w") as out:
        for i in range(dim):
            for j in range(dim):
                line += str(matrix[i][j])  # mulig denne ma byttes om
            out.write(line.replace("\n", "")[0:-1] + "\n")
            line = ""

def read_highest_from_file(): #Return highest available matrix
    filename = highest_ramsey_dir()
    dim = int(filename.replace("ramsey-", "").replace(".txt", ""))
    return read_matrix_from_file(filename, dim)

def read_matrix_from_file(filename, dimension):  #Reads a matrix from file
    path = PATH_STRING + filename
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

###################################
#       Statistical Methods       # 
###################################

def clique_counter(g, gsize):  # counts all number of cliques 5-10
    count5 = 0
    count6 = 0
    count7 = 0
    count8 = 0
    count9 = 0
    count10 = 0
    sgsize = 10
    for i in range(gsize - sgsize + 1):
        for j in range(i + 1, gsize - sgsize + 2):
            for k in range(j + 1, gsize - sgsize + 3):
                if (g[i * gsize + j] == g[i * gsize + k]) and (g[i * gsize + j] == g[j * gsize + k]):
                    for l in range(k + 1, gsize - sgsize + 4):
                        if (g[i * gsize + j] == g[i * gsize + l]) and (g[i * gsize + j] == g[j * gsize + l]) and (
                            g[i * gsize + j] == g[k * gsize + l]):
                            for m in range(l + 1, gsize - sgsize + 5):
                                if (g[i * gsize + j] == g[i * gsize + m]) and (
                                    g[i * gsize + j] == g[j * gsize + m]) and (
                                    g[i * gsize + j] == g[k * gsize + m]) and (g[i * gsize + j] == g[l * gsize + m]):
                                    count5 += 1
                                    for n in range(m + 1, gsize - sgsize + 6):
                                        if (g[i * gsize + j] == g[i * gsize + n]) and (
                                            g[i * gsize + j] == g[j * gsize + n]) and (
                                            g[i * gsize + j] == g[k * gsize + n]) and (
                                            g[i * gsize + j] == g[l * gsize + n]) and (
                                            g[i * gsize + j] == g[m * gsize + n]):
                                            count6 += 1
                                            for o in range(n + 1, gsize - sgsize + 7):
                                                if (g[i * gsize + j] == g[i * gsize + o]) and (
                                                    g[i * gsize + j] == g[j * gsize + o]) and (
                                                    g[i * gsize + j] == g[k * gsize + o]) and (
                                                    g[i * gsize + j] == g[l * gsize + o]) and (
                                                    g[i * gsize + j] == g[m * gsize + o]) and (
                                                    g[i * gsize + j] == g[n * gsize + o]):
                                                    count7 += 1
                                                    for p in range(o + 1, gsize - sgsize + 8):
                                                        if (g[i * gsize + j] == g[i * gsize + p]) and (
                                                            g[i * gsize + j] == g[j * gsize + p]) and (
                                                            g[i * gsize + j] == g[k * gsize + p]) and (
                                                            g[i * gsize + j] == g[l * gsize + p]) and (
                                                            g[i * gsize + j] == g[m * gsize + p]) and (
                                                            g[i * gsize + j] == g[n * gsize + p]) and (
                                                            g[i * gsize + j] == g[o * gsize + p]):
                                                            count8 += 1
                                                            for q in range(p + 1, gsize - sgsize + 9):
                                                                if (g[i * gsize + j] == g[i * gsize + q]) and (
                                                                    g[i * gsize + j] == g[j * gsize + q]) and (
                                                                    g[i * gsize + j] == g[k * gsize + q]) and (
                                                                    g[i * gsize + j] == g[l * gsize + q]) and (
                                                                    g[i * gsize + j] == g[m * gsize + q]) and (
                                                                    g[i * gsize + j] == g[n * gsize + q]) and (
                                                                    g[i * gsize + j] == g[o * gsize + q]) and (
                                                                    g[i * gsize + j] == g[p * gsize + q]):
                                                                    count9 += 1
                                                                    for r in range(q + 1, gsize - sgsize + 10):
                                                                        if (g[i * gsize + j] == g[i * gsize + r]) and (
                                                                            g[i * gsize + j] == g[j * gsize + r]) and (
                                                                            g[i * gsize + j] == g[k * gsize + r]) and (
                                                                            g[i * gsize + j] == g[l * gsize + r]) and (
                                                                            g[i * gsize + j] == g[m * gsize + r]) and (
                                                                            g[i * gsize + j] == g[n * gsize + r]) and (
                                                                            g[i * gsize + j] == g[o * gsize + r]) and (
                                                                            g[i * gsize + j] == g[p * gsize + r]) and (
                                                                            g[i * gsize + j] == g[q * gsize + r]):
                                                                            count10 += 1
    return count5, count6, count7, count8, count9, count10

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

def edge_counter(matrix): #returns an array with the number of "blue" edges for each node
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
    return clique_count_five > orange_threshold


######################################
#       Current State  Methods       # 
######################################

def initialize_current_state(matrix): #Current_state is a vector containing values representing the current state program in regards to the matrix being processed.
    #The vector:
    #[dimension, 10-cliques, 5-cliques, hcbc, total_count, current_count, state, while_counter]
    #[    0    ,     1    ,      3   ,   4 ,      5     ,        6     ,   7    ,       8     ]
    return [len(matrix[0]), INF, MILLION, 0, 0, 0, 0, 0, 0]

def update_current_state(current_state, index, value):
    if isinstance(index, list):
        return update_current_state_multiple(current_state, index, value)
    elif isinstance(index, int):
        return update_current_state_single(current_state, index, value)
    return False

def update_current_state_multiple(current_state, indices, values):
    if len(indices) != len(values):
            return False
    for i in range(len(indices)):
        current_state[indices[i]] = values[i]
    return True

def update_current_state_single(current_state, index, value):
    if index > len(current_state)-1:
        return False
    if not isinstance(value, int):
            return False
    current_state[index] = value
    return True


#################################
#       Complements Main()      # 
#################################

def choose_algorithm(current_state):# 10cliques,dimension, 5cliques,attempts,t1,t2,t3
    nr_of_ten_cliques = current_state[1]
    if nr_of_ten_cliques > THRESHOLD_3:
        return re_shuffle_edge
    elif THRESHOLD_2 <= nr_of_ten_cliques <= THRESHOLD_3:
        return bit_flipper_edge
    else:
        return bit_flipper

def analysis_of_matrix(matrix,current_state):
    dim = current_state[0]
    hit, five_clique_count = is_counter_example(matrix_to_array(matrix),dim)
    print ("   nr of 5 cliques before 1st 10 clique : %d\n")%(five_clique_count)
    if hit:
        update_current_state(current_state, 6,1)
    elif is_worth_checking(five_clique_count, dim):
        c5,c6,c7,c8,c9,c10 = clique_counter(matrix_to_array(matrix), dim)
        print ("5 -> %d, 6 -> %d, 7 -> %d, 8 -> %d, 9 -> %d, 10 -> %d ") %(c5,c6,c7,c8,c9,c10)
        if c10 < current_state[1]:
            update_current_state(current_state, [1,6, 8], [c10,2, current_state[8]+1])
    else:
        update_current_state(current_state, [6,8], [3,current_state[8]+1])
    return current_state

def handle_state_cases(current_matrix, temp_matrix, current_state):
    state_status = current_state[6]
    if state_status == 1:#Found Counter example
        current_matrix, current_state = process_new_counter_example(temp_matrix, current_state)
        return current_matrix, current_state
    elif state_status == 2:#Counter Example was not found, but a better matrix was discovered
        send_matrix_to_server(temp_matrix, IMPROVEMENT, current_state[1])
        print ("Switching to a better matrix with clique count: %s") %(current_state[1])
        return temp_matrix, current_state;
    elif state_status == 3: # A worse matrix was found
        return current_matrix, current_state

def probe_better_solution(current_matrix, current_state):
    if NETWORK_DOWN:
        if exists_higher_counter_example(current_state[0]):
            current_matrix = expand_matrix(read_highest_from_file())
            update_current_state(0, len(current_matrix[0]))
            print("Found better matrix from other program, now working on %d") %current_state[0]
    else:
        new_matrix = recv_matrix(server_socket, 0)
        if new_matrix:
            current_matrix = expand_matrix(new_matrix)
            update_current_state(0, len(current_matrix[0]))
            print ("Received better matrix from server, now working on %d") %current_state[0]
    return current_matrix, current_state

def fetch_matrix():
    if NETWORK_DOWN:
        current_matrix = expand_matrix(read_highest_from_file())
    else:
        current_matrix = expand_matrix(query_server_for_highest())
    return current_matrix


##############################
#           Main()           # 
##############################

def main():
    current_matrix = fetch_matrix()
    current_state = initialize_current_state(current_matrix)
    print_hollywood_sign(current_state)
    while True:
        print_temperary_lowest_10_clique_count(current_state)
        algorithm = choose_algorithm(current_state)
        temp_matrix = matrix_adjustment(current_matrix,algorithm)# adjusts the matrix
        current_state = analysis_of_matrix(temp_matrix, current_state)
        current_matrix, current_state = handle_state_cases(current_matrix, temp_matrix, current_state)
        current_matrix, current_state = probe_better_solution(current_matrix, current_state)


##############################
#           Other            # 
##############################

def validation(start, stopp):
    for i in range(start, stopp + 1):
        matrise = matrix_to_array(read_matrix_from_file(filenamestring(i), i))
        print("%s  %d")%(filenamestring(i), i)
        valid = is_counter_example(matrise, i)
        if valid is True:
            print("Matrix %d is not a counter example") %(i)
        else:
            print("%d  OK")%(i)

def print_hollywood_sign(current_state):
    print "\n"
    print HASHTAGS
    print("#    Working on %d   #") %(current_state[0])
    print HASHTAGS
    print "\n"

def print_temperary_lowest_10_clique_count(current_state):
    print("%d. lowest 10-clique count: %d") %(current_state[8], current_state[1])


################################
#        Ben Zao Methods       # 
################################
def process_new_counter_example(matrix, current_state):
    print("Counterexample found of size %d") %(current_state[0])
    print ("Number of cycles in total = %d") %(current_state[8])
    if NETWORK_DOWN:
        write_matrix_to_file(matrix)
    else:
        send_matrix_to_server(matrix, "SUCCESS")
    new_matrix = expand_matrix(matrix)
    update_current_state(current_state, [0,1,3] , [current_state[0]+1, THOUSAND, MILLION])
    return new_matrix, current_state


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
main()



