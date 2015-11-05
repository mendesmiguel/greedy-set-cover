import numpy as np
import random

class Solver(object):

	def __init__(self, A, c):
		self.A_copy = A.copy()
		self.A = A
		self.c = c
		self.c_copy = c.copy()
		self.m, self.n = self.A_copy.shape
		self.total_cost = 0
		self.S = None

	def solve(self, alpha, N):
		best_sol = np.ones(self.n, dtype=bool)

		for i in range(N):
			self.A_copy = self.A.copy()
			self.c_copy = self.c.copy()
			print "iteration {0}:".format(i)
			print "best solution found so far {0} has cost: {1}".format(best_sol, self._get_cost(best_sol))
			solution = self._greedy_randomized_construction(alpha)
			print "greedy construction generated solution {0} with cost: {1}".format(solution, self._get_cost(solution))
			solution = self._local_search(solution)
			print "local search generated solution {0} with cost: {1}".format(solution, self._get_cost(solution))

			if self._get_cost(solution) < self._get_cost(best_sol): 
				best_sol = solution
				print "local search produced a better solution {0} with cost: {1}".format(best_sol, self._get_cost(solution))
		self.S = np.where(best_sol == True)[0].tolist()
		self.total_cost = self._get_cost(best_sol)

	def _local_search(self, sol):
		# sol: [True, False, True...]
		best_sol_cost = self._get_cost(sol)
		best_sol = sol.copy()
		print "### local search ###"
		for i in range(len(sol)):
			sol_copy = sol.copy()
			sol_copy[i] = not sol_copy[i]
			A = self.A.copy()
			print "	best solution found so far {0} has cost: {1}".format(best_sol, self._get_cost(best_sol))
			print "	solution {0}: {1}".format(i, sol_copy)
			print "	A: {0}".format(A)
			self._ls_helper(sol_copy, A)
			if self._is_feasible(sol_copy, A):
				cost = self._get_cost(sol_copy)
				print "	solution {0} is feasible and has cost: {1}".format(sol_copy, cost)
				if cost < best_sol_cost:
					best_sol_cost = cost
					best_sol = sol_copy
		return best_sol

	def _ls_helper(self, solution, A):
		idx = np.where(solution == True)[0]
		A[:, idx] = 0

	def _greedy_randomized_construction(self, alpha):
		solution = np.zeros(self.n, dtype=bool)
		print "### greedy randomized construction ###"
		print "	solution: {0}".format(solution)
		while not self._is_feasible(solution, self.A_copy):
		# for i in range(3):
			# self._is_feasible(solution)
			rcl = self._get_rcl(alpha)
			print "	rlc: {0}".format(rcl)
			v = self._get_candidate(rcl)
			print "	chosen candidate: {0}".format(v)
			solution[v] = True
			self.c_copy[v] = 0
			print "	solution: {0}".format(solution)
			self._remove_intersection(v)
		return solution

	def _get_rcl(self, alpha):
		# card = np.sum(self.A_copy, axis=0).astype(float)
		cost = self.c_copy
		print "	cost: {0}".format(cost)
		n = self.A_copy.shape[1]
		return np.argsort(cost)[::-1][:alpha * n + 1]

	def _get_candidate(self, rlc):
		return random.choice(rlc)

	def _get_cost(self, sol):
		cost = np.sum(self.c[sol])
		return cost

	def _is_feasible(self, solution, A):
		idx = np.where(solution == False)[0]
		print "solution inside is_feasible: {0}".format(solution)
		res = np.sum(A[:, idx], axis=1)
		print "res inside is_feasible: {0}".format(res)
		return np.sum(res) == 0

	def _remove_intersection(self, sj):
		print "## remove intersection ##"
		print "	before: {0}".format(self.A_copy)
		p = self.A_copy[:, sj] > 0
		# para cada coluna (set) remova a intersecao
		# print "A = ", self.A_copy
		for j in range(self.n):
			self.A_copy[:, j][p] = 0
		print "	after: {0}".format(self.A_copy)

	def _get_collumn(self, col_idx):
		return np.nonzero(self.A_copy[:, col_idx] > 0)[0]

	def _get_universe(self):
		return set([i for i in range(self.m)])

	def get_solution_as_sets(self):
		return [self._get_set_by_index(sj) for sj in self.S]

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