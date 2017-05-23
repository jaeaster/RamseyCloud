from FileManager import FileManager
from Static import Static
from MatrixManager import MatrixManager
from socket import *


TIMEOUT = 2
class NetworkManager:

  def __init__(self):
    self.static = Static()
    self.server_port = 57339
    self.server_name = "100.112.48.4"
    self.m = {
      "SUCCESS": "0",
      "IMPROVEMENT": "1",
      "STATE_QUERY": "2",
      "CLIENT_REGISTER": "3",
      "RAMSEY_REGISTER": "4",
      "MATRIX_ACK": "5",
      "SERVER_LIST_ACK": "6"
    }
    if not self.static.NETWORK_DOWN:
      self.server_socket = socket(AF_INET, SOCK_STREAM)
      self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
      self.server_socket.connect((self.server_name, self.server_port))
    self.file_manager = FileManager()
    self.matrix_manager = MatrixManager()
    

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
      self.server_socket.send(msg)
      ret_matrix = self.recv_matrix()
      if ret_matrix:
          return ret_matrix
      else:
          return matrix

  def recv_matrix(self, timeout=TIMEOUT):
      resp = self.recv_payload(timeout).split("\n", 2)
      if len(resp) < 3:
          return None
      message_type, n, new_matrix = resp[0], int(resp[1]), resp[2]
      if message_type == self.m["MATRIX_ACK"]:
          ret_matrix = self.matrix_manager.make_matrix(n)
          new_matrix = new_matrix.split("\n")
          for i, line in enumerate(new_matrix):
              for j, entry in enumerate(line):
                  if entry == 'E':
                    return ret_matrix
                  ret_matrix[i][j] = int(entry)
          return ret_matrix
      else:
          return None

  def recv_payload(self, timeout=TIMEOUT):
    payload = ""
    self.server_socket.settimeout(timeout)
    while (1):
      try:
        partial_load = self.server_socket.recv(self.static.MAX_RECV_LINE)
        if not partial_load:
            return payload
        else:
            payload += partial_load
            if "END" in partial_load:
                print(payload[:-4])
                return payload[:-4]
      except Exception as e:
        return payload

  def query_server_for_highest(self):
      msg = "{0}\nEND\n".format(self.m["STATE_QUERY"])
      n = self.server_socket.send(msg)
      ret_matrix = self.recv_matrix()
      return ret_matrix

  def probe_better_solution(self, current_matrix):
      if self.static.NETWORK_DOWN:
          dim = len(current_matrix[0])
          if self.file_manager.exists_higher_counter_example(dim):
              current_matrix = self.matrix_manager.expand_matrix(self.file_manager.read_highest_from_file())
              new_dim = dim+1
              print("Found better matrix from other program, now working on %d") %(new_dim)
      else:
          new_matrix = self.recv_matrix(0)
          if new_matrix:
              current_matrix = self.matrix_manager.expand_matrix(new_matrix)
              dim = len(current_matrix[0])
              print ("Received better matrix from server, now working on %d") %dim
      return current_matrix

  def fetch_and_expand_matrix(self):
      if self.static.NETWORK_DOWN:
          current_matrix = self.matrix_manager.expand_matrix(self.file_manager.read_highest_from_file())
      else:
          current_matrix = self.matrix_manager.expand_matrix(self.query_server_for_highest())
      return current_matrix
