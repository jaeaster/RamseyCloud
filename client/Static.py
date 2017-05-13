
import os

class Static:
	def __init__(self):
		self.MAX_RECV_LINE = 2048
		self.TIMEOUT = 2
		self.NETWORK_DOWN = False
		self.PATH_STRING_SOLUTION = os.getcwd()+'/../textfiles/'
		self.PATH_STRING_IMPROVEMENTS = os.getcwd() + '/../improvements/'
		self.MAILING_LIST = ['oliver.damsgaard@gmail.com', 'kristoffer.alvern@hotmail.com', 'jonathaneasterman@gmail.com']

		self.THRESHOLD_1 = 5
		self.THRESHOLD_2 = 15
		self.THRESHOLD_3 = 50
		self.GREEDY_THRESHOLD = 1
		self.GREEDY_DOUBLE_THRESHOLD = 3
		self.GREEDY_MAX_THRESHOLD = 10
		self.SMARTH_THRESHOLD = 3
		self.THOUSAND = 1000
		self.MILLION = 1000000
		self.INF = 100000000000
		self.WIDE_PERCENTAGE_THRESHOLD = 0.15
		self.TIGHT_PERCENTAGE_THRESHOLD = 0.1
		
		self.STATISTICS_FILENAME = "../clique_distribution.txt"
		self.HASHTAGS = "########################"
		self.IMPROVEMENT = "IMPROVEMENT"
		self.CLIQUE_TYPE_LIST = ['C9', 'C10']