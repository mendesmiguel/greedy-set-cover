from set_cover.solver import Solver
from file_handler.handler import FileHandler
import numpy as np

if __name__ == "__main__":


	# A = np.array([
	# 				[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 				[0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
	# 				[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
	# 				[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
	# 				[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1]
	# 				]).T

	# c = np.array([1, 1, 1, 1, 1]).astype(float)



	# A = np.array([
	# 				[1, 0, 0, 1, 1, 0, 0, 0, 0, 0],
	# 				[1, 0, 0, 1, 0, 1, 0, 0, 0, 0],
	# 				[0, 1, 0, 1, 0, 0, 1, 0, 0, 0],
	# 				[0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
	# 				[0, 0, 1, 1, 0, 0, 0, 0, 1, 0],
	# 				[0, 0, 1, 1, 0, 0, 0, 0, 0, 1]
	# 				])

	# c = np.array([3, 3, 3, 14, 1, 1, 1, 1, 1, 1]).astype(float)

	# A = np.array([
	# 				[1, 0, 1],
	# 				[0, 1, 1],
	# 				[1, 0, 1],
	# 				[1, 0, 1],
	# 				[0, 1, 0]
	# 				])

	# c = np.array([5, 10, 3]).astype(float)

	# # esse exemplo nao da otimo: 2
	# A = np.array([
	# 				[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 				[0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
	# 				[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
	# 				[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
	# 				[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1]
	# 				]).T

	# c = np.array([1, 1, 1, 1, 1]).astype(float)

	# # esse exemplo nao da otimo - otimo: 22
	# A = np.array([
	# 				[0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
	# 				[1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
	# 				[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
	# 				]).T

	# c = np.array([6, 15, 7]).astype(float)

	fh = FileHandler('datasets/scp41.txt')
	A, c = fh.process()


	s = Solver(A, c, "reactive_test")
	s.solve(N=2000, limit=50)
	s.print_solution()
	# print "solution as sets: {0}".format(s.get_solution_as_sets())
	# print "solution as matrix A: {0}".format(s.get_solution_as_matrix())