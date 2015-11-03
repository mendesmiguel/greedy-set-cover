import numpy as np

class Solver(object):

	def __init__(self, A, c):
		self.A_copy = A.copy()
		self.A = A
		self.c = c
		self.m, self.n = self.A_copy.shape
		self.total_cost = 0
		self.U = None
		self.S = []

	def solve(self, alpha, M):
		m, n = self.m, self.n

		C = set()
		self.U = self.__get_universe()
		cj = self.c

		iteration = 0
		print "\nSOLVING..."
		print "U: %s" % (self.U)
		print "cost array c: %s" % (self.c)
		while C != self.U:
			sj, max_ratio = self.__best_set()
			self.S.append(sj)
			elem = np.nonzero(self.A[:, sj] > 0)[0].tolist()
			C = C.union(elem)
			self.__remove_intersection(sj)	
			self.total_cost += cj[sj]
			iteration += 1
			print "# iteration %d: " % (iteration)
			print "Best set found: %d - ratio: %.3f" % (sj, max_ratio)
			print "Sets added to the solution so far: %s" % (self.S) 
			print "C: ", C
		print "DONE!\n\n"

	def __local_search(self, sol):
		# sol: [True, False, True...]
		best_sol_cost = self.__get_cost(sol)
		best_sol = sol.copy()

		for i in range(len(sol)):
			sol_copy = sol.copy()
			sol_copy[i] = not sol_copy[i]
			if self.__is_feasible(sol_copy):
				cost = self.__get_cost(sol_copy)
				if cost < best_sol:
					best_sol_cost = cost
					best_sol = sol_copy
		return best_sol

	def __get_cost(self, sol):
		cost = np.sum(c[sol])
		return cost

	def __is_feasible(self, sol):
		res = np.sum(self.A[:, sol], axis=1)
		return 0 in res

	def __remove_intersection(self, sj):
		p = self.A_copy[:, sj] > 0
		# para cada coluna (set) remova a intersecao
		# print "A = ", self.A_copy
		for j in range(self.n):
			self.A_copy[:, j][p] = 0
		# print "p: ", p
	def __best_set(self):
		max_ratio = -1
		sj = -1

		for j, cj in enumerate(self.c):
			# seleciona a coluna pj
			pj = self.__get_collumn(j)
			# se |pj| / cj > max_ratio entao guarde o indice
			if len(pj) / cj > max_ratio:
				max_ratio = len(pj) / cj
				sj = j
		return sj, max_ratio

	def __get_collumn(self, col_idx):
		return np.nonzero(self.A_copy[:, col_idx] > 0)[0]
	def __get_universe(self):
		return set([i for i in range(self.m)])

	def get_solution_as_sets(self):
		return [self.__get_set_by_index(sj) for sj in self.S]

	def get_total_cost(self):
		return self.total_cost

	def get_solution_as_matrix(self):
		A_copy = self.A.copy()
		return A_copy[:, [sj for sj in self.S]]

	def __get_set_by_index(self, j):
		pj = np.nonzero(self.A[:, j] > 0)[0].tolist()
		return pj

	def print_solution(self):
		print "# universe: %s" % (self.U)
		print "# original sets: "
		for j in range(self.n):
			print "S%d: %s -- cost: %.3f" % (j, self.__get_set_by_index(j), self.c[j])

		print "# solution: "
		for sj in self.S:
			print "S%d: %s" % (sj, self.__get_set_by_index(sj))

		print "Total cost: %.3f" % (self.total_cost)