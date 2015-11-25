import numpy as np
import random
import logging
import abc

class AbstractSolver(object):
    __metaclass__ = abc.ABCMeta
    def __init__(self, A, c, problem_name, alpha, N):
        self.A = A
        self.c = c
        self.A_copy = A.copy()
        self.c_copy = c.copy()
        self.m, self.n = self.A_copy.shape
        self.total_cost = 0
        self.S = None
        self.problem_name = problem_name
        self.alpha = alpha
        self.N = N
        logging.basicConfig(filename=problem_name+'.log',
                            level=logging.DEBUG,
                            format='%(asctime)s %(message)s', 
                            datefmt='%m/%d/%Y %I:%M:%S %p')

    @abc.abstractmethod
    def solve(self):
         raise NotImplemented('AbstractSolver cannot be instantiated')

    def _greedy_randomized_construction(self, alpha):
        solution = np.zeros(self.n, dtype=bool)

        A = self.A.copy()
        while not self._is_feasible(solution, A):
            rcl = self._get_rcl(alpha)
            v = self._get_candidate(rcl)
            solution[v] = True
            self.c_copy[v] = 0
            self._remove_intersection(v)
        return solution

    def _get_rcl(self, alpha):
        card = np.sum(self.A_copy, axis=0).astype(float)
        cost = self.c.copy()
        factor = card / cost
        n = self.A_copy.shape[1]
        return np.argsort(factor)[::-1][:alpha * n + 1]

    def _get_candidate(self, rlc):
        return random.choice(rlc)

    def _get_cost(self, sol):
        cost = np.sum(self.c[sol])
        return cost

    def _is_feasible(self, solution, A):
        idx = np.where(solution == True)[0]
        res = np.sum(A[:, idx], axis=1)
        return not (0 in res)

    def _remove_intersection(self, sj):
        p = self.A_copy[:, sj] > 0

        for j in range(self.n):
            self.A_copy[:, j][p] = 0

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

    def print_total_cost(self):
        print self.get_total_cost()

    def print_solution(self):
        print "# original sets: "

        for j in range(self.n):
            print "S%d: %s -- cost: %.3f" % (j, self._get_set_by_index(j), self.c[j])
            logging.info("S%d: %s -- cost: %.3f" % (j, self._get_set_by_index(j), self.c[j]))
        print "# solution: "
        logging.info("# solution: ")

        for sj in self.S:
            print "S%d: %s" % (sj, self._get_set_by_index(sj))
            logging.info("S%d: %s" % (sj, self._get_set_by_index(sj)))
        print "Total cost: %.3f" % (self.total_cost)
        logging.info("Total cost: %.3f" % (self.total_cost))


    

class LocalSearchSolver(AbstractSolver):

    def solve(self):
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
            solution = self._local_search(solution)

            if self._get_cost(solution) < self._get_cost(best_sol): 
                best_sol = solution
            logging.info("best solution so far has cost:: {0}".format(self._get_cost(best_sol)))
        self.S = np.where(best_sol == True)[0].tolist()
        self.total_cost = self._get_cost(best_sol)

    def _local_search(self, sol):
        best_sol_cost = self._get_cost(sol)
        best_sol = sol.copy()

        for i in range(len(sol)):
            sol_copy = sol.copy()
            sol_copy[i] = not sol_copy[i]
            A = self.A.copy()

            if self._is_feasible(sol_copy, A):
                cost = self._get_cost(sol_copy)
                if cost < best_sol_cost:
                    logging.info("local search produced solution with cost: {0}".format(cost))
                    best_sol_cost = cost
                    best_sol = sol_copy
        return best_sol

    def _ls_helper(self, solution, A):
        idx = np.where(solution == True)[0]
        A[:, idx] = 0


class TabuSearchSolver(AbstractSolver):

    def solve(self):
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