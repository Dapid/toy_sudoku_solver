import solver
import numpy as np


if __name__ == '__main__':
    solution = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
                [6, 0, 0, 1, 9, 5, 0, 0, 0],
                [0, 9, 8, 0, 0, 0, 0, 6, 0],
                [8, 0, 0, 0, 6, 0, 0, 0, 3],
                [4, 0, 0, 8, 0, 3, 0, 0, 1],
                [7, 0, 0, 0, 2, 0, 0, 0, 6],
                [0, 6, 0, 0, 0, 0, 2, 8, 0],
                [0, 0, 0, 4, 1, 9, 0, 0, 5],
                [0, 0, 0, 0, 8, 0, 0, 7, 9]]

    solution = [[1, 0, 0, 0, 0, 7, 0, 9, 0],
                [0, 3, 0, 0, 2, 0, 0, 0, 8],
                [0, 0, 9, 6, 0, 0, 5, 0, 0],

                [0, 0, 5, 3, 0, 0, 9, 0, 0],
                [0, 1, 0, 0, 8, 0, 0, 0, 2],
                [6, 0, 0, 0, 0, 4, 0, 0, 0],

                [3, 0, 0, 0, 0, 0, 0, 1, 0],
                [0, 4, 1, 0, 0, 0, 0, 0, 7],
                [0, 0, 7, 0, 0, 0, 3, 0, 0]]

    solution = np.array(solution, dtype=np.int8)

    solutions = solver.solve_lookahead(solution)
    print(len(solutions))

