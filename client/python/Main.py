#!/usr/bin/env python
from NetworkManager import NetworkManager
from Visualizer import Visualizer
from MatrixManager import MatrixManager
from SMTPClient import SMTPClient
from Static import Static
from Validator import Validator
from NewMatrixAgent import NewMatrixAgent

class Main:
	def __init__(self):
		self.network_manager = NetworkManager()
		self.visualizer = Visualizer()
		self.matrix_manager = MatrixManager()
		self.smtp_client = SMTPClient()
		self.static = Static()
		self.validator = Validator()
		self.new_matrix_agent = NewMatrixAgent(self.network_manager)




	def main_mini_matrix(self):
	    current_matrix = self.network_manager.fetch_and_expand_matrix()
	    cover_set_log = []
	    counter = 1
	    while True:
	        dim = len(current_matrix[0])
	        self.visualizer.print_hollywood_sign(dim, counter)
	        current_matrix, is_ce, blue_clique_count, red_clique_count = self.new_matrix_agent.mini_matrix_reduction(current_matrix)
	        if is_ce:
	            cover_set_log = []
	            current_matrix = self.network_manager.process_new_counter_example(current_matrix)
	            self.smtp_client.send_email(self.static.MAILING_LIST, dim)
	            counter = 0
	        current_matrix = self.network_manager.probe_better_solution(current_matrix)
	       	counter += 1


	def main_mini_matrix_expanded(self, k):
		current_matrix = self.network_manager.fetch_and_expand_matrix()
		current_matrix = self.matrix_manager.expand_matrix_k_times(current_matrix, k)
		cover_set_log = []
		counter = 1
		while True:
			dim = len(current_matrix[0])
			self.visualizer.print_hollywood_sign(dim, counter)
			current_matrix, is_ce, blue_clique_count, red_clique_count = self.new_matrix_agent.mini_matrix_reduction(current_matrix)
			if is_ce:
				cover_set_log = []
				self.smtp_client.send_email(self.static.MAILING_LIST, dim)
				current_matrix = self.network_manager.process_new_counter_example(current_matrix)
				counter = 0
			current_matrix = self.network_manager.probe_better_solution(current_matrix)
			counter += 1

	def main_validate(self, start, stop):
		self.validator.validate(start,stop)

def run():
	main = Main()
	main.main_mini_matrix()
	#main.main_mini_matrix_expanded(65)
	#main.main_k_greedy()
	#main.main_validate(40,80)

if __name__ == '__main__':
	run()




