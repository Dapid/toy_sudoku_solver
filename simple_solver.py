
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

#pythran export solve_simple(int8[][])
def solve_simple(initial_board):
    candidates = {(i, j): set(range(1, 10)) for i in range(9) for j in range(9)}
    recursive_single_elimination(candidates, initial_board)
    return initial_board