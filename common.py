import numpy as np


def uncertainty(candidates, solution):
    return np.sum(solution == 0) + sum(len(x) for x in candidates.values())


def validate(solution):
    for i in range(9):
        if np.bincount(solution[i, :])[1:].max() > 1:
            return False
        if np.bincount(solution[:, i])[1:].max() > 1:
            return False
    for i in range(3):
        for j in range(3):
            i_low, i_hi = 3 * (i // 3), 3 * (i // 3) + 3
            j_low, j_hi = 3 * (j // 3), 3 * (j // 3) + 3
            if np.bincount(solution[i_low:i_hi, j_low:j_hi].ravel())[1:].max() > 1:
                return False
    return True


def is_solved(solution):
    return np.sum(solution == 0) == 0 and validate(solution)
