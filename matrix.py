import os
from random import randint
from socket import *

MAX_RECV_LINE = 2048
TIMEOUT = 2
PATH_STRING = "/Users/jdogg5566/go/src/github.com/easterandjay/cloud/counterexamples/"

m = {
  "SUCCESS": "0",
  "ACK": "1",
  "STATE_QUERY": "2"  
}

def make_matrix(dimension):## lager en matrise av storrelse dimension
    return [[0 for col in range(dimension)] for row in range(dimension)]

def makeplain10():
    write_matrix_to_file(make_matrix(10))

def matrix_print(matri): # Prints
    delimitter  = " | "
    linje = delimitter
    for i in range(len(matri[0])):
        for j in range(len(matri[0])):
            linje += str(matri[i][j]) + delimitter
        print(delimitter + str(i) + "- " + linje + "\n")
        linje = delimitter



def expand_matrix(matrix):
    prev_size = len(matrix[0])
    new_matrix = make_matrix(prev_size+1)
    for i in range(prev_size):
        for j in range(prev_size):
            new_matrix[i][j] = matrix[i][j]

    for k in range(prev_size):
        a = randint(0,1)
        new_matrix[prev_size][k] = a
        new_matrix[k][prev_size] = a
    return new_matrix

def two_to_one_dimensions(matrix):
    dim = len(matrix[0])
    out_array = [0]*(dim**2)
    for i in range(dim):
        for j in range(dim):
            out_array[i*dim +j] = matrix[i][j]
    return out_array

def bitflipper(matrix):
    dim = len(matrix[0])
    a = randint(0,dim-1)
    b = randint(0,dim-1)
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

def filenamestring(size):
    return str("ramsey-" + str(size) + ".txt")
def highest_ramsey_dir():
    highest = 0
    for fil in os.listdir(PATH_STRING):
        if fil.startswith("ramsey-"):
            a = str(fil)
            a = a[7:-4]
            if int(a) > highest:
                highest = int(a)
    return filenamestring(highest)

def change_to_higher(current):# burde kanskje
    currentfile = highest_ramsey_dir()
    #print("current dimension is "+ str(current) + "   highest in file is" + str(int(currentfile[7:-4])))
    if int(currentfile[7:-4]) >= current:
        return True

def write_matrix_to_file(matrix): # write to file
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
                line += str(matrix[i][j]) + delimitter # mulig denne ma byttes om
            out.write(line.replace("\n", "")[0:-1] + "\n")
            line = ""

def clique_count(g,gsize):# g is an array of all
    count = 0
    sgsize = 10
    for i in range(gsize-sgsize+1):
        for j in range(i+1,gsize-sgsize+2):
            for k in range(j+1,gsize-sgsize+3):
                if(g[i*gsize+j] == g[i*gsize+k]) and (g[i*gsize+j] == g[j*gsize+k]):
                    for l in range(k+1,gsize-sgsize+4):
                        if (g[i * gsize + j] == g[i * gsize + l]) and (g[i * gsize + j] == g[j * gsize + l]) and (g[i * gsize + j] == g[k * gsize + l]):
                            for m in range(l+1,gsize-sgsize+5):
                                if (g[i * gsize + j] == g[i * gsize + m]) and (g[i * gsize + j] == g[j * gsize + m]) and (g[i * gsize + j] == g[k * gsize + m]) and (g[i * gsize + j] == g[l * gsize + m]):
                                    if sgsize <= 5:
                                        count+=1
                                    else:
                                        for n in range(m+1,gsize-sgsize+6):
                                            if(g[i * gsize + j] == g[i * gsize + n]) and (g[i * gsize + j] == g[j * gsize + n]) and (g[i * gsize + j] == g[k * gsize + n]) and (g[i * gsize + j] == g[l * gsize + n]) and (g[i * gsize + j] == g[m * gsize + n]):
                                                if sgsize <= 6:
                                                    count+=1
                                                else:
                                                    for o in range(n+1,gsize-sgsize+7):
                                                        if (g[i*gsize+j] == g[i*gsize+o]) and (g[i*gsize+j] == g[j*gsize+o]) and (g[i*gsize+j] == g[k*gsize+o]) and (g[i*gsize+j] == g[l*gsize+o]) and (g[i*gsize+j] == g[m*gsize+o]) and (g[i*gsize+j] == g[n*gsize+o]):
                                                            if sgsize <= 7:
                                                                count +=1
                                                            else:
                                                                for p in range(o+1,gsize-sgsize+8):
                                                                    if(g[i * gsize + j] == g[i * gsize + p]) and (g[i * gsize + j] == g[j * gsize + p]) and (g[i * gsize + j] == g[k * gsize + p]) and (g[i * gsize + j] == g[l * gsize + p]) and (g[i * gsize + j] == g[m * gsize + p]) and (g[i * gsize + j] == g[n * gsize + p]) and (g[i * gsize + j] == g[o * gsize + p]):
                                                                        if sgsize <= 8:
                                                                            count += 1
                                                                        else:
                                                                            for q in range(p+1,gsize-sgsize+9):
                                                                                if (g[i*gsize+j] == g[i*gsize+q]) and (g[i*gsize+j] == g[j*gsize+q]) and (g[i*gsize+j] == g[k*gsize+q]) and (g[i*gsize+j] == g[l*gsize+q]) and (g[i*gsize+j] == g[m*gsize+q]) and (g[i*gsize+j] == g[n*gsize+q]) and (g[i*gsize+j] == g[o*gsize+q]) and (g[i*gsize+j] == g[p*gsize+q]):
                                                                                    if sgsize<=9:
                                                                                        count+=1
                                                                                    else:
                                                                                        for r in range(q+1,gsize-sgsize+10):
                                                                                            if (g[i*gsize+j] == g[i*gsize+r]) and (g[i*gsize+j] == g[j*gsize+r]) and (g[i*gsize+j] == g[k*gsize+r]) and (g[i*gsize+j] == g[l*gsize+r]) and (g[i*gsize+j] == g[m*gsize+r]) and (g[i*gsize+j] == g[n*gsize+r]) and (g[i*gsize+j] == g[o*gsize+r]) and (g[i*gsize+j] == g[p*gsize+r]) and (g[i*gsize+j] == g[q*gsize+r]):
                                                                                                count +=1
    return count

