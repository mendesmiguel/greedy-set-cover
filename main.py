#!/usr/bin/python
from setcover.solver import GRASPSolver, LocalSearch, TabuSearch, VNDSearch
from filehandler.handler import FileHandler
import numpy as np
import sys

if __name__ == "__main__":


    # A = np.array([
    #               [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #               [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    #               [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    #               [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    #               [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1]
    #               ]).T

    # c = np.array([1, 1, 1, 1, 1]).astype(float)



    # A = np.array([
    #               [1, 0, 0, 1, 1, 0, 0, 0, 0, 0],
    #               [1, 0, 0, 1, 0, 1, 0, 0, 0, 0],
    #               [0, 1, 0, 1, 0, 0, 1, 0, 0, 0],
    #               [0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
    #               [0, 0, 1, 1, 0, 0, 0, 0, 1, 0],
    #               [0, 0, 1, 1, 0, 0, 0, 0, 0, 1]
    #               ])

    # c = np.array([3, 3, 3, 14, 1, 1, 1, 1, 1, 1]).astype(float)

    # A = np.array([
    #               [1, 0, 1],
    #               [0, 1, 1],
    #               [1, 0, 1],
    #               [1, 0, 1],
    #               [0, 1, 0]
    #               ])

    # c = np.array([5, 10, 3]).astype(float)

    # # esse exemplo nao da otimo: 2
    # A = np.array([
    #               [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #               [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    #               [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    #               [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    #               [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1]
    #               ]).T

    # c = np.array([1, 1, 1, 1, 1]).astype(float)

    # # esse exemplo nao da otimo - otimo: 22
    # A = np.array([
    #               [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    #               [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    #               [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
    #               ]).T

    # c = np.array([6, 15, 7]).astype(float)

    total = len(sys.argv)
    if total != 6:
        print "Usage: ./main.py [dataset] [logfilename] [alpha] [num of seconds] [search strategy]" 
        # print "Given: ", sys.argv
    else:
        # print "Given: ", sys.argv
        dataset, logfile, alpha, N, SearchStrategy = sys.argv[1:]
        fh = FileHandler(dataset)
        A, c = fh.process()
        s = GRASPSolver(A, c, "logs/" + logfile, float(alpha), int(N), eval(SearchStrategy))
        s.solve()
        s.print_total_cost()
        # print "solution as sets: {0}".format(s.get_solution_as_sets())
    # print "solution as matrix A: {0}".format(s.get_solution_as_matrix())