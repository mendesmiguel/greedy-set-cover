import numpy as np
import random
import logging
import abc
import signal
class TimeoutException(Exception):   # Custom exception class
    pass

def TimeoutHandler(signum, frame):   # Custom signal handler
    raise TimeoutException

class GRASPSolver(object):
    def __init__(self, A, c, problem_name, alpha, N, SearchStrategy):
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
        self.best_sol = None
        self.search_strategy = SearchStrategy(self)
        logging.basicConfig(filename=problem_name+'.log',
                            level=logging.DEBUG,
                            format='%(asctime)s %(message)s', 
                            datefmt='%m/%d/%Y %I:%M:%S %p')

    def solve(self):
            alpha = self.alpha
            N = self.N

            best_sol = np.ones(self.n, dtype=bool)
            logging.info("A shape: {0}".format(self.A.shape))
            logging.info("N iterations: {0}".format(N))
            logging.info("alpha: {0}".format(alpha))
            logging.info("RCL length: {0}".format(len(self._get_rcl(alpha))))
            i = 0
            signal.signal(signal.SIGALRM,TimeoutHandler)
            signal.alarm(N)
            logging.info("solver will stop after {0} seconds".format(N))

            try:    
                while True:
                # for i in range(N):
                    self.A_copy = self.A.copy()
                    self.c_copy = self.c.copy()
                    logging.info("iteration {0}:".format(i))
                    solution = self._greedy_randomized_construction(alpha)
                    logging.info("greedy construction generated solution with cost: {0}".format(self.get_cost(solution)))
                    self.update_solution(solution)
                    solution = self.search_strategy.search(solution)

                    if self.get_cost(solution) < self.get_cost(best_sol): 
                        best_sol = solution
                        self.update_solution(solution)
                    logging.info("best solution so far has cost:: {0}".format(self.get_cost(best_sol)))
                    i += 1
            except TimeoutException:
                self.S = np.where(self.best_sol == True)[0].tolist()
                self.total_cost = self.get_cost(self.best_sol)
                logging.info("solver completed")
            logging.info("best solution found has cost: {0}".format(self.total_cost))

    def _greedy_randomized_construction(self, alpha):
        solution = np.zeros(self.n, dtype=bool)

        A = self.A.copy()
        while not self.is_feasible(solution, A):
            rcl = self._get_rcl(alpha)
            v = self._get_candidate(rcl)
            solution[v] = True
            self.c_copy[v] = 0
            self._remove_intersection(v)
        return solution

    def is_feasible(self, solution, A):
        idx = np.where(solution == True)[0]
        res = np.sum(A[:, idx], axis=1)
        return not (0 in res)

    def update_solution(self, new_sol):
        if self.best_sol is None or self.get_cost(new_sol) < self.get_cost(self.best_sol):
            logging.info("best solution found updated has cost of {0}".format(self.get_cost(new_sol)))
            logging.info("the old solution had cost of {0}".format(self.get_cost(self.best_sol)))
            self.best_sol = new_sol.copy()

    def _get_rcl(self, alpha):
        card = np.sum(self.A_copy, axis=0).astype(float)
        cost = self.c.copy()
        factor = card / cost
        n = self.A_copy.shape[1]
        return np.argsort(factor)[::-1][:alpha * n + 1]

    def _get_candidate(self, rlc):
        return random.choice(rlc)

    def get_cost(self, sol):
        cost = np.sum(self.c[sol])
        return cost

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


class AbstractSearch(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, solver):
        self.A = solver.A
        self.solver = solver

    def _get_best_neighbor(self, s):
        A = self.A.copy()
        best_s = s.copy()
        for i in range(len(s)):
            s_candidate = s.copy()
            s_candidate[i] = not s_candidate[i]

            if self.solver.is_feasible(s_candidate, A) and self.solver.get_cost(s_candidate) < self.solver.get_cost(best_s):
                best_s = s_candidate.copy()
        return best_s
        
