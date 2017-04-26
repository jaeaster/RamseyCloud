import os
from random import randint

from socket import *

MAX_RECV_LINE = 2048
TIMEOUT = 2
NETWORK_DOWN = False
PATH_STRING = os.getcwd() + "/counterexamples/"

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

def re_shuffle_edge(matrix):
    size = len(matrix[0])
    for i in range(size-1):
        a = randint(0,1)
        matrix[size-1][i] = a
        matrix[i][size-1] = a
    return matrix



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

def bitflipper2(matrix):
    a = len(matrix[0])
    b = randint(0,a-1)
    if matrix[b][a-1] == 0:
        matrix[a-1][b] = 1
        matrix[b][a-1] = 1
    else:
        matrix[a-1][b] = 0
        matrix[b][a-1] = 0
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
                                        count += 1
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
                                                                                                count += 1
    return count


def clique_count2(g,gsize):# g is an array of all, contains stats on number of cliques
    count5 = 0
    count6 = 0
    count7 = 0
    count8 = 0
    count9 = 0
    count10 = 0
    sgsize = 10
    for i in range(gsize-sgsize+1):
        for j in range(i+1,gsize-sgsize+2):
            for k in range(j+1,gsize-sgsize+3):
                if(g[i*gsize+j] == g[i*gsize+k]) and (g[i*gsize+j] == g[j*gsize+k]):
                    for l in range(k+1,gsize-sgsize+4):
                        if (g[i * gsize + j] == g[i * gsize + l]) and (g[i * gsize + j] == g[j * gsize + l]) and (g[i * gsize + j] == g[k * gsize + l]):
                            for m in range(l+1,gsize-sgsize+5):
                                if (g[i * gsize + j] == g[i * gsize + m]) and (g[i * gsize + j] == g[j * gsize + m]) and (g[i * gsize + j] == g[k * gsize + m]) and (g[i * gsize + j] == g[l * gsize + m]):
                                    count5 += 1
                                    for n in range(m+1,gsize-sgsize+6):
                                        if(g[i * gsize + j] == g[i * gsize + n]) and (g[i * gsize + j] == g[j * gsize + n]) and (g[i * gsize + j] == g[k * gsize + n]) and (g[i * gsize + j] == g[l * gsize + n]) and (g[i * gsize + j] == g[m * gsize + n]):
                                            count6+=1
                                            for o in range(n+1,gsize-sgsize+7):
                                                if (g[i*gsize+j] == g[i*gsize+o]) and (g[i*gsize+j] == g[j*gsize+o]) and (g[i*gsize+j] == g[k*gsize+o]) and (g[i*gsize+j] == g[l*gsize+o]) and (g[i*gsize+j] == g[m*gsize+o]) and (g[i*gsize+j] == g[n*gsize+o]):
                                                    count7 +=1
                                                    for p in range(o+1,gsize-sgsize+8):
                                                        if(g[i * gsize + j] == g[i * gsize + p]) and (g[i * gsize + j] == g[j * gsize + p]) and (g[i * gsize + j] == g[k * gsize + p]) and (g[i * gsize + j] == g[l * gsize + p]) and (g[i * gsize + j] == g[m * gsize + p]) and (g[i * gsize + j] == g[n * gsize + p]) and (g[i * gsize + j] == g[o * gsize + p]):
                                                            count8 += 1
                                                            for q in range(p+1,gsize-sgsize+9):
                                                                if (g[i*gsize+j] == g[i*gsize+q]) and (g[i*gsize+j] == g[j*gsize+q]) and (g[i*gsize+j] == g[k*gsize+q]) and (g[i*gsize+j] == g[l*gsize+q]) and (g[i*gsize+j] == g[m*gsize+q]) and (g[i*gsize+j] == g[n*gsize+q]) and (g[i*gsize+j] == g[o*gsize+q]) and (g[i*gsize+j] == g[p*gsize+q]):
                                                                    count9+=1
                                                                    for r in range(q+1,gsize-sgsize+10):
                                                                        if (g[i*gsize+j] == g[i*gsize+r]) and (g[i*gsize+j] == g[j*gsize+r]) and (g[i*gsize+j] == g[k*gsize+r]) and (g[i*gsize+j] == g[l*gsize+r]) and (g[i*gsize+j] == g[m*gsize+r]) and (g[i*gsize+j] == g[n*gsize+r]) and (g[i*gsize+j] == g[o*gsize+r]) and (g[i*gsize+j] == g[p*gsize+r]) and (g[i*gsize+j] == g[q*gsize+r]):
                                                                            print("c5 " + str(count5))
                                                                            count10 += 1
    return count5,count6,count7,count8,count9,count10

def clique_count3(g,gsize):# g is an array of all, contains stats on number of cliques
    sgsize = 10
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
                                                                            return True
    return False



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

def edgecounter(matrix):
    dim = len(matrix[0])
    edgearray = [0]*dim
    for i in range(dim):
        for j in range(dim):
            if matrix[i][j] == 1:
                edgearray[i] += 1
    return edgearray

