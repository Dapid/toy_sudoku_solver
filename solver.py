# import copy
# import collections

import numpy as np


def uncertainty(candidates, solution):
    return np.sum(solution == 0) + sum(len(x) for x in candidates.values())


def recursive_single_elimination(candidates, solution):
    changed = True
    while changed:
        changed = False
        for i in range(9):
            for j in range(9):
                if solution[i, j] > 0:
                    this_value = solution[i, j]
                    candidates[i, j] = set()

                    # Invalidate from row and columns:
                    for xx in range(9):
                        if this_value in candidates[xx, j]:
                            candidates[xx, j].discard(this_value)
                            changed = True
                        if this_value in candidates[i, xx]:
                            candidates[i, xx].discard(this_value)
                            changed = True

                    # Invalidate from block:
                    i_low, i_hi = 3 * (i // 3), 3 * (i // 3) + 3
                    j_low, j_hi = 3 * (j // 3), 3 * (j // 3) + 3
                    for xx in range(i_low, i_hi):
                        for yy in range(j_low, j_hi):
                            if this_value in candidates[xx, yy]:
                                candidates[xx, yy].discard(this_value)
                                changed = True
                else:
                    if len(candidates[i, j]) == 1:
                        if solution[i, j] == 0:
                            solution[i, j] = candidates[i, j].pop()
                            changed = True


def recursive_single_elimination_alt(candidates, solution):
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


def single_elimination(candidates, solution):
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


def lookahead(candidates, solution):
    # pick one of the smallest candidates:
    ## Pythran doesn't like key to min :(
    # selected = min(((x, v) for x, v in candidates.items() if len(v) > 0), key=lambda x: len(x[1]))
    ## A full sort is unnecesary. And makes compilation take forever.
    # selected = sorted([(x, v) for x, v in candidates.items() if len(v) > 0], key=lambda x: len(x[1]))[0]

    # Rolling min manually
    selected_k = (0, 0)
    selected_v = candidates[(0, 0)]
    len_selected_v = 50
    for x, v in candidates.items():
        if 0 < len(v) < len_selected_v:
            selected_k = x
            selected_v = v
            len_selected_v = len(v)
    selected = (selected_k, selected_v)

    vector = []
    for value in selected[1]:
        this_candidate = {k: v.copy() for k, v in candidates.items()}
        # this_candidate = copy.deepcopy(candidates)
        this_candidate[selected[0]] = {value}
        vector.append((this_candidate, solution.copy()))

    return vector


# pythran export solve_lookahead(int8[][])
def solve_lookahead(initial_board):
    candidates = {(i, j): set(range(1, 10)) for i in range(9) for j in range(9)}
    possibilities = [(candidates, initial_board)]
    pp = possibilities[0]
    recursive_single_elimination(pp[0], pp[1])
    if is_solved(possibilities[0][1]):
        return possibilities[0][1]

    while True:
        new_possibilities = []
        for p in possibilities:
            new_possibilities.extend(lookahead(p[0], p[1]))
        valid_possibilities = []
        for p in new_possibilities:
            recursive_single_elimination(p[0], p[1])
            if validate(p[1]):
                valid_possibilities.append(p)
        if any(is_solved(p[1]) for p in valid_possibilities):
            return [p[1] for p in valid_possibilities if is_solved(p[1])]
        possibilities = valid_possibilities
        # print('Length:', len(possibilities))