def read_highest_from_file():
    filename = highest_ramsey_dir()
    dim = int(filename.replace("ramsey-","").replace(".txt",""))
    return read_matrix_from_file(filename,dim)


def read_matrix_from_file(filename,dimension):# les galskapen fra fil
    path = PATH_STRING + filename
    delimitter = "-"
    matrix = make_matrix(dimension)
    with open(path, "r") as read_file:
        for i in range(dimension):
            line = read_file.readline()
            lineattributes = line.split(delimitter)
            for j in range(dimension):
                matrix[i][j] = int(lineattributes[j])
    return matrix



##
## Alt under dette er skrevet i C , det skal oversettes til python ettersom dette er algoritmen Rich bruker for a sjekke maxclique
##

#---------------






def brute(): # main
    dim = 10
    #testmatrix = make_matrix(dim)
    #write_matrix_to_file("test3.txt",testmatrix)
    test_read = read_matrix_from_file("test3.txt", dim)
    array_rep = two_to_one_dimensions(test_read)
    counter = 0
    while True:
        while clique_count(array_rep,dim)>0:
            test_read = bitflipper(test_read)
            array_rep = two_to_one_dimensions(test_read)
            counter +=1
        print( "Example of dimension " + str(dim))
        matrix_print(test_read)
        dim += 1
        test_read = expand_matrix(test_read)
        array_rep = two_to_one_dimensions(test_read)
    #matrix_print(test_read)
    #matrix_print(testmatrix)
    #result = has_max_clique(testmatrix,10)
    print("yo")


def wait4better(): # main
    dim = 10
    #testmatrix = make_matrix(dim)
    #write_matrix_to_file("test3.txt",testmatrix)
    test_read = read_matrix_from_file("test3.txt", dim)
    counter = 0
    current_count = 100000000000000
    current_matrix = test_read
    probe_matrix = test_read

    while True:
        while current_count>0:
            probe_matrix = bitflipper(current_matrix)
            probe_array = two_to_one_dimensions(probe_matrix)
            no_ten_cliques = clique_count(probe_array, dim)
            if no_ten_cliques < current_count:
                current_matrix = probe_matrix
                current_count = no_ten_cliques
            counter += 1
        print( "Example of dimension " + str(dim))
        print("antall forsok totalt = " + str(counter))
        matrix_print(current_matrix)
        dim += 1
        current_matrix = expand_matrix(current_matrix)
        current_count = 100000000000