def startfromhighest():
    test_read = read_highest_from_file()
    dim = len(test_read[0])
    counter = 0
    current_count10 = 100000000000000
    current_count9 = 10000000000000
    current_matrix = test_read
    while True:
        while current_count10 > 0:
            probe_matrix = bitflipper2(current_matrix)
            probe_array = two_to_one_dimensions(probe_matrix)
            c5,c6,c7,c8,c9,c10 = clique_count2(probe_array, dim)
            print("c5 " + str(c5) + "    c6 " + str(c6) + "   c7 " + str(c7) + "   c8 " + str(c8) + "   c9 " + str(c9) + "     c10 " + str(c10))

            if c10 < current_count10 or (c10 == current_count10 and c9 < current_count10):
                current_matrix = probe_matrix
                current_count10 = c10
                print("c5" + str(c5)+"    c6 " + str(c6)+"   c7 " + str(c7)+"   c8 " + str(c8)+"   c9 " + str(c9)+"     c10 " + str(c10))
                print("Improved current matrix-> Clique count = " + str(current_count10))
            if change_to_higher(dim):
                #startfromhighest()
                current_matrix = expand_matrix(read_highest_from_file())
                print("Changing matrix to another found by other program, now working on " + str(len(current_matrix)))
                current_count10 = 1000000000001
                current_count9 = 1000000000001
                dim = len(current_matrix[0])
                continue
            if current_count10 > 1:# pass pa a bytte denne tilbake
                print("++++++++++++++ currently number of 10-cliques -> " + str(current_count10))
                probe_matrix = re_shuffle_edge(current_matrix)
                #probe_matrix = bitflipper2(current_matrix)
                #probe_matrix = bitflipper2(probe_matrix)
                #probe_matrix = bitflipper2(probe_matrix)
                #probe_matrix = bitflipper(probe_matrix)
                #probe_matrix = bitflipper(probe_matrix)
                probe_array = two_to_one_dimensions(probe_matrix)
                c5, c6, c7, c8, c9, c10 = clique_count2(probe_array, dim)
                print("c5 " + str(c5)+"    c6 " + str(c6)+"   c7 " + str(c7)+"   c8 " + str(c8)+"   c9 " + str(c9)+"     c10 " + str(c10))
            if c10 < current_count10:
                current_matrix = probe_matrix
                current_count10 = c10
                print("Improved current matrix-> Clique count = " + str(current_count10))
            counter += 1
        print("Counterexample found of size " + str(dim))
        print("Number of cycles in total = " + str(counter))
        write_matrix_to_file(current_matrix)
        # matrix_print(current_matrix)
        dim += 1
        current_matrix = expand_matrix(current_matrix)
        current_count10 = 100000000000
        current_count9 = 100000000000

def main():
    if NETWORK_DOWN:
        current_matrix = read_highest_from_file()
        print("Read matrix from filesystem")
    else:
        current_matrix = expand_matrix(query_server_for_highest())
        print("Read matrix from server")   
    dim = len(current_matrix[0])
    counter = 0
    while True:
        probe_matrix = re_shuffle_edge(current_matrix)
        probe_array = two_to_one_dimensions(probe_matrix)
        found = not clique_count3(probe_array, dim)
        if found:
            current_matrix = process_new_counterexample(probe_matrix, dim, counter)
            dim += 1
            counter += 1
            continue
        if NETWORK_DOWN:
            if change_to_higher(dim):
                current_matrix = expand_matrix(read_highest_from_file())
                dim = len(current_matrix[0])
                print("Found better matrix from other program, now working on " + str(dim))
                continue
        else:
            new_matrix = recv_matrix(server_socket, 0)
            if new_matrix:
                current_matrix = expand_matrix(new_matrix)
                dim = len(current_matrix[0])
                print("Received better matrix from server, now working on " + str(dim))
                continue

            
        

def process_new_counterexample(matrix, dim, counter):
    print("Counterexample found of size " + str(dim))
    print("Number of cycles in total = " + str(counter))
    if NETWORK_DOWN:
        write_matrix_to_file(matrix)
    else:
        send_matrix_to_server(matrix)
    new_matrix = expand_matrix(matrix)
    return new_matrix


# Networking Code below here

def send_matrix_to_server(matrix):
    dim = len(matrix[0])
    line = ""
    for i in range(dim):
        for j in range(dim):
            line += str(matrix[i][j])
        line += "\n"
    msg = "{0}\n{1}\n{2}END\n".format(m["SUCCESS"], dim, line)
    server_socket.send(str.encode(msg))
    ret_matrix = recv_matrix(server_socket)
    if ret_matrix:
        return ret_matrix
    else:
        return matrix

def recv_matrix(conn, timeout = TIMEOUT):
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

def recv_payload(conn, timeout = TIMEOUT):
    payload = ""
    conn.settimeout(timeout)
    while(1):
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
    server_socket.connect((serverName,serverPort))
main()
