class Static:
	def __init__(self):
		base_path = os.path.dirname(__file__)
		if not base_path:
			path_solution = "../../textfiles/"
			path_improvements = "../../improvements/"
			path_statistics = "../../clique_distribution.txt"
		else:
			path_solution = base_path + "/../../textfiles/"
			path_improvements = base_path + "/../../improvements/"
			path_statistics = base_path + "/../../clique_distribution.txt"
	
		self.MAX_RECV_LINE = 2048
		self.TIMEOUT = 2
		self.NETWORK_DOWN = True

		self.PATH_STRING_SOLUTION = path_solution
		self.PATH_STRING_IMPROVEMENTS = path_improvements
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
		
		self.STATISTICS_FILENAME = path_statistics
		self.HASHTAGS = "########################"
		self.IMPROVEMENT = "IMPROVEMENT"