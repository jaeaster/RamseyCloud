#!/usr/bin/env python

from GreedyAgent import GreedyAgent
from SmartAgent import SmartAgent
from NetworkManager import NetworkManager
from Visualizer import Visualizer
from MatrixManager import MatrixManager
from SMTPClient import SMTPClient
from Static import Static
from Validator import Validator
from NineCliqueAgent import NineCliqueAgent
from FileManager import FileManager

class Main:
	def __init__(self):
		self.network_manager = NetworkManager()
		self.file_manager = FileManager()
		self.nine_clique_agent = NineCliqueAgent(self.network_manager)
		self.smart_agent = SmartAgent(self.network_manager)
		self.visualizer = Visualizer()
		self.matrix_manager = MatrixManager()
		self.smtp_client = SMTPClient()
		self.static = Static()
		self.validator = Validator()


	def main_reduction(self):
	    current_matrix = self.network_manager.fetch_and_expand_matrix()
	    cover_set_log = []
	    counter = 1
	    while True:
	        dim = len(current_matrix[0])
	        self.visualizer.print_hollywood_sign(dim, counter)
	        #current_matrix, is_ce, blue_clique_count, red_clique_count,cover_set,backup = self.smart_agent.smart_reduction(current_matrix,cover_set_log)
	        current_matrix, is_ce, blue_clique_count, red_clique_count,cover_set,backup = self.nine_clique_agent.reduce(current_matrix,cover_set_log)
	        if is_ce:
	            cover_set_log = []
	            current_matrix = self.network_manager.process_new_counter_example(current_matrix)
	            #self.smtp_client.send_email(self.static.MAILING_LIST, dim)
	            counter = 0
	        elif cover_set in cover_set_log:
	            print("a coverset was returned that should not have been returned")
	            current_matrix = self.matrix_manager.re_shuffle_edge(current_matrix)
	            cover_set_log = []
	            print("Starting over, hit a loop")
	            continue
	        else:
	            cover_set_log.append(cover_set)
	        current_matrix = self.network_manager.probe_better_solution(current_matrix)
	       	counter += 1

	def main_smart_expand(self, k):
		current_matrix = self.network_manager.fetch_and_expand_matrix()
		current_matrix = self.matrix_manager.expand_matrix_k_times(current_matrix, k)                                                                   
		cover_set_log = []
		counter = 0
		while True:
			dim = len(current_matrix[0])
			self.visualizer.print_hollywood_sign(dim, counter)
			current_matrix, is_ce, blue_clique_count, red_clique_count,cover_set,backup = self.smart_agent.smart_reduction(current_matrix,cover_set_log)
			temp_file_name = 'ramsey-%d-b:%d-r:%d-test.txt' %(dim,blue_clique_count, red_clique_count)
			self.file_manager.write_matrix_to_file(current_matrix, self.static.PATH_STRING_IMPROVEMENTS, temp_file_name)
			if is_ce:
				cover_set_log = []
				current_matrix = self.network_manager.process_new_counter_example(current_matrix)
				counter = 0
			if cover_set in cover_set_log:
				print("a coverset was returned that should not have been returned")
				current_matrix = self.matrix_manager.re_shuffle_edge(current_matrix)
				cover_set_log = []
				print("Starting over, hit a loop")
				continue
			else:
				cover_set_log.append(cover_set)
			current_matrix = self.network_manager.probe_better_solution(current_matrix)
			counter += 1


	def main_validate(self, start, stop):
		self.validator.validate(start,stop)

def run():
	main = Main()
	main.main_reduction()
	#main.main_smart_expand(30)

if __name__ == '__main__':
	run()




