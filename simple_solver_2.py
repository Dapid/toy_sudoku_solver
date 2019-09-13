import numpy as np


def uncertainty(candidates, solution):
    return np.sum(solution == 0) + sum(len(x) for x in candidates.values())


def recursive_single_elimination(candidates, solution):
    prev_unc = uncertainty(candidates, solution)
    while True:
        for i in range(9):
            for j in range(9):
                if solution[i, j] > 0:
                    this_value = solution[i, j]
                    candidates[i, j] = set()

                    # Invalidate from row and columns:
                    for xx in range(9):
                        candidates[xx, j].discard(this_value)
                        candidates[i, xx].discard(this_value)

                    # Invalidate from block:
                    i_low, i_hi = 3 * (i // 3), 3 * (i // 3) + 3
                    j_low, j_hi = 3 * (j // 3), 3 * (j // 3) + 3
                    for xx in range(i_low, i_hi):
                        for yy in range(j_low, j_hi):
                            candidates[xx, yy].discard(this_value)
                else:
                    if len(candidates[i, j]) == 1:
                        solution[i, j] = candidates[i, j].pop()
        new_unc = uncertainty(candidates, solution)
        if prev_unc == new_unc:
            break
        prev_unc = new_unc


# pythran export solve_simple(int8[][])
def solve_simple(initial_board):
    candidates = {(i, j): set(range(1, 10)) for i in range(9) for j in range(9)}
    recursive_single_elimination(candidates, initial_board)
    return initial_board
