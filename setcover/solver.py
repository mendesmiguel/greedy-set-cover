import numpy as np
import random
import logging


class VNDSolver(AbstractSolver):

	def _vnd(self, sol):
		logging.info("VND called")
		best_s = sol.copy()
		k = 0
		r = len(sol)
		A = self.A.copy()
		solutions = []
		while k < r:
			# logging.info("exploring k {0} neighborhood".format(k))
			s_cand = best_s.copy()
			s_cand[k] = not s_cand[k]
			if any((s_cand == e).all() for e in solutions):
				logging.info("solution already explored")
				k = k + 1
				continue
			s_cand = self._get_best_neighbor(s_cand)
			solutions.append(s_cand)
			if self._is_feasible(s_cand, A) and self._get_cost(s_cand) < self._get_cost(best_s):
				logging.info("VND found a better solution with cost: {0}".format(self._get_cost(s_cand)))
				best_s = s_cand.copy()
				k = 0
			else:
				k = k + 1
		return best_s

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
