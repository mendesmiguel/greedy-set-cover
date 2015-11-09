import numpy as np
class FileHandler(object):

	def __init__(self, filename):
		self.f = open(filename)
		self.A = None
		self.c = None
		self.m = 0
		self.n = 0

	def process(self):
		self.__init_matrix()
		self.__create_cost_vector()
		self.__create_matrix()

		self.f.close()
		return self.A, self.c

	def __init_matrix(self):
		m, n = self.f.readline().split()
		self.m, self.n = int(m), int(n)
		self.A = np.zeros((self.m, self.n))
		self.c = np.zeros(self.n)

	def __create_cost_vector(self):
		nums = []
		while len(nums) < self.n:
			nums += self.f.readline().split()
		self.c = np.array(nums).astype(float)

	def __create_matrix(self):
		row = 0
		while row < self.m:
			n = int(self.f.readline())
			# print "n: ", n
			# print "row: ", row
			row_idx = []
			while len(row_idx) < n:
				row_idx += self.f.readline().split()
			row_idx = np.array(row_idx).astype(int) - 1
			# print "row_idx: ", row_idx
			self.A[row][row_idx] = 1
			row += 1