def wait4better2():  # main
    dim = 10
    # testmatrix = make_matrix(dim)
    # write_matrix_to_file("test3.txt",testmatrix)
    test_read = read_matrix_from_file("test3.txt", dim)
    counter = 0
    current_count = 100000000000000
    current_matrix = test_read
    while True:
        while current_count > 0:
            probe_matrix = bitflipper(current_matrix)
            probe_array = two_to_one_dimensions(probe_matrix)
            no_ten_cliques = clique_count(probe_array, dim)
            if counter % 50 == 0:
                if change_to_higher(dim):
                    print("Bytter matrise")
                    current_matrix = read_highest_from_file()
                    current_count = 100000000000000000
                    dim = len(current_matrix[0])
                    continue
            if (current_count > 100):
                print("++++++++++++++ current count " + str(current_count))
                probe_matrix = bitflipper(current_matrix)
                probe_matrix = bitflipper(probe_matrix)
                probe_matrix = bitflipper(probe_matrix)
                probe_matrix = bitflipper(probe_matrix)
                probe_matrix = bitflipper(probe_matrix)
                probe_array = two_to_one_dimensions(probe_matrix)
                no_ten_cliques = clique_count(probe_array, dim)
            if no_ten_cliques < current_count:
                current_matrix = probe_matrix
                current_count = no_ten_cliques
            counter += 1
            if counter%50==0:
                print("-------------------------------------antall 10 cliques = " + str(current_count))
        print("Example of dimension " + str(dim))
        print("antall forsok totalt = " + str(counter))
        write_matrix_to_file(current_matrix)
        #matrix_print(current_matrix)
        dim += 1
        current_matrix = expand_matrix(current_matrix)
        current_count = 100000000000

def send_matrix_to_server(matrix):
    dim = len(matrix[0])
    line = ""
    for i in range(dim):
        for j in range(dim):
            line += str(matrix[i][j])
        line += "\n"
    msg = "{0}\n{1}\n{2}".format(m["SUCCESS"], dim, line)
    server_socket.send(str.encode(msg))
    resp = recv_payload(server_socket).split("\n", 2)
    message_type, n, new_matrix = resp[0], int(resp[1]), resp[2]
    ret_matrix = make_matrix(n)
    if message_type == m["ACK"]:
        new_matrix = new_matrix[:-1].split("\n")
        for i, line in enumerate(new_matrix):
            for j, entry in enumerate(line):
                ret_matrix[i][j] = int(entry)
        return ret_matrix
    else:
        return matrix

def recv_payload(conn):
    payload = ""
    while(1):
        try:
            partial_load = conn.recv(MAX_RECV_LINE)
            partial_load = bytes.decode(partial_load)
            if not partial_load:
                return payload
            else:
                payload += partial_load
        except:
            return payload

def query_server_for_highest():
    server_socket


def startfromhighest():
    # test_read = read_highest_from_file()
    test_read = query_server_for_highest()
    dim = len(test_read[0])
    counter = 0
    current_count = 100000000000000
    current_matrix = test_read
    while True:
        while current_count > 0:
            probe_matrix = bitflipper(current_matrix)
            probe_array = two_to_one_dimensions(probe_matrix)
            no_ten_cliques = clique_count(probe_array, dim)
            if no_ten_cliques < current_count:
                current_matrix = probe_matrix
                current_count = no_ten_cliques
                print("Improved current matrix-> Clique count = " + str(current_count))
            if change_to_higher(dim):
                #startfromhighest()
                current_matrix = expand_matrix(read_highest_from_file())
                print("Changing matrix to another found by other program, now working on " + str(len(current_matrix)))

                current_count = 1000000000001
                dim = len(current_matrix[0])
                continue
            if current_count > 100:
                print("++++++++++++++ currently number of 10-cliques -> " + str(current_count))
                probe_matrix = bitflipper(current_matrix)
                probe_matrix = bitflipper(probe_matrix)
                probe_matrix = bitflipper(probe_matrix)
                probe_matrix = bitflipper(probe_matrix)
                probe_matrix = bitflipper(probe_matrix)
                probe_array = two_to_one_dimensions(probe_matrix)
                no_ten_cliques = clique_count(probe_array, dim)
            if no_ten_cliques < current_count:
                current_matrix = probe_matrix
                current_count = no_ten_cliques
                print("Improved current matrix-> Clique count = " + str(current_count))
            counter += 1
        print("Counterexample found of size " + str(dim))
        print("Number of cycles in total = " + str(counter))
        write_matrix_to_file(current_matrix)
        current_matrix = send_matrix_to_server(current_matrix)
        # matrix_print(current_matrix)
        dim += 1
        current_matrix = expand_matrix(current_matrix)
        current_count = 100000000000

serverPort = 57339
serverName = "0.0.0.0"
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_socket.settimeout(TIMEOUT)
server_socket.connect((serverName,serverPort))
#makeplain10()
#brute()
#wait4better()
#wait4better2()
startfromhighest()
