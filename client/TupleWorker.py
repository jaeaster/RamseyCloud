
import threading
class TupleWorker(threading.Thread):

	def __init__(self):
		pass
		#threading.Thread.__init__(self)
		#self.thread_lock = threading.Lock()
		#self.thread_id = thread_id

	def count_added_ten_cliques_by_tuple(self, tup, color_set_list): #cross-checks one tuple with all of the nine cliques of opposite color
		color_set_list_length = len(color_set_list)
		counter = 0
		proved_dirty = False
		for i in range(color_set_list_length-1): #for each 9 clique one
			for j in range(i+1, color_set_list_length): #for each 9 clique two (nine clique one and two are compared)
				set_i = color_set_list[i] #nine clique one
				set_j = color_set_list[j] #nine clique two
				if self.proceed_check(tup, set_i, set_j): 
					diff = set_i.symmetric_difference(set_j)
					if len(diff) == 2 and tup[0] in diff and tup[1] in diff:
						proved_dirty = True
						counter += 1
		return tup[0], tup[1], proved_dirty, counter #Returns tuple value one, tuple value two, is_dirty boolean, 
													#and cost of flipping the edge represented by the tuple

	# def proceed_check(self,tup, set_one, set_two):
	# 	a = tup[0]
	# 	b = tup[1]
	# 	if a in set_one and b in set_two:
	# 		return not(b in set_one or a in set_two)
	# 	elif b in set_one and a in set_two:
	# 		return not(a in set_one or b in set_two)
	# 	else:
	# 		return False

	def proceed_check(self, tup, set_one, set_two):
		a = tup[0]
		b = tup[1]
		if a in set_one and b in set_two:
			return True
		elif a in set_two and b in set_one:
			return True
		else:
			return False 





	# def run(self):
	# 	self.thread_lock.acquire()
	# 	temp = self.count_added_ten_cliques_by_tuple()
	# 	self.thread_lock.release()
	# 	return temp




if __name__ == '__main__':
	tup = (1,2)
	s = [set([1,3,4,5,6,7,8,9,10]), set([2,3,4,5,6,7,8,9,10])]
	tup2 = (1,10)
	#worker_one	 = TupleWorker(1, tup, s, q)
	#worker_two = TupleWorker(2, tup2, s, q)
	#worker_one.start()
	#worker_two.start()
	w = TupleWorker()
	r = w.count_added_ten_cliques_by_tuple(tup, s)
	print r


