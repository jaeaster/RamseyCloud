

from FileManager import FileManager
from Static import Static
from MatrixManager import MatrixManager
from socket import *


TIMEOUT = 2
class NetworkManager:

	def __init__(self):
		self.file_manager = FileManager()
		self.matrix_manager = MatrixManager()
		self.static = Static()
		self.serverPort = 57339
		self.serverName = "128.111.43.14"
		self.m = {
    			"SUCCESS": "0",
				"ACK": "1",
    			"STATE_QUERY": "2",
    			"IMPROVEMENT": "3"
				}
		if not self.static.NETWORK_DOWN:
		    self.server_socket = socket(AF_INET, SOCK_STREAM)
		    self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		    self.server_socket.connect((serverName, serverPort))
		

	def process_new_counter_example(self,matrix):
	    if self.static.NETWORK_DOWN:
	        self.file_manager.write_matrix_to_file(matrix, self.static.PATH_STRING_SOLUTION, self.file_manager.generate_solution_filename(matrix))
	    else:
	        self.send_matrix_to_server(matrix, "SUCCESS")
	    new_matrix = self.matrix_manager.expand_matrix(matrix)
	    return new_matrix

	def send_matrix_to_server(self, matrix, message_type, num_cliques=0):
	    dim = len(matrix[0])
	    line = ""
	    for i in range(dim):
	        for j in range(dim):
	            line += str(matrix[i][j])
	        line += "\n"
	    if message_type == "SUCCESS":
	        msg = "{0}\n{1}\n{2}END\n".format(self.m[message_type], dim, line)
	    elif message_type == "IMPROVEMENT":
	        msg = "{0}\n{1}\n{2}\n{3}END\n".format(self.m[message_type], num_cliques, dim, line)
	    self.server_socket.send(str.encode(msg))
	    ret_matrix = self.recv_matrix(server_socket)
	    if ret_matrix:
	        return ret_matrix
	    else:
	        return matrix

	def recv_matrix(self, conn, timeout=TIMEOUT):
	    resp = self.recv_payload(conn, timeout).split("\n", 2)
	    if len(resp) < 3:
	        return False
	    message_type, n, new_matrix = resp[0], int(resp[1]), resp[2]
	    if message_type == self.m["ACK"]:
	        ret_matrix = make_matrix(n)
	        new_matrix = new_matrix.split("\n")
	        for i, line in enumerate(new_matrix):
	            for j, entry in enumerate(line):
	                ret_matrix[i][j] = int(entry)
	        return ret_matrix
	    else:
	        return False

	def recv_payload(self,conn, timeout=TIMEOUT):
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

	def query_server_for_highest(self):
	    msg = "{0}\nEND\n".format(self.m["STATE_QUERY"])
	    self.server_socket.send(str.encode(msg))
	    ret_matrix = self.recv_matrix(server_socket)
	    return ret_matrix

	def probe_better_solution(self, current_matrix):
	    if self.static.NETWORK_DOWN:
	        dim = len(current_matrix[0])
	        if self.file_manager.exists_higher_counter_example(dim):
	            current_matrix = self.matrix_manager.expand_matrix(self.file_manager.read_highest_from_file())
	            new_dim = dim+1
	            print("Found better matrix from other program, now working on %d") %(new_dim)
	    else:
	        new_matrix = self.network_manager.recv_matrix(self.network_manager.server_socket, 0)
	        if new_matrix:
	            current_matrix = self.matrix_manager.expand_matrix(new_matrix)
	            dim = len(current_matrix[0])
	            print ("Received better matrix from server, now working on %d") %dim
	    return current_matrix

	def fetch_and_expand_matrix(self):

	    if self.static.NETWORK_DOWN:
	        current_matrix = self.matrix_manager.expand_matrix(self.file_manager.read_highest_from_file())
	    else:
	        current_matrix = self.matrix_manager.expand_matrix(query_server_for_highest())
	    return current_matrix
