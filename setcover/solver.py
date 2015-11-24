import numpy as np
import random
import logging

class TabuSearch(AbstractSearchStrategy):

	def solve(self, alpha, N):
		alpha = self.alpha
		N = self.N

		best_sol = np.ones(self.n, dtype=bool)
		logging.info("A shape: {0}".format(self.A.shape))
		logging.info("N iterations: {0}".format(N))
		logging.info("alpha: {0}".format(alpha))
		logging.info("RCL length: {0}".format(len(self._get_rcl(alpha))))
		for i in range(N):
			self.A_copy = self.A.copy()
			self.c_copy = self.c.copy()
			logging.info("iteration {0}:".format(i))
			solution = self._greedy_randomized_construction(alpha)
			logging.info("greedy construction generated solution with cost: {0}".format(self._get_cost(solution)))
			solution = self._tabu_search(solution)
			logging.info("tabu search generated solution with cost: {0}".format(self._get_cost(solution)))

			if self._get_cost(solution) < self._get_cost(best_sol): 
				best_sol = solution
			logging.info("best solution so far has cost:: {0}".format(self._get_cost(best_sol)))
		self.S = np.where(best_sol == True)[0].tolist()
		self.total_cost = self._get_cost(best_sol)

	def _tabu_search(self, sol):
		# logging.info("tabu search called")
		s_best = sol.copy()
		s = sol.copy()
		it = 0
		best_it = 0
		bt_max = 5
		tabu_list = []
		
		while (it - best_it) <= bt_max:
			it += 1
			logging.info("tabu search iteration {0}:".format(it))
			s_candidate = self._get_best_neighbor(s)
			logging.info("s_candidate cost: {0}".format(self._get_cost(s_candidate)))
			if any((s_candidate == e).all() for e in tabu_list) or \
				self._get_cost(s_candidate) >= self._get_cost(s):
				continue

			logging.info("adding solution with cost: {0} to tabu list".format(self._get_cost(s_candidate)))
			tabu_list.append(s_candidate)
			s = s_candidate

			if self._get_cost(s) < self._get_cost(s_best):
				s_best = s.copy()
				best_it = it
				logging.info("tabu search found a better solution with cost: {0}".format(self._get_cost(s_best)))
		return s_best

	def _get_best_neighbor(self, s):
		A = self.A.copy()
		best_s = s.copy()
		for i in range(len(s)):
			s_candidate = s.copy()
			s_candidate[i] = not s_candidate[i]

			if self._is_feasible(s_candidate, A) and self._get_cost(s_candidate) < self._get_cost(best_s):
				best_s = s_candidate.copy()
		return best_s

	def _ls_helper(self, solution, A):
		idx = np.where(solution == True)[0]
		A[:, idx] = 0