class LocalSearch(AbstractSearch):
    def search(self, sol):
        best_sol_cost = self.solver.get_cost(sol)
        best_sol = sol.copy()

        for i in range(len(sol)):
            sol_copy = sol.copy()
            sol_copy[i] = not sol_copy[i]
            A = self.A.copy()

            if self.solver.is_feasible(sol_copy, A):
                cost = self.solver.get_cost(sol_copy)
                if cost < best_sol_cost:
                    logging.info("local search produced solution with cost: {0}".format(cost))
                    self.solver.update_solution(sol_copy)
                    best_sol_cost = cost
                    best_sol = sol_copy
        return best_sol

class TabuSearch(AbstractSearch):
    def search(self, sol):
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
            logging.info("s_candidate cost: {0}".format(self.solver.get_cost(s_candidate)))
            if any((s_candidate == e).all() for e in tabu_list) or \
                self.solver.get_cost(s_candidate) >= self.solver.get_cost(s):
                continue

            logging.info("adding solution with cost: {0} to tabu list".format(self.solver.get_cost(s_candidate)))
            tabu_list.append(s_candidate)
            s = s_candidate

            if self.solver.get_cost(s) < self.solver.get_cost(s_best):
                s_best = s.copy()
                best_it = it
                self.solver.update_solution(s_best)
                logging.info("tabu search found a better solution with cost: {0}".format(self.solver.get_cost(s_best)))
        return s_best


class VNDSearch(AbstractSearch):
    def search(self, sol):
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
            if self.solver.is_feasible(s_cand, A) and self.solver.get_cost(s_cand) < self.solver.get_cost(best_s):
                self.solver.update_solution(s_cand)
                logging.info("VND found a better solution with cost: {0}".format(self.solver.get_cost(s_cand)))
                best_s = s_cand.copy()
                k = 0
            else:
                k = k + 1
        return best_s

class GreedySolver(object):

    def __init__(self, A, c, problem_name):
        self.A_copy = A.copy()
        self.A = A
        self.c = c
        self.m, self.n = self.A_copy.shape
        self.total_cost = 0
        self.U = None
        self.S = []
        logging.basicConfig(filename=problem_name+'.log',
                            level=logging.DEBUG,
                            format='%(asctime)s %(message)s', 
                            datefmt='%m/%d/%Y %I:%M:%S %p')

    def solve(self):
        m, n = self.m, self.n

        C = set()
        self.U = self.__get_universe()
        cj = self.c

        iteration = 0
        logging.info("U: {0}".format(self.U))
        logging.info("cost array c: %s" % (self.c))
        while C != self.U:
            sj, max_ratio = self.__best_set()
            self.S.append(sj)
            elem = np.nonzero(self.A[:, sj] > 0)[0].tolist()
            C = C.union(elem)
            self.__remove_intersection(sj)  
            self.total_cost += cj[sj]
            iteration += 1
            logging.info("# iteration %d: " % (iteration))
            logging.info("Best set found: %d - ratio: %.3f" % (sj, max_ratio))
            logging.info("Sets added to the solution so far: %s" % (self.S))
            logging.info("C: {0}".format(C))
        logging.info("DONE!")

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
            pj = np.nonzero(self.A_copy[:, j] > 0)[0]
            # se |pj| / cj > max_ratio entao guarde o indice
            if len(pj) / cj > max_ratio:
                max_ratio = len(pj) / cj
                sj = j
        return sj, max_ratio

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
        # print "# universe: %s" % (self.U)
        # print "# original sets: "
        # for j in range(self.n):
        #     print "S%d: %s -- cost: %.3f" % (j, self.__get_set_by_index(j), self.c[j])

        # print "# solution: "
        # for sj in self.S:
        #     print "S%d: %s" % (sj, self.__get_set_by_index(sj))

        print "Total cost: %.3f" % (self.total_cost)