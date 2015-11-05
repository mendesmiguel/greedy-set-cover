import numpy as np
import random

class Solver(object):

	def __init__(self, A, c):
		self.A_copy = A.copy()
		self.A = A
		self.c = c
		self.m, self.n = self.A_copy.shape
		self.total_cost = 0
		self.S = []

	"""
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
	"""
	def solve(self, alpha, N):
		best_sol = np.ones(self.n, dtype=bool)

		for i in range(N):
			print "iteration {0}: \n".format(i)
			print "best solution found so far {0} has cost: {1}\n".format(best_sol, self._get_cost(best_sol))
			solution = self._greedy_randomized_construction(alpha)
			print "greedy construction generated solution {0} with cost: {1}\n".format(solution, self._get_cost(solution))
			solution = self._local_search(solution)
			print "local search generated solution {0} with cost: {1}\n".format(solution, self._get_cost(solution))

			if self._get_cost(solution) < self._get_cost(best_sol): 
				best_sol = solution
				print "local search produced a better solution {0} with cost: {1}\n".format(best_sol, self._get_cost(solution))
		return best_sol

	def _local_search(self, sol):
		# sol: [True, False, True...]
		best_sol_cost = self._get_cost(sol)
		best_sol = sol.copy()
		print "### local search ###\n"
		for i in range(len(sol)):
			sol_copy = sol.copy()
			sol_copy[i] = not sol_copy[i]
			print "	best solution found so far {0} has cost: {1}\n".format(best_sol, self._get_cost(best_sol))
			print "	solution {0}: {1}\n".format(i, sol_copy)
			if self._is_feasible(sol_copy):
				cost = self._get_cost(sol_copy)
				print "	solution {0} is feasible and has cost: {1}\n".format(sol_copy, cost)
				if cost < best_sol_cost:
					best_sol_cost = cost
					best_sol = sol_copy
		return best_sol

	def _greedy_randomized_construction(self, alpha):
		solution = np.zeros(self.n, dtype=bool)
		print "### greedy randomized construction ###\n"
		# while not self._is_feasible(solution):
		for i in range(5):
			rcl = self._get_rcl(alpha)
			print "	rlc: {0}\n".format(rcl)
			v = self._get_candidate(rcl)
			print "	chosen candidate: {0}\n".format(v)
			solution[v[0]] = True
			print "	solution: {0}\n".format(solution)
			self._remove_intersection(v[0])
		return solution

	def _get_rcl(self, alpha):
		card = np.sum(self.A_copy, axis=0).astype(float)
		n = self.A_copy.shape[1]
		return np.argsort(card)[::-1][:alpha * n]

	def _get_candidate(self, rlc):
		return random.choice(list(enumerate(rlc)))

	def _get_cost(self, sol):
		cost = np.sum(self.c[sol])
		return cost

	def _is_feasible(self, sol):
		res = np.sum(self.A[:, sol], axis=1)
		return 0 in res

	def _remove_intersection(self, sj):
		print "## remove intersection ##"
		print "	before: {0}".format(self.A_copy)
		p = self.A_copy[:, sj] > 0
		# para cada coluna (set) remova a intersecao
		# print "A = ", self.A_copy
		for j in range(self.n):
			self.A_copy[:, j][p] = 0
		print "	after: {0}".format(self.A_copy)
	"""
	def __best_set(self):
		max_ratio = -1
		sj = -1

		for j, cj in enumerate(self.c):
			# seleciona a coluna pj
			pj = self._get_collumn(j)
			# se |pj| / cj > max_ratio entao guarde o indice
			if len(pj) / cj > max_ratio:
				max_ratio = len(pj) / cj
				sj = j
		return sj, max_ratio
	"""

	def _get_collumn(self, col_idx):
		return np.nonzero(self.A_copy[:, col_idx] > 0)[0]

	def _get_universe(self):
		return set([i for i in range(self.m)])

	def get_solution_as_sets(self):
		return [self.__get_set_by_index(sj) for sj in self.S]

	def get_total_cost(self):
		return self.total_cost

	def get_solution_as_matrix(self):
		A_copy = self.A.copy()
		return A_copy[:, [sj for sj in self.S]]

	def _get_set_by_index(self, j):
		pj = np.nonzero(self.A[:, j] > 0)[0].tolist()
		return pj

	def print_solution(self):
		print "# original sets: "
		for j in range(self.n):
			print "S%d: %s -- cost: %.3f" % (j, self._get_set_by_index(j), self.c[j])

		print "# solution: "
		for sj in self.S:
			print "S%d: %s" % (sj, self._get_set_by_index(sj))

		print "Total cost: %.3f" % (self.total_cost)