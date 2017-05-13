import os
from subprocess import Popen, PIPE, call
from TupleWorker import TupleWorker
from MatrixManager import MatrixManager

class TenCliqueWorker():

	def __init__(self):
		# threading.Thread.__init__(self, thread_id)
		# self.thread_id = thread_id
		# self.pool = ThreadPool(processes=45)
		pass

	def generate_ten_clique_tuples(self, ten_clique_array):
		clique_array_length = len(ten_clique_array)
		tuple_list = []
		color = ten_clique_array[0]
		for j in range(1, clique_array_length+1):
			for k in range(j + 1, clique_array_length):
				tuple_list.append((ten_clique_array[j],ten_clique_array[k]))
		return tuple_list, color

	# def generate_nine_clique_color_set(self, nine_clique_double_array, color):
	# 	color_set_list = []
	# 	for li in nine_clique_double_array:
	# 		if li[0] == color:
	# 			color_set_list.append(set(li[1:]))
	# 	return color_set_list

	def generate_nine_clique_color_set_list_string(self, nine_clique_double_array, color):
		string = ''
		length = 0
		for li in nine_clique_double_array:
			if li[0] == color:
				counter = 0
				for c in li[1:]:
					string += str(c)
					counter += 1
					if counter != 9:
						string += ',' 
				string += '|'
				length += 1
		string = string[:-1]
		return string, str(length)

	def genereate_complete_cover_set_for_ten_clique(self, ten_clique_array, nine_clique_double_array):
		all_ten_clique_tuples, color = self.generate_ten_clique_tuples(ten_clique_array)
		nine_clique_color_set_list_string, length = self.generate_nine_clique_color_set_list_string(nine_clique_double_array, color)
		clean_set = []
		dirty_set = []
		for tup in all_ten_clique_tuples: #size 45
			temp_string_tuple = self.generate_tuple_string(tup)
			temp_tup_info = self.fetch_data_from_tuple_worker_c(temp_string_tuple, nine_clique_color_set_list_string, length)
			if self.is_clean_tuple(temp_tup_info):
				clean_set.append(temp_tup_info)
			else:
				dirty_set.append(temp_tup_info)
		return clean_set, dirty_set


	def fetch_data_from_tuple_worker_c(self,tup_string,nine_clique_color_set_list_string, length ):
		path = os.path.dirname(__file__)
		if not path:
			path = "./tuple_worker"
		else:
			path += "/tuple_worker"
		cmd = [path, tup_string, nine_clique_color_set_list_string , length]
		result = Popen(cmd, stdout=PIPE)
		out = result.stdout.read()
		parsed = out.split(':')
		tuple_info = (int(parsed[0]),int(parsed[1]),int(parsed[2]),int(parsed[3]))
		return tuple_info

	def is_clean_tuple(self, temp_result):
		if not temp_result[2] and temp_result[3] == 0:
			return True
		return False

	def invert_color(self, color):
		return int(not color)

	def generate_tuple_string(self, tup):
		string = ''
		string += str(tup[0])
		string += ','
		string += str(tup[1])	
		return string



if __name__ == '__main__':
	w = TenCliqueWorker()	

	ten = [1, 22, 36, 60, 74, 112, 126, 127, 129, 137, 139]
	nine = [[0, 0, 1, 2, 3, 4, 5, 6, 7, 9], [0, 0, 1, 2, 3, 4, 5, 7, 9, 94], [0, 0, 1, 2, 3, 4, 5, 7, 22, 94], [0, 0, 1, 2, 4, 5, 7, 22, 94, 123], [0, 0, 2, 3, 4, 5, 8, 9, 64, 94], [0, 0, 2, 3, 4, 5, 8, 22, 64, 94], [0, 0, 2, 3, 5, 8, 9, 46, 64, 94], [0, 0, 2, 3, 5, 8, 9, 46, 64, 121], [0, 0, 2, 3, 5, 8, 9, 46, 94, 109], [0, 0, 2, 3, 5, 8, 9, 46, 109, 121], [0, 0, 2, 3, 5, 9, 29, 46, 94, 109], [0, 0, 2, 3, 5, 9, 29, 46, 109, 121], [0, 0, 2, 3, 8, 22, 64, 94, 100, 114], [0, 0, 2, 3, 8, 22, 94, 100, 109, 114], [0, 0, 2, 4, 5, 22, 28, 64, 94, 123], [0, 0, 2, 5, 8, 9, 46, 64, 94, 97], [0, 0, 2, 5, 8, 9, 46, 94, 97, 109], [0, 0, 2, 5, 8, 10, 22, 64, 80, 97], [0, 0, 2, 5, 8, 22, 64, 80, 94, 97], [0, 0, 2, 8, 10, 22, 64, 80, 97, 100], [0, 0, 2, 8, 22, 64, 80, 94, 97, 100], [0, 0, 2, 8, 22, 64, 80, 94, 100, 114], [0, 0, 2, 10, 22, 57, 64, 80, 97, 100], [0, 0, 5, 7, 22, 31, 32, 94, 109, 123], [0, 0, 5, 8, 9, 46, 92, 94, 97, 109], [0, 0, 5, 8, 9, 46, 92, 108, 121, 133], [0, 0, 5, 9, 46, 92, 105, 108, 121, 133], [0, 0, 5, 10, 20, 28, 30, 92, 121, 122], [0, 0, 5, 10, 28, 29, 46, 105, 107, 121], [0, 0, 5, 10, 28, 46, 92, 105, 107, 121], [0, 0, 8, 9, 52, 67, 90, 92, 97, 109], [0, 0, 9, 14, 25, 46, 55, 57, 64, 97], [0, 0, 9, 14, 25, 46, 55, 57, 97, 133], [0, 0, 9, 46, 55, 57, 70, 92, 108, 133], [0, 0, 10, 14, 25, 43, 44, 52, 53, 122], [0, 0, 10, 14, 25, 46, 57, 64, 97, 100], [1, 0, 11, 19, 26, 69, 71, 77, 119, 127], [1, 0, 13, 15, 75, 83, 91, 96, 104, 137], [1, 0, 13, 15, 83, 88, 93, 96, 101, 137], [1, 0, 16, 18, 65, 87, 104, 113, 131, 137], [1, 0, 16, 18, 75, 104, 113, 115, 131, 137], [1, 0, 16, 18, 87, 104, 113, 115, 131, 137], [1, 0, 18, 33, 54, 75, 91, 104, 110, 131], [1, 0, 33, 42, 47, 77, 79, 93, 110, 134], [1, 0, 33, 54, 75, 83, 91, 104, 110, 131], [0, 1, 4, 6, 7, 58, 59, 123, 126, 134], [0, 1, 4, 7, 58, 59, 69, 94, 123, 134], [0, 1, 4, 7, 58, 59, 94, 123, 126, 134], [0, 1, 4, 10, 14, 25, 44, 53, 115, 135], [0, 1, 7, 9, 23, 63, 73, 89, 96, 126], [0, 1, 7, 24, 59, 69, 90, 101, 123, 134], [0, 1, 7, 58, 59, 69, 90, 101, 123, 134], [0, 1, 7, 58, 59, 69, 94, 101, 123, 134], [0, 1, 9, 14, 25, 57, 67, 96, 97, 135], [0, 1, 9, 14, 63, 67, 71, 73, 129, 138], [0, 1, 9, 23, 63, 67, 73, 89, 96, 126], [0, 1, 9, 23, 63, 67, 73, 89, 96, 127], [0, 1, 9, 23, 63, 67, 73, 89, 122, 127], [0, 1, 9, 23, 63, 67, 73, 89, 129, 138], [0, 1, 9, 63, 67, 71, 73, 89, 129, 138], [0, 1, 10, 14, 25, 44, 53, 102, 115, 135], [0, 1, 10, 14, 44, 53, 101, 102, 115, 135], [0, 1, 10, 14, 44, 79, 101, 102, 115, 135], [0, 1, 10, 24, 44, 69, 86, 90, 97, 101], [0, 1, 10, 24, 44, 69, 86, 90, 101, 115], [0, 1, 10, 24, 44, 69, 90, 97, 101, 113], [0, 1, 10, 25, 36, 44, 53, 102, 115, 135], [0, 1, 10, 35, 39, 58, 90, 97, 113, 138], [0, 1, 10, 36, 44, 53, 90, 102, 115, 135], [0, 1, 10, 36, 44, 69, 79, 102, 115, 135], [0, 1, 10, 36, 44, 69, 86, 90, 115, 135], [0, 1, 10, 36, 44, 69, 90, 102, 115, 135], [0, 1, 10, 36, 57, 69, 79, 102, 115, 135], [0, 1, 10, 36, 57, 69, 90, 102, 115, 135], [0, 1, 10, 39, 44, 58, 69, 90, 97, 113], [0, 1, 10, 44, 53, 90, 101, 102, 115, 135], [0, 1, 10, 44, 58, 69, 90, 97, 101, 113], [0, 1, 10, 44, 69, 79, 101, 102, 115, 135], [0, 1, 10, 44, 69, 86, 90, 97, 101, 135], [0, 1, 10, 44, 69, 86, 90, 101, 115, 135], [0, 1, 10, 44, 69, 90, 101, 102, 115, 135], [1, 1, 11, 29, 33, 54, 77, 83, 103, 104], [1, 1, 11, 29, 33, 54, 77, 83, 104, 110], [1, 1, 11, 29, 49, 54, 77, 83, 103, 104], [1, 1, 11, 29, 49, 54, 77, 103, 104, 136], [1, 1, 11, 29, 49, 77, 100, 103, 104, 136], [1, 1, 12, 33, 54, 75, 83, 103, 104, 131], [1, 1, 12, 33, 54, 75, 83, 104, 110, 131], [1, 1, 12, 33, 54, 75, 103, 104, 107, 131], [1, 1, 12, 33, 54, 75, 104, 107, 110, 131], [1, 1, 12, 33, 54, 83, 93, 104, 110, 131], [1, 1, 12, 33, 54, 93, 104, 107, 110, 131], [0, 1, 18, 23, 51, 63, 67, 79, 89, 129], [0, 1, 18, 23, 51, 63, 67, 89, 129, 138], [0, 1, 18, 51, 63, 67, 71, 79, 89, 129], [0, 1, 18, 51, 63, 67, 71, 89, 129, 138], [1, 1, 28, 49, 54, 55, 56, 75, 83, 103], [1, 1, 28, 49, 54, 55, 75, 83, 103, 131], [1, 1, 28, 49, 54, 56, 75, 83, 103, 133], [1, 1, 29, 33, 54, 55, 77, 83, 103, 104], [1, 1, 29, 33, 54, 55, 77, 83, 104, 110], [1, 1, 29, 49, 54, 55, 56, 83, 103, 104], [1, 1, 29, 49, 54, 55, 77, 83, 103, 104], [1, 1, 29, 49, 54, 56, 83, 103, 104, 133], [1, 1, 33, 54, 55, 75, 83, 103, 104, 131], [1, 1, 33, 54, 55, 75, 83, 104, 110, 131], [1, 1, 33, 54, 55, 77, 83, 93, 104, 110], [1, 1, 33, 54, 55, 77, 83, 93, 104, 128], [1, 1, 33, 54, 55, 77, 83, 103, 104, 128], [1, 1, 33, 54, 55, 83, 93, 104, 110, 131], [1, 1, 49, 54, 55, 56, 75, 83, 103, 104], [1, 1, 49, 54, 55, 56, 83, 103, 104, 128], [1, 1, 49, 54, 55, 75, 83, 103, 104, 131], [1, 1, 49, 54, 55, 77, 83, 103, 104, 128], [1, 1, 49, 54, 56, 75, 83, 103, 104, 133], [1, 1, 49, 54, 56, 75, 103, 104, 107, 133], [1, 1, 49, 54, 75, 103, 104, 107, 133, 136], [1, 1, 49, 75, 103, 104, 107, 124, 133, 136], [0, 2, 3, 5, 8, 9, 11, 41, 64, 94], [0, 2, 3, 5, 8, 9, 11, 41, 94, 109], [0, 2, 3, 8, 22, 64, 94, 100, 101, 114], [0, 2, 3, 8, 22, 94, 100, 101, 109, 114], [0, 2, 5, 7, 13, 26, 27, 49, 59, 85], [0, 2, 5, 8, 10, 26, 35, 64, 91, 97], [0, 2, 5, 8, 10, 51, 64, 80, 91, 97], [0, 2, 5, 8, 11, 22, 64, 76, 80, 94], [0, 2, 5, 10, 24, 51, 64, 80, 91, 97], [0, 2, 6, 7, 24, 27, 59, 123, 131, 134], [0, 2, 7, 27, 59, 85, 94, 100, 123, 134], [0, 2, 7, 27, 59, 94, 100, 123, 131, 134], [0, 2, 8, 10, 26, 35, 64, 91, 97, 113], [0, 2, 8, 10, 26, 64, 91, 97, 101, 113], [0, 2, 8, 10, 51, 64, 71, 80, 91, 100], [0, 2, 8, 10, 51, 64, 71, 80, 91, 113], [0, 2, 8, 10, 51, 64, 80, 91, 97, 100], [0, 2, 8, 10, 51, 64, 80, 91, 97, 113], [0, 2, 8, 11, 22, 64, 76, 80, 94, 114], [0, 2, 8, 11, 22, 64, 76, 80, 96, 114], [0, 2, 8, 11, 51, 64, 76, 80, 96, 113], [0, 2, 8, 22, 64, 71, 76, 80, 96, 114], [0, 2, 8, 22, 64, 71, 80, 96, 100, 114], [0, 2, 8, 51, 62, 67, 89, 96, 97, 100], [0, 2, 8, 51, 64, 71, 76, 80, 96, 113], [0, 2, 9, 16, 29, 46, 48, 78, 91, 109], [0, 2, 9, 16, 29, 48, 78, 88, 91, 109], [0, 2, 9, 16, 41, 48, 71, 78, 88, 91], [0, 2, 9, 16, 41, 48, 78, 88, 91, 109], [0, 2, 10, 24, 51, 64, 80, 91, 97, 113], [0, 2, 10, 26, 35, 64, 97, 106, 113, 117], [0, 2, 10, 51, 64, 74, 80, 91, 97, 100], [0, 2, 13, 59, 71, 89, 100, 106, 116, 131], [1, 2, 15, 20, 33, 55, 63, 75, 99, 105], [1, 2, 15, 23, 38, 52, 58, 72, 105, 115], [1, 2, 15, 23, 38, 52, 58, 72, 115, 128], [0, 2, 16, 22, 64, 71, 80, 96, 100, 114], [1, 2, 17, 21, 30, 32, 52, 98, 127, 138], [1, 2, 17, 21, 30, 32, 52, 99, 127, 138], [1, 2, 17, 30, 32, 52, 99, 105, 127, 138], [1, 2, 19, 23, 30, 52, 72, 81, 115, 133], [1, 2, 21, 30, 32, 52, 79, 98, 127, 138], [1, 2, 21, 30, 32, 52, 79, 99, 127, 138], [1, 2, 21, 30, 32, 79, 99, 112, 127, 138], [0, 2, 22, 57, 64, 80, 96, 97, 100, 116], [0, 2, 22, 57, 64, 96, 97, 100, 116, 120], [1, 2, 30, 32, 52, 79, 99, 105, 127, 138], [0, 2, 46, 57, 64, 96, 97, 100, 116, 120], [0, 3, 4, 5, 8, 17, 22, 54, 64, 94], [0, 3, 4, 13, 14, 17, 25, 44, 45, 54], [0, 3, 5, 8, 9, 11, 17, 41, 64, 94], [0, 3, 5, 8, 9, 11, 17, 41, 94, 109], [0, 3, 6, 11, 17, 41, 44, 45, 58, 60], [0, 3, 6, 11, 17, 44, 45, 58, 60, 121], [0, 3, 6, 17, 39, 41, 44, 45, 58, 60], [0, 3, 6, 17, 39, 41, 44, 58, 60, 77], [0, 3, 6, 17, 39, 44, 58, 60, 77, 81], [0, 3, 6, 17, 44, 45, 54, 58, 60, 121], [0, 3, 8, 9, 11, 14, 17, 41, 64, 94], [0, 3, 8, 9, 11, 14, 17, 41, 94, 109], [0, 3, 8, 9, 17, 41, 69, 94, 103, 109], [0, 3, 8, 17, 22, 64, 94, 101, 103, 114], [0, 3, 8, 17, 22, 94, 101, 103, 109, 114], [0, 3, 8, 17, 58, 69, 94, 101, 103, 113], [0, 3, 8, 17, 69, 94, 101, 103, 109, 114], [0, 3, 8, 69, 75, 90, 100, 101, 114, 134], [0, 3, 9, 11, 14, 17, 41, 44, 64, 94], [0, 3, 11, 14, 27, 40, 64, 94, 98, 114], [0, 3, 11, 14, 27, 44, 52, 64, 94, 113], [0, 3, 11, 14, 27, 44, 52, 64, 102, 113], [0, 3, 13, 17, 25, 44, 45, 54, 60, 121], [0, 3, 13, 17, 44, 45, 54, 58, 60, 121], [0, 3, 17, 36, 41, 69, 79, 102, 103, 109], [0, 3, 19, 33, 38, 46, 100, 116, 120, 138], [0, 3, 19, 33, 38, 46, 100, 116, 130, 138], [0, 3, 19, 33, 38, 46, 100, 116, 137, 138], [1, 3, 20, 21, 24, 31, 53, 56, 70, 73], [1, 3, 20, 21, 31, 51, 53, 56, 70, 73], [1, 3, 20, 31, 51, 53, 56, 70, 73, 78], [1, 3, 28, 34, 50, 63, 74, 82, 108, 125], [1, 3, 28, 34, 50, 67, 74, 82, 108, 125], [0, 3, 30, 33, 37, 40, 58, 85, 120, 126], [0, 3, 33, 38, 46, 100, 116, 130, 133, 138], [0, 3, 33, 38, 46, 100, 116, 133, 137, 138], [0, 4, 5, 17, 22, 28, 64, 94, 123, 128], [0, 4, 6, 7, 58, 59, 123, 126, 130, 134], [0, 4, 6, 7, 58, 66, 123, 126, 130, 134], [0, 4, 8, 14, 21, 54, 88, 94, 134, 135], [0, 4, 8, 21, 54, 59, 69, 94, 134, 135], [0, 4, 8, 21, 54, 69, 88, 94, 134, 135], [0, 4, 9, 25, 59, 68, 91, 93, 105, 126], [0, 4, 9, 59, 68, 91, 92, 93, 105, 126], [0, 4, 10, 14, 25, 44, 53, 54, 115, 135], [1, 4, 11, 15, 23, 33, 35, 57, 72, 101], [1, 4, 11, 15, 33, 35, 57, 63, 83, 101], [1, 4, 11, 15, 33, 35, 57, 72, 83, 101], [1, 4, 11, 23, 26, 38, 43, 57, 72, 131], [1, 4, 11, 23, 26, 43, 57, 72, 131, 137], [1, 4, 11, 23, 30, 43, 57, 72, 101, 131], [1, 4, 11, 23, 30, 43, 57, 72, 110, 131], [1, 4, 11, 23, 33, 35, 57, 72, 81, 101], [1, 4, 11, 23, 33, 35, 57, 72, 101, 131], [1, 4, 11, 23, 38, 43, 57, 72, 110, 131], [1, 4, 11, 23, 43, 57, 72, 101, 131, 137], [1, 4, 11, 33, 35, 57, 72, 81, 83, 101], [1, 4, 11, 33, 35, 57, 72, 83, 101, 131], [1, 4, 11, 33, 57, 72, 83, 86, 110, 131], [1, 4, 11, 33, 57, 72, 83, 104, 110, 131], [1, 4, 11, 43, 57, 72, 85, 101, 131, 137], [1, 4, 15, 23, 30, 41, 52, 57, 72, 101], [1, 4, 15, 23, 30, 41, 52, 72, 101, 133], [1, 4, 15, 23, 33, 35, 41, 57, 72, 101], [1, 4, 15, 24, 41, 52, 74, 96, 106, 111], [1, 4, 15, 24, 52, 74, 96, 106, 111, 137], [1, 4, 15, 29, 30, 32, 41, 52, 106, 114], [1, 4, 15, 29, 30, 41, 52, 74, 96, 106], [1, 4, 15, 29, 41, 52, 74, 96, 106, 111], [1, 4, 15, 29, 49, 83, 104, 113, 132, 133], [1, 4, 15, 30, 41, 52, 57, 72, 83, 89], [1, 4, 15, 30, 41, 52, 57, 72, 83, 101], [1, 4, 15, 30, 41, 52, 57, 72, 89, 114], [1, 4, 15, 30, 41, 52, 72, 83, 96, 101], [1, 4, 15, 30, 41, 52, 72, 83, 101, 133], [1, 4, 15, 33, 35, 41, 57, 72, 83, 101], [1, 4, 16, 36, 49, 70, 77, 97, 104, 137], [1, 4, 16, 36, 49, 70, 77, 104, 113, 137], [1, 4, 23, 30, 41, 43, 57, 72, 101, 131], [1, 4, 23, 30, 41, 43, 57, 72, 110, 131], [1, 4, 23, 30, 41, 52, 57, 72, 81, 101], [1, 4, 23, 30, 41, 52, 57, 72, 101, 131], [1, 4, 23, 30, 41, 52, 72, 81, 101, 133], [1, 4, 23, 33, 35, 41, 57, 72, 81, 101], [1, 4, 23, 33, 35, 41, 57, 72, 101, 131], [1, 4, 23, 41, 52, 72, 81, 101, 133, 136], [1, 4, 24, 26, 40, 56, 60, 70, 74, 137], [1, 4, 24, 26, 40, 60, 70, 71, 74, 137], [1, 4, 24, 31, 35, 46, 60, 71, 74, 85], [1, 4, 24, 31, 35, 60, 70, 71, 74, 85], [1, 4, 24, 36, 52, 60, 74, 106, 111, 137], [0, 4, 25, 53, 59, 68, 93, 105, 123, 126], [1, 4, 26, 39, 52, 57, 71, 74, 127, 137], [1, 4, 26, 52, 57, 60, 71, 74, 127, 137], [1, 4, 29, 34, 56, 61, 74, 106, 111, 127], [1, 4, 30, 39, 52, 57, 106, 107, 114, 127], [1, 4, 30, 41, 52, 57, 72, 81, 83, 101], [1, 4, 30, 41, 52, 57, 72, 83, 101, 131], [1, 4, 30, 41, 52, 72, 81, 83, 101, 133], [1, 4, 30, 41, 52, 72, 83, 96, 101, 131], [1, 4, 33, 35, 41, 57, 72, 81, 83, 101], [1, 4, 33, 35, 41, 57, 72, 83, 101, 131], [1, 4, 33, 41, 57, 72, 83, 104, 110, 131], [1, 4, 36, 39, 46, 52, 61, 71, 74, 127], [1, 4, 36, 39, 52, 61, 71, 74, 127, 137], [1, 4, 36, 39, 52, 61, 74, 106, 127, 137], [1, 4, 36, 52, 60, 74, 106, 111, 127, 137], [1, 4, 36, 52, 61, 74, 106, 111, 127, 137], [1, 4, 36, 52, 61, 74, 111, 120, 127, 137], [1, 4, 52, 57, 60, 74, 106, 111, 127, 137], [0, 5, 7, 13, 26, 27, 49, 85, 111, 112], [0, 5, 8, 9, 11, 17, 41, 56, 94, 109], [0, 5, 8, 9, 17, 41, 56, 88, 94, 109], [0, 5, 8, 9, 41, 59, 90, 92, 137, 138], [0, 5, 8, 9, 46, 59, 91, 92, 121, 133], [0, 5, 8, 9, 46, 59, 92, 133, 137, 138], [0, 5, 8, 9, 46, 92, 108, 133, 137, 138], [0, 5, 9, 11, 20, 91, 92, 121, 122, 133], [0, 5, 9, 11, 91, 92, 105, 109, 121, 122], [0, 5, 9, 11, 91, 92, 105, 121, 122, 133], [0, 5, 9, 20, 41, 59, 92, 128, 137, 138], [0, 5, 9, 20, 59, 91, 92, 121, 122, 133], [0, 5, 9, 20, 59, 92, 128, 133, 137, 138], [0, 5, 9, 20, 92, 108, 128, 133, 137, 138], [0, 5, 9, 33, 46, 92, 108, 133, 137, 138], [0, 5, 9, 46, 59, 91, 92, 105, 121, 133], [0, 5, 9, 59, 91, 92, 105, 121, 122, 133], [0, 5, 10, 17, 20, 28, 107, 112, 121, 128], [0, 5, 10, 20, 28, 29, 107, 112, 121, 128], [0, 5, 10, 28, 29, 46, 105, 107, 112, 121], [0, 5, 10, 28, 29, 105, 107, 112, 121, 128], [0, 5, 11, 17, 22, 28, 64, 94, 123, 128], [0, 5, 11, 20, 41, 92, 107, 128, 132, 138], [0, 5, 11, 20, 84, 92, 107, 128, 132, 138], [0, 5, 11, 20, 84, 92, 123, 128, 132, 138], [0, 5, 11, 20, 84, 92, 123, 128, 133, 138], [1, 5, 12, 14, 69, 72, 83, 104, 110, 131], [1, 5, 12, 19, 23, 40, 60, 69, 70, 71], [1, 5, 16, 19, 65, 70, 77, 104, 113, 135], [1, 5, 19, 65, 70, 77, 104, 113, 114, 135], [0, 5, 20, 26, 28, 41, 59, 91, 92, 122], [0, 5, 20, 59, 92, 123, 128, 133, 137, 138], [0, 5, 20, 84, 92, 123, 128, 133, 137, 138], [1, 5, 23, 25, 82, 101, 116, 117, 118, 136], [1, 5, 23, 43, 72, 82, 101, 118, 124, 136], [1, 5, 23, 43, 82, 101, 116, 117, 118, 136], [0, 5, 27, 33, 80, 90, 92, 123, 137, 138], [0, 5, 27, 33, 84, 90, 92, 123, 137, 138], [0, 5, 28, 30, 33, 46, 84, 92, 123, 130], [0, 5, 30, 33, 46, 84, 92, 123, 126, 130], [0, 5, 33, 46, 84, 92, 97, 130, 133, 138], [0, 5, 33, 46, 84, 92, 123, 130, 133, 138], [0, 5, 33, 46, 84, 92, 123, 133, 137, 138], [0, 6, 7, 10, 16, 58, 66, 79, 85, 126], [0, 6, 8, 11, 56, 76, 96, 102, 113, 118], [0, 6, 8, 32, 56, 76, 96, 102, 113, 118], [0, 6, 10, 16, 33, 37, 58, 66, 85, 126], [0, 6, 10, 16, 33, 37, 66, 85, 117, 126], [0, 6, 10, 16, 37, 58, 66, 85, 106, 126], [0, 6, 10, 16, 37, 66, 85, 106, 117, 126], [0, 6, 10, 16, 58, 66, 79, 85, 106, 126], [0, 6, 10, 17, 39, 58, 77, 81, 124, 131], [0, 6, 10, 17, 77, 81, 102, 124, 125, 131], [0, 6, 11, 17, 44, 47, 56, 102, 113, 121], [0, 6, 11, 17, 44, 47, 56, 102, 113, 129], [0, 6, 11, 44, 47, 56, 76, 96, 102, 113], [0, 6, 11, 44, 47, 56, 76, 102, 113, 129], [1, 6, 13, 15, 23, 30, 52, 72, 101, 133], [1, 6, 13, 15, 23, 30, 52, 72, 115, 133], [1, 6, 13, 15, 23, 52, 72, 101, 120, 133], [1, 6, 13, 15, 23, 52, 72, 115, 120, 133], [0, 6, 17, 47, 56, 59, 81, 102, 124, 131], [1, 6, 23, 26, 52, 72, 82, 115, 120, 133], [1, 6, 23, 26, 52, 78, 82, 115, 120, 133], [1, 6, 23, 43, 72, 82, 101, 120, 133, 136], [1, 6, 23, 52, 72, 82, 101, 120, 133, 136], [1, 6, 23, 52, 72, 82, 115, 120, 133, 136], [0, 6, 32, 56, 57, 76, 96, 102, 113, 118], [0, 7, 9, 25, 56, 59, 62, 89, 96, 126], [0, 7, 10, 16, 22, 58, 71, 73, 101, 111], [0, 7, 10, 20, 58, 69, 79, 95, 101, 103], [0, 7, 10, 22, 71, 73, 89, 101, 111, 128], [0, 7, 10, 22, 71, 73, 89, 111, 128, 131], [0, 7, 10, 24, 69, 90, 95, 101, 107, 112], [0, 7, 11, 73, 74, 76, 80, 93, 94, 117], [1, 7, 12, 17, 29, 34, 61, 82, 97, 127], [0, 7, 13, 40, 62, 87, 98, 103, 110, 112], [0, 7, 13, 40, 87, 98, 103, 110, 111, 112], [0, 7, 25, 54, 59, 62, 89, 96, 100, 126], [0, 7, 27, 31, 66, 94, 117, 123, 131, 134], [1, 7, 28, 44, 48, 57, 65, 68, 106, 114], [1, 7, 28, 48, 50, 57, 60, 65, 68, 106], [1, 7, 28, 48, 50, 57, 65, 68, 106, 114], [1, 7, 28, 61, 65, 70, 102, 106, 114, 132], [1, 7, 30, 39, 50, 57, 65, 68, 106, 114], [1, 7, 30, 39, 50, 65, 68, 106, 114, 135], [1, 7, 30, 44, 48, 57, 65, 68, 106, 114], [1, 7, 30, 44, 48, 57, 68, 106, 114, 127], [1, 7, 30, 48, 50, 57, 65, 68, 106, 114], [0, 7, 40, 62, 87, 98, 101, 103, 110, 112], [0, 7, 40, 87, 98, 101, 103, 110, 111, 112], [0, 7, 40, 87, 98, 101, 110, 111, 112, 128], [0, 8, 9, 11, 50, 52, 91, 109, 121, 124], [0, 8, 9, 14, 63, 67, 73, 87, 96, 127], [0, 8, 9, 14, 63, 67, 73, 96, 127, 133], [0, 8, 9, 17, 41, 56, 59, 63, 69, 94], [0, 8, 9, 17, 41, 56, 63, 69, 94, 109], [0, 8, 9, 17, 41, 56, 69, 88, 94, 109], [0, 8, 9, 17, 41, 69, 88, 94, 103, 109], [0, 8, 9, 23, 63, 67, 73, 89, 96, 127], [0, 8, 9, 41, 59, 63, 90, 119, 137, 138], [0, 8, 9, 41, 59, 90, 92, 119, 137, 138], [0, 8, 9, 46, 92, 108, 110, 133, 137, 138], [0, 8, 9, 50, 62, 87, 88, 103, 110, 119], [0, 8, 9, 56, 59, 63, 71, 89, 96, 124], [0, 8, 9, 63, 67, 73, 89, 96, 127, 133], [0, 8, 10, 14, 40, 53, 61, 87, 101, 112], [0, 8, 10, 17, 58, 69, 95, 101, 103, 113], [0, 8, 10, 35, 40, 43, 52, 86, 97, 119], [0, 8, 10, 35, 43, 52, 86, 90, 97, 119], [0, 8, 10, 35, 43, 52, 90, 97, 113, 119], [0, 8, 10, 35, 43, 86, 90, 97, 119, 130], [0, 8, 10, 35, 52, 90, 102, 113, 118, 119], [0, 8, 10, 35, 58, 90, 97, 113, 119, 138], [0, 8, 10, 35, 58, 90, 97, 119, 130, 138], [0, 8, 10, 35, 86, 89, 90, 97, 130, 135], [0, 8, 10, 35, 87, 90, 97, 119, 130, 138], [0, 8, 10, 35, 90, 102, 113, 118, 119, 138], [0, 8, 10, 40, 43, 52, 86, 92, 97, 119], [0, 8, 10, 43, 52, 86, 90, 92, 97, 119], [0, 8, 10, 43, 86, 90, 92, 97, 119, 130], [0, 8, 10, 53, 61, 75, 87, 90, 101, 135], [0, 8, 10, 72, 75, 80, 87, 90, 97, 138], [0, 8, 10, 72, 75, 80, 90, 97, 100, 138], [0, 8, 10, 75, 80, 87, 90, 97, 119, 138], [0, 8, 11, 12, 41, 56, 67, 102, 118, 138], [0, 8, 11, 12, 67, 73, 87, 111, 132, 138], [0, 8, 11, 50, 52, 53, 102, 109, 121, 124], [0, 8, 11, 51, 64, 76, 80, 82, 96, 113], [0, 8, 11, 51, 64, 76, 82, 96, 102, 113], [0, 8, 12, 32, 56, 76, 86, 89, 96, 135], [0, 8, 12, 32, 56, 76, 86, 96, 132, 135], [0, 8, 12, 32, 56, 86, 89, 96, 135, 136], [0, 8, 12, 32, 56, 86, 96, 132, 135, 136], [0, 8, 17, 41, 56, 69, 88, 94, 95, 109], [0, 8, 17, 41, 58, 69, 88, 94, 95, 103], [0, 8, 17, 41, 69, 88, 94, 95, 103, 109], [0, 8, 17, 58, 69, 88, 94, 95, 103, 113], [0, 8, 17, 58, 69, 94, 95, 101, 103, 113], [0, 8, 17, 69, 88, 94, 95, 103, 109, 114], [0, 8, 17, 69, 94, 95, 101, 103, 109, 114], [0, 8, 23, 51, 76, 86, 89, 92, 96, 127], [0, 8, 23, 51, 76, 86, 92, 96, 127, 132], [0, 8, 35, 40, 50, 52, 62, 88, 102, 112], [0, 8, 35, 40, 50, 52, 62, 88, 102, 119], [0, 8, 35, 40, 50, 52, 62, 88, 110, 112], [0, 8, 35, 40, 50, 52, 62, 88, 110, 119], [0, 8, 35, 40, 50, 62, 87, 88, 110, 112], [0, 8, 35, 40, 50, 62, 87, 88, 110, 119], [0, 8, 40, 50, 62, 72, 87, 88, 103, 112], [0, 8, 40, 50, 62, 75, 87, 97, 101, 119], [0, 8, 40, 50, 62, 87, 88, 103, 110, 112], [0, 8, 40, 50, 62, 87, 88, 103, 110, 119], [0, 8, 40, 50, 62, 87, 101, 103, 110, 112], [0, 8, 40, 50, 62, 87, 101, 103, 110, 119], [0, 8, 40, 50, 87, 101, 103, 110, 111, 112], [0, 8, 40, 62, 87, 88, 103, 110, 112, 114], [0, 8, 40, 62, 87, 101, 103, 110, 112, 114], [0, 8, 41, 56, 69, 86, 88, 90, 95, 109], [0, 8, 41, 58, 59, 63, 90, 119, 130, 138], [0, 8, 41, 58, 59, 63, 90, 119, 137, 138], [0, 8, 50, 71, 73, 86, 91, 101, 111, 132], [0, 8, 51, 62, 67, 89, 96, 97, 100, 133], [0, 8, 59, 63, 69, 90, 100, 114, 134, 137], [0, 9, 11, 50, 64, 78, 91, 93, 105, 121], [0, 9, 11, 50, 78, 91, 105, 109, 121, 124], [0, 9, 11, 64, 78, 91, 93, 105, 121, 122], [0, 9, 14, 16, 25, 46, 55, 57, 64, 96], [0, 9, 14, 25, 46, 55, 57, 64, 96, 97], [0, 9, 14, 25, 46, 55, 57, 96, 97, 133], [0, 9, 14, 25, 46, 55, 57, 96, 97, 135], [0, 9, 14, 63, 67, 71, 73, 93, 129, 138], [0, 9, 14, 63, 67, 73, 87, 93, 122, 127], [0, 9, 16, 17, 25, 41, 64, 91, 93, 103], [0, 9, 16, 17, 41, 48, 88, 91, 103, 109], [0, 9, 16, 25, 29, 46, 78, 91, 93, 105], [0, 9, 16, 25, 29, 46, 91, 93, 105, 126], [0, 9, 16, 25, 46, 64, 78, 91, 93, 105], [0, 9, 16, 29, 46, 48, 78, 91, 105, 109], [0, 9, 17, 25, 41, 64, 70, 91, 93, 103], [0, 9, 20, 59, 89, 92, 128, 133, 137, 138], [0, 9, 20, 67, 89, 92, 121, 122, 127, 133], [0, 9, 20, 67, 89, 92, 121, 127, 128, 133], [0, 9, 25, 29, 46, 59, 91, 93, 105, 121], [0, 9, 25, 29, 46, 59, 91, 93, 105, 126], [0, 9, 25, 29, 46, 78, 91, 93, 105, 121], [0, 9, 25, 29, 59, 68, 91, 93, 105, 126], [0, 9, 25, 46, 64, 78, 91, 93, 105, 121], [0, 9, 25, 64, 78, 91, 93, 105, 121, 122], [0, 9, 33, 37, 44, 52, 70, 92, 108, 129], [0, 9, 33, 43, 44, 52, 56, 90, 97, 129], [0, 9, 33, 43, 44, 52, 56, 94, 97, 129], [0, 9, 33, 43, 44, 52, 90, 92, 97, 119], [0, 9, 33, 43, 44, 52, 90, 92, 97, 129], [0, 9, 33, 43, 44, 52, 92, 94, 97, 129], [0, 9, 33, 44, 52, 70, 92, 94, 108, 129], [0, 9, 46, 55, 57, 70, 92, 96, 108, 133], [0, 9, 67, 89, 92, 97, 128, 129, 133, 138], [0, 10, 14, 16, 25, 46, 57, 64, 93, 100], [0, 10, 14, 16, 25, 52, 64, 93, 100, 102], [0, 10, 14, 16, 25, 57, 64, 93, 100, 102], [0, 10, 14, 25, 44, 52, 53, 54, 122, 135], [0, 10, 15, 17, 22, 39, 77, 81, 124, 131], [0, 10, 15, 17, 22, 77, 81, 102, 124, 131], [0, 10, 15, 17, 77, 81, 102, 124, 125, 131], [0, 10, 15, 22, 34, 39, 53, 77, 124, 131], [0, 10, 16, 25, 29, 46, 78, 91, 93, 105], [0, 10, 16, 25, 29, 46, 91, 93, 105, 126], [0, 10, 16, 25, 46, 57, 64, 78, 93, 100], [0, 10, 16, 25, 46, 64, 78, 91, 93, 100], [0, 10, 16, 25, 46, 64, 78, 91, 93, 105], [0, 10, 16, 25, 57, 64, 78, 93, 100, 102], [0, 10, 16, 78, 85, 90, 102, 112, 117, 124], [0, 10, 17, 20, 58, 69, 79, 95, 101, 103], [0, 10, 17, 22, 39, 58, 77, 81, 124, 131], [0, 10, 17, 25, 64, 72, 93, 103, 113, 121], [0, 10, 17, 25, 64, 91, 93, 103, 113, 121], [0, 10, 17, 25, 64, 93, 102, 103, 113, 121], [0, 10, 17, 58, 69, 79, 95, 101, 103, 113], [0, 10, 24, 33, 43, 44, 90, 92, 97, 119], [0, 10, 24, 33, 43, 44, 90, 92, 115, 119], [0, 10, 24, 33, 43, 44, 90, 97, 113, 119], [0, 10, 24, 33, 44, 69, 80, 90, 92, 97], [0, 10, 24, 33, 44, 69, 80, 90, 92, 115], [0, 10, 24, 33, 44, 69, 80, 90, 97, 113], [0, 10, 24, 33, 44, 78, 90, 97, 113, 119], [0, 10, 24, 33, 44, 80, 90, 92, 97, 119], [0, 10, 24, 33, 44, 80, 90, 92, 115, 119], [0, 10, 24, 33, 44, 80, 90, 97, 113, 119], [0, 10, 24, 43, 44, 86, 90, 92, 97, 119], [0, 10, 24, 43, 44, 86, 90, 92, 115, 119], [0, 10, 24, 44, 69, 86, 90, 92, 97, 101], [0, 10, 24, 44, 69, 86, 90, 92, 101, 115], [0, 10, 24, 44, 86, 90, 92, 97, 101, 119], [0, 10, 24, 44, 86, 90, 92, 101, 115, 119], [0, 10, 24, 69, 86, 90, 92, 95, 101, 115], [0, 10, 25, 29, 46, 78, 91, 93, 105, 121], [0, 10, 25, 44, 52, 53, 54, 121, 122, 135], [0, 10, 25, 44, 52, 53, 75, 121, 122, 135], [0, 10, 25, 46, 57, 64, 78, 93, 100, 121], [0, 10, 25, 46, 64, 78, 91, 93, 100, 121], [0, 10, 25, 46, 64, 78, 91, 93, 105, 121], [0, 10, 25, 52, 53, 75, 93, 121, 122, 135], [0, 10, 25, 57, 64, 78, 93, 100, 102, 121], [0, 10, 25, 57, 64, 78, 93, 102, 113, 121], [0, 10, 25, 57, 64, 93, 102, 103, 113, 121], [0, 10, 25, 64, 78, 91, 93, 105, 121, 122], [0, 10, 28, 29, 46, 78, 91, 93, 105, 121], [0, 10, 28, 29, 46, 78, 93, 105, 112, 121], [0, 10, 28, 46, 64, 78, 91, 93, 105, 121], [0, 10, 28, 64, 78, 91, 93, 105, 121, 122], [0, 10, 33, 43, 44, 52, 90, 92, 97, 119], [0, 10, 33, 43, 44, 52, 90, 97, 113, 119], [0, 10, 33, 43, 44, 74, 90, 97, 119, 130], [0, 10, 33, 43, 44, 74, 90, 115, 119, 130], [0, 10, 33, 43, 44, 90, 92, 97, 119, 130], [0, 10, 33, 43, 44, 90, 92, 115, 119, 130], [0, 10, 33, 44, 58, 74, 90, 97, 119, 130], [0, 10, 33, 44, 58, 78, 90, 97, 113, 119], [0, 10, 33, 44, 58, 78, 90, 97, 119, 130], [0, 10, 33, 44, 70, 80, 90, 92, 115, 119], [0, 10, 33, 44, 70, 90, 92, 115, 119, 130], [0, 10, 33, 46, 58, 78, 97, 119, 130, 138], [0, 10, 33, 58, 78, 90, 97, 113, 119, 138], [0, 10, 33, 58, 78, 90, 97, 119, 130, 138], [0, 10, 33, 78, 87, 90, 97, 119, 130, 138], [0, 10, 35, 39, 58, 90, 97, 113, 119, 138], [0, 10, 36, 57, 69, 79, 102, 103, 115, 135], [0, 10, 43, 44, 52, 86, 90, 92, 97, 119], [0, 10, 43, 44, 74, 86, 90, 97, 119, 130], [0, 10, 43, 44, 74, 86, 90, 115, 119, 130], [0, 10, 43, 44, 86, 90, 92, 97, 119, 130], [0, 10, 43, 44, 86, 90, 92, 115, 119, 130], [0, 10, 44, 70, 86, 90, 92, 101, 115, 119], [0, 10, 44, 70, 86, 90, 92, 115, 119, 130], [0, 11, 14, 21, 27, 64, 80, 93, 94, 113], [0, 11, 14, 21, 27, 64, 96, 102, 105, 116], [0, 11, 14, 27, 64, 80, 93, 94, 113, 117], [0, 11, 14, 27, 73, 80, 93, 94, 113, 117], [0, 11, 14, 52, 53, 67, 93, 102, 118, 129], [0, 11, 14, 52, 53, 93, 102, 113, 118, 129], [1, 11, 18, 33, 54, 57, 72, 104, 110, 131], [1, 11, 18, 54, 57, 72, 85, 101, 131, 137], [0, 11, 20, 34, 47, 60, 76, 95, 114, 133], [0, 11, 20, 34, 47, 60, 76, 114, 128, 133], [0, 11, 20, 41, 67, 92, 107, 128, 132, 138], [0, 11, 21, 34, 47, 65, 76, 94, 128, 129], [0, 11, 21, 34, 47, 76, 94, 95, 113, 129], [0, 11, 21, 34, 47, 76, 94, 113, 128, 129], [1, 11, 23, 38, 43, 54, 57, 72, 110, 131], [1, 11, 23, 43, 54, 57, 72, 101, 131, 137], [1, 11, 26, 32, 39, 71, 99, 126, 127, 137], [0, 11, 27, 50, 64, 78, 93, 98, 102, 105], [0, 11, 27, 50, 78, 98, 102, 105, 109, 124], [0, 11, 28, 64, 76, 78, 93, 98, 105, 122], [0, 11, 28, 64, 78, 91, 93, 105, 121, 122], [0, 11, 28, 64, 78, 93, 98, 105, 121, 122], [1, 11, 33, 54, 57, 68, 83, 104, 110, 131], [1, 11, 33, 54, 57, 72, 83, 86, 110, 131], [1, 11, 33, 54, 57, 72, 83, 104, 110, 131], [1, 11, 43, 54, 57, 72, 85, 101, 131, 137], [0, 11, 50, 64, 76, 78, 93, 98, 102, 105], [0, 11, 50, 64, 78, 93, 98, 102, 105, 121], [0, 11, 50, 78, 98, 102, 105, 109, 121, 124], [0, 11, 52, 53, 67, 75, 93, 121, 122, 135], [1, 12, 17, 27, 29, 34, 61, 71, 82, 97], [1, 12, 17, 27, 34, 61, 71, 82, 97, 126], [1, 12, 17, 29, 34, 61, 71, 82, 97, 127], [1, 12, 17, 34, 61, 71, 82, 97, 126, 127], [1, 12, 19, 23, 26, 40, 60, 69, 70, 71], [0, 12, 22, 31, 32, 44, 55, 96, 132, 136], [0, 12, 25, 32, 36, 44, 56, 96, 102, 135], [0, 12, 25, 32, 36, 56, 57, 96, 102, 135], [1, 12, 29, 34, 61, 71, 82, 97, 103, 127], [0, 12, 32, 36, 44, 56, 86, 96, 135, 136], [0, 12, 32, 36, 44, 56, 96, 102, 135, 136], [0, 12, 32, 36, 56, 57, 96, 102, 135, 136], [0, 12, 32, 36, 56, 86, 89, 96, 135, 136], [0, 12, 32, 44, 56, 76, 86, 96, 132, 135], [0, 12, 32, 44, 56, 86, 96, 132, 135, 136], [1, 12, 34, 61, 71, 82, 97, 103, 126, 127], [0, 13, 14, 27, 40, 77, 84, 98, 102, 105], [1, 13, 15, 21, 23, 57, 75, 91, 117, 137], [1, 13, 15, 21, 23, 57, 75, 109, 117, 137], [1, 13, 15, 23, 30, 41, 52, 57, 72, 101], [1, 13, 15, 23, 30, 41, 52, 72, 101, 133], [1, 13, 15, 30, 41, 52, 57, 72, 83, 101], [1, 13, 15, 30, 41, 52, 72, 83, 96, 101], [1, 13, 15, 30, 41, 52, 72, 83, 101, 133], [1, 13, 15, 33, 57, 72, 83, 91, 104, 128], [0, 13, 17, 25, 44, 47, 56, 102, 113, 121], [0, 13, 18, 51, 63, 67, 71, 79, 89, 129], [1, 13, 19, 23, 30, 52, 72, 81, 101, 133], [1, 13, 19, 23, 30, 52, 72, 81, 115, 133], [1, 13, 19, 30, 52, 72, 81, 83, 101, 133], [1, 13, 20, 21, 24, 31, 70, 73, 99, 124], [1, 13, 20, 24, 31, 70, 73, 99, 124, 135], [1, 13, 21, 23, 42, 57, 75, 91, 117, 137], [1, 13, 21, 23, 42, 57, 75, 109, 117, 137], [1, 13, 21, 23, 42, 57, 81, 91, 117, 137], [1, 13, 23, 30, 41, 52, 57, 72, 81, 101], [1, 13, 23, 30, 41, 52, 72, 81, 101, 133], [1, 13, 30, 41, 52, 57, 72, 81, 83, 101], [1, 13, 30, 41, 52, 72, 81, 83, 101, 133], [1, 14, 15, 31, 49, 58, 72, 83, 89, 91], [1, 14, 15, 31, 49, 58, 72, 83, 91, 128], [1, 14, 22, 35, 51, 59, 70, 78, 95, 99], [1, 14, 22, 36, 48, 60, 65, 70, 106, 137], [1, 14, 22, 36, 48, 65, 70, 106, 121, 137], [1, 14, 22, 48, 56, 60, 65, 70, 106, 137], [1, 14, 36, 65, 70, 104, 106, 121, 132, 137], [0, 15, 17, 47, 56, 59, 81, 102, 124, 131], [1, 15, 23, 30, 41, 52, 57, 72, 101, 105], [1, 15, 23, 33, 35, 41, 57, 72, 101, 105], [1, 15, 24, 52, 74, 96, 99, 106, 111, 137], [1, 15, 29, 41, 52, 74, 84, 96, 106, 111], [1, 15, 30, 41, 52, 57, 72, 89, 105, 114], [1, 16, 18, 36, 65, 70, 77, 104, 113, 137], [1, 16, 18, 36, 65, 87, 104, 113, 131, 137], [1, 16, 18, 36, 65, 87, 104, 121, 131, 137], [0, 16, 22, 33, 38, 64, 71, 80, 96, 100], [0, 16, 22, 33, 38, 64, 71, 96, 100, 102], [0, 16, 22, 33, 64, 71, 80, 96, 100, 114], [0, 16, 31, 47, 62, 81, 88, 102, 103, 112], [0, 16, 31, 47, 62, 81, 88, 102, 103, 119], [0, 16, 31, 47, 62, 81, 88, 103, 112, 114], [0, 17, 18, 41, 45, 49, 59, 60, 63, 93], [1, 17, 19, 23, 26, 52, 71, 87, 115, 133], [0, 17, 20, 41, 45, 48, 58, 88, 95, 103], [0, 17, 20, 47, 59, 60, 81, 128, 131, 132], [0, 17, 20, 47, 59, 81, 123, 128, 131, 132], [0, 17, 20, 47, 81, 88, 102, 112, 125, 131], [0, 17, 20, 47, 81, 88, 112, 123, 125, 131], [0, 17, 20, 47, 81, 88, 112, 123, 131, 132], [0, 17, 20, 47, 81, 112, 123, 128, 131, 132], [1, 17, 21, 30, 32, 53, 98, 100, 119, 127], [1, 17, 21, 30, 52, 57, 74, 98, 127, 138], [1, 17, 21, 32, 35, 53, 73, 92, 98, 100], [1, 17, 23, 26, 52, 78, 82, 115, 120, 133], [0, 17, 25, 47, 59, 60, 81, 128, 131, 132], [0, 17, 25, 47, 59, 81, 123, 128, 131, 132], [1, 17, 26, 62, 66, 78, 80, 86, 99, 118], [1, 17, 26, 62, 66, 78, 80, 86, 118, 120], [1, 17, 26, 62, 66, 80, 86, 99, 105, 118], [1, 17, 29, 52, 61, 71, 74, 82, 84, 127], [1, 17, 29, 52, 61, 74, 84, 96, 106, 111], [1, 17, 29, 52, 61, 74, 84, 106, 111, 127], [1, 17, 30, 52, 57, 74, 98, 106, 127, 138], [1, 17, 31, 35, 71, 74, 82, 99, 108, 126], [1, 17, 31, 35, 71, 82, 99, 108, 122, 126], [1, 17, 32, 35, 42, 71, 99, 108, 122, 126], [1, 17, 32, 42, 71, 90, 99, 108, 122, 126], [1, 17, 34, 71, 82, 97, 108, 115, 122, 126], [1, 18, 33, 54, 57, 72, 91, 104, 110, 131], [1, 18, 33, 54, 57, 75, 91, 104, 110, 131], [0, 18, 35, 40, 47, 50, 86, 88, 119, 132], [0, 18, 35, 40, 47, 50, 86, 97, 119, 132], [0, 18, 41, 48, 67, 71, 107, 128, 132, 138], [1, 19, 23, 26, 52, 60, 71, 87, 115, 123], [1, 19, 26, 53, 56, 60, 79, 107, 119, 127], [1, 20, 21, 24, 31, 70, 73, 99, 118, 124], [1, 20, 21, 31, 51, 70, 73, 99, 118, 124], [1, 20, 24, 31, 70, 73, 99, 118, 124, 135], [1, 20, 24, 31, 70, 99, 106, 118, 124, 135], [1, 20, 24, 62, 70, 73, 99, 118, 124, 135], [0, 20, 34, 41, 42, 45, 48, 58, 88, 95], [0, 20, 34, 41, 42, 45, 48, 86, 88, 95], [0, 20, 34, 41, 42, 45, 48, 88, 95, 107], [0, 20, 34, 42, 43, 45, 48, 52, 86, 95], [0, 20, 34, 42, 43, 45, 48, 84, 95, 107], [0, 20, 34, 42, 45, 48, 52, 86, 88, 95], [0, 20, 34, 42, 45, 48, 84, 88, 95, 107], [0, 20, 34, 42, 45, 48, 84, 95, 101, 107], [0, 20, 34, 48, 66, 84, 123, 128, 131, 132], [0, 20, 34, 48, 77, 84, 88, 123, 131, 132], [0, 20, 38, 50, 59, 69, 100, 102, 121, 133], [0, 20, 38, 59, 69, 100, 102, 116, 121, 133], [0, 20, 44, 47, 50, 81, 88, 119, 123, 132], [0, 20, 47, 50, 81, 88, 112, 123, 131, 132], [0, 20, 59, 89, 92, 116, 128, 133, 137, 138], [0, 20, 59, 92, 116, 123, 128, 133, 137, 138], [0, 21, 22, 34, 64, 66, 94, 123, 128, 131], [0, 21, 22, 34, 66, 84, 123, 128, 131, 132], [0, 21, 22, 34, 77, 84, 88, 123, 131, 132], [0, 21, 25, 29, 46, 59, 93, 105, 123, 126], [0, 21, 25, 34, 47, 55, 59, 60, 96, 132], [0, 21, 25, 34, 47, 59, 60, 128, 131, 132], [0, 21, 25, 34, 47, 59, 123, 128, 131, 132], [0, 21, 25, 34, 47, 60, 84, 128, 131, 132], [0, 21, 25, 34, 47, 84, 123, 128, 131, 132], [0, 21, 25, 34, 60, 66, 84, 128, 131, 132], [0, 21, 25, 34, 66, 84, 123, 128, 131, 132], [1, 21, 30, 32, 53, 79, 98, 100, 119, 127], [1, 21, 30, 32, 79, 99, 100, 112, 119, 127], [0, 21, 34, 43, 47, 76, 94, 95, 113, 129], [0, 21, 34, 48, 66, 84, 123, 128, 131, 132], [0, 21, 34, 48, 77, 84, 88, 123, 131, 132], [1, 21, 39, 52, 57, 71, 74, 82, 127, 137], [1, 21, 39, 52, 71, 74, 82, 99, 127, 137], [1, 22, 25, 27, 35, 63, 74, 82, 108, 125], [1, 22, 26, 48, 87, 115, 118, 121, 126, 137], [1, 22, 27, 30, 63, 70, 74, 95, 106, 135], [1, 22, 27, 36, 47, 48, 87, 106, 108, 118], [1, 22, 30, 63, 70, 74, 95, 99, 106, 135], [0, 22, 31, 32, 44, 55, 81, 96, 97, 132], [0, 22, 31, 44, 50, 81, 88, 119, 123, 132], [0, 22, 31, 50, 81, 88, 100, 123, 131, 132], [0, 22, 33, 38, 64, 71, 80, 96, 100, 116], [0, 22, 33, 38, 64, 71, 96, 100, 102, 116], [0, 22, 33, 38, 64, 71, 96, 100, 116, 120], [0, 22, 33, 38, 64, 80, 96, 97, 100, 116], [0, 22, 33, 38, 64, 96, 97, 100, 116, 120], [1, 22, 36, 48, 60, 65, 87, 113, 126, 137], [1, 22, 36, 48, 60, 112, 113, 126, 127, 137], [1, 22, 36, 48, 60, 112, 126, 127, 129, 137], [1, 22, 36, 60, 74, 112, 113, 126, 127, 137], [1, 22, 36, 60, 74, 112, 126, 127, 129, 137], [1, 22, 60, 74, 112, 113, 126, 127, 135, 137], [1, 22, 60, 74, 112, 126, 127, 129, 135, 137], [1, 22, 74, 82, 99, 126, 127, 129, 135, 137], [1, 22, 74, 99, 112, 113, 126, 127, 135, 137], [1, 22, 74, 99, 112, 126, 127, 129, 135, 137], [1, 23, 30, 41, 43, 57, 72, 101, 105, 131], [1, 23, 30, 41, 52, 57, 72, 81, 101, 105], [1, 23, 30, 41, 52, 57, 72, 101, 105, 131], [1, 23, 33, 35, 41, 57, 72, 81, 101, 105], [1, 23, 33, 35, 41, 57, 72, 101, 105, 131], [1, 23, 33, 41, 54, 57, 72, 81, 101, 105], [1, 23, 33, 41, 54, 57, 72, 101, 105, 131], [1, 23, 41, 43, 54, 57, 72, 82, 101, 131], [1, 23, 41, 43, 54, 57, 72, 101, 105, 131], [1, 23, 41, 43, 54, 72, 82, 101, 133, 136], [1, 23, 41, 43, 72, 82, 101, 124, 133, 136], [1, 23, 43, 54, 57, 72, 82, 91, 131, 137], [1, 23, 43, 54, 57, 72, 82, 101, 131, 137], [0, 24, 27, 33, 43, 44, 84, 90, 92, 115], [0, 24, 27, 33, 43, 44, 84, 90, 92, 123], [0, 24, 27, 33, 43, 66, 84, 90, 92, 115], [0, 24, 27, 33, 43, 66, 84, 90, 92, 123], [1, 24, 28, 48, 56, 60, 65, 70, 106, 137], [1, 24, 28, 48, 56, 60, 65, 87, 106, 137], [0, 24, 30, 33, 69, 80, 82, 88, 90, 113], [0, 24, 33, 44, 69, 80, 82, 88, 90, 113], [0, 24, 33, 44, 80, 82, 88, 90, 113, 119], [0, 24, 43, 47, 76, 86, 92, 95, 115, 127], [0, 24, 69, 86, 90, 92, 95, 101, 109, 115], [0, 24, 69, 90, 92, 95, 101, 109, 114, 115], [1, 25, 27, 28, 63, 74, 82, 101, 108, 125], [1, 25, 27, 35, 63, 74, 82, 101, 108, 125], [1, 25, 27, 39, 63, 74, 82, 101, 108, 125], [1, 25, 28, 74, 82, 101, 120, 125, 129, 137], [0, 25, 31, 32, 44, 55, 81, 96, 97, 132], [0, 25, 31, 44, 47, 55, 81, 96, 97, 132], [0, 25, 34, 47, 53, 59, 123, 128, 131, 132], [0, 25, 34, 47, 55, 59, 60, 96, 114, 133], [0, 25, 34, 47, 70, 84, 123, 128, 131, 133], [0, 25, 51, 62, 67, 89, 96, 97, 100, 133], [0, 25, 52, 53, 67, 75, 93, 121, 122, 135], [1, 26, 39, 52, 57, 71, 74, 82, 127, 137], [1, 26, 39, 52, 71, 74, 82, 99, 127, 137], [1, 26, 39, 57, 71, 74, 82, 126, 127, 137], [1, 26, 39, 71, 74, 82, 99, 126, 127, 137], [1, 27, 28, 55, 74, 82, 101, 125, 126, 129], [1, 27, 36, 39, 55, 74, 101, 121, 126, 129], [1, 27, 39, 55, 74, 82, 101, 125, 126, 129], [0, 27, 40, 50, 53, 102, 112, 117, 124, 131], [0, 28, 29, 46, 78, 93, 98, 105, 112, 121], [1, 28, 38, 54, 57, 72, 86, 114, 129, 131], [0, 28, 43, 47, 76, 92, 94, 95, 115, 127], [1, 28, 48, 50, 57, 60, 65, 68, 106, 137], [1, 28, 54, 57, 72, 81, 83, 101, 129, 137], [1, 28, 54, 57, 72, 82, 101, 129, 131, 137], [1, 28, 54, 57, 72, 83, 101, 129, 131, 137], [1, 28, 57, 74, 82, 101, 125, 126, 129, 137], [1, 28, 57, 74, 82, 101, 126, 129, 131, 137], [0, 30, 33, 56, 69, 80, 82, 88, 90, 113], [0, 30, 36, 56, 69, 82, 86, 88, 90, 109], [1, 30, 39, 52, 57, 65, 68, 106, 107, 114], [1, 30, 39, 52, 57, 68, 106, 107, 114, 127], [1, 31, 39, 74, 82, 99, 126, 127, 129, 135], [0, 31, 44, 47, 50, 81, 88, 119, 123, 132], [0, 31, 44, 47, 55, 81, 92, 96, 97, 132], [0, 31, 44, 47, 55, 92, 96, 97, 130, 133], [0, 31, 47, 50, 62, 81, 88, 102, 103, 112], [0, 31, 47, 50, 62, 81, 88, 102, 103, 119], [0, 31, 47, 50, 62, 81, 88, 103, 112, 123], [0, 31, 47, 50, 62, 81, 88, 103, 119, 123], [0, 31, 47, 50, 81, 88, 112, 123, 131, 132], [0, 31, 47, 55, 57, 92, 96, 97, 130, 133], [0, 31, 50, 62, 81, 88, 103, 110, 112, 123], [0, 31, 50, 62, 81, 88, 103, 110, 119, 123], [0, 31, 55, 57, 92, 96, 97, 116, 130, 133], [0, 33, 38, 46, 64, 96, 97, 100, 116, 120], [0, 33, 38, 46, 96, 97, 100, 116, 130, 133], [0, 33, 38, 46, 97, 100, 116, 130, 133, 138], [1, 33, 41, 54, 57, 68, 83, 104, 110, 131], [1, 33, 41, 54, 57, 72, 83, 104, 110, 131], [0, 33, 43, 44, 52, 56, 76, 94, 113, 129], [0, 33, 43, 44, 52, 56, 90, 97, 113, 129], [0, 33, 43, 44, 52, 56, 94, 97, 113, 129], [0, 33, 44, 56, 69, 80, 82, 88, 90, 113], [0, 33, 44, 56, 69, 82, 88, 90, 102, 113], [0, 33, 46, 66, 70, 84, 92, 123, 126, 130], [1, 33, 54, 57, 72, 83, 91, 104, 110, 131], [1, 33, 54, 57, 72, 91, 104, 107, 110, 131], [1, 33, 54, 57, 75, 83, 91, 104, 110, 131], [1, 33, 54, 57, 75, 91, 104, 107, 110, 131], [0, 34, 40, 47, 53, 112, 124, 128, 131, 132], [0, 36, 41, 56, 69, 86, 88, 90, 95, 109], [1, 38, 54, 57, 72, 86, 105, 114, 129, 131], [1, 39, 52, 55, 63, 74, 78, 82, 101, 125], [1, 39, 52, 55, 63, 74, 78, 82, 103, 125], [1, 39, 55, 74, 78, 82, 101, 125, 126, 129], [1, 39, 57, 74, 82, 101, 125, 126, 129, 137], [1, 39, 57, 74, 82, 101, 126, 127, 129, 137], [1, 39, 74, 82, 99, 126, 127, 129, 135, 137], [0, 40, 47, 50, 62, 98, 101, 102, 103, 112], [0, 40, 50, 62, 87, 98, 101, 103, 110, 112], [0, 40, 50, 87, 98, 101, 103, 110, 111, 112], [0, 40, 62, 87, 98, 101, 103, 110, 112, 114], [1, 41, 43, 54, 57, 72, 85, 101, 105, 131], [1, 41, 43, 54, 57, 72, 85, 105, 114, 131], [0, 41, 44, 70, 86, 90, 92, 115, 119, 130], [0, 46, 47, 55, 57, 70, 84, 92, 115, 130], [0, 46, 47, 55, 57, 70, 84, 92, 130, 133], [0, 46, 47, 55, 57, 70, 92, 96, 115, 130], [0, 46, 47, 55, 57, 70, 92, 96, 130, 133], [0, 46, 47, 55, 57, 84, 92, 97, 130, 133], [0, 46, 47, 55, 57, 92, 96, 97, 130, 133], [0, 46, 55, 57, 70, 92, 96, 108, 130, 133], [0, 46, 55, 57, 70, 92, 96, 116, 130, 133], [0, 46, 55, 57, 92, 96, 97, 116, 130, 133], [0, 50, 64, 71, 76, 78, 93, 98, 102, 105], [0, 50, 70, 87, 98, 101, 103, 110, 111, 112], [0, 68, 70, 72, 75, 87, 93, 98, 122, 125]]
	n = [[0, 0, 1, 2, 3, 4, 5, 6, 7, 9], [0, 0, 1, 2, 3, 4, 5, 7, 9, 94], [0, 0, 1, 2, 3, 4, 5, 7, 22, 94]]
	print w.genereate_complete_cover_set_for_ten_clique(ten, n)

