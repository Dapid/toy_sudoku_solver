import numpy as np

from common import uncertainty, validate, is_solved
from simple_solver import recursive_single_elimination


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


# pythran export solve_lookahead(int8[][], bool)
# pythran export solve_lookahead(int8[][])
def solve_lookahead(initial_board, verbose=False):
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

        if verbose:
            print('Increasing from', len(possibilities), 'to', len(new_possibilities))

        valid_possibilities = []
        for p in new_possibilities:
            recursive_single_elimination(p[0], p[1])
            if validate(p[1]):
                valid_possibilities.append(p)

        if verbose:
            diff = len(new_possibilities) - len(valid_possibilities)
            if diff:
                print('Removed:', diff, 'invalid options')

        if any(is_solved(p[1]) for p in valid_possibilities):
            return [p[1] for p in valid_possibilities if is_solved(p[1])]
        possibilities = valid_possibilities

        if verbose:
            print('Length:', len(possibilities))


#pythran export solve_simple(int8[][])
def solve_simple(initial_board):
    candidates = {(i, j): set(range(1, 10)) for i in range(9) for j in range(9)}
    recursive_single_elimination(candidates, initial_board)
    return initial_board
