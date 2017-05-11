
import threading
class TupleWorker(threading.Thread):

	def __init__(self, thread_id, tup, color_set_list):
		threading.Thread.__init__(self)
		self.thread_lock = threading.Lock()
		self.thread_id = thread_id
		self.tup = tup
		self.color_set_list = color_set_list
		self.error_counter = 0
		self.valid_tuple = False
	
	
	def count_added_ten_cliques_by_tuple(self, thread_name ,tup, color_set_list):
		color_set_list_length = len(color_set_list)
		counter = 0
		bo = False
		for i in range(color_set_list_length-1):
			for j in range(i+1, color_set_list_length):
				set_i = color_set_list[i]
				set_j = color_set_list[j]
				if self.proceed_check(tup, set_i, set_j):
					bo = True
					#self.valid_tuple = True
					diff = set_i.symmetric_difference(set_j)
					if len(diff) == 2 and tup[0] in diff and tup[1] in diff:
						#self.valid_tuple = False
						bo = True
						counter += 1
		self.error_counter = counter

	def proceed_check(self,tup, set_one, set_two):
		a = tup[0]
		b = tup[1]
		if a in set_one and b in set_two:
			return not(b in set_one or a in set_two)
		elif b in set_one and a in set_two:
			return not(a in set_one or b in set_two)
		else:
			return False

	def run(self):
		self.thread_lock.acquire()
		temp = self.count_added_ten_cliques_by_tuple(self.name,self.tup, self.color_set_list)
		self.thread_lock.release()
		return temp




if __name__ == '__main__':
	tup = (1,2)
	s = [set([1,2,3,4,5,6,7,8,9]), set([3,4,5,6,7,8,9,10,11])]
	tup2 = (1,10)
	worker_one	 = TupleWorker(1, tup, s)
	worker_two = TupleWorker(2, tup2, s)
	print worker_one.start()
	print worker_two.start()
	#print worker_one.error_counter
	#print worker_one.valid_tuple

	#print worker_two.error_counter
	#print worker_two.valid_tuple



	#print worker.start_new_thread(count_added_ten_cliques_by_tuple, ( "thread1", tup, s))
	#print worker.start_new_thread(count_added_ten_cliques_by_tuple, ( "thread2", tup, s))




