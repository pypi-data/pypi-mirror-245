from copy import deepcopy
from typing import final

from pycubing.cube import Cube
from pycubing.error import ParityException
from pycubing.solver.solver3x3 import PIPELINE_3x3, solve_pll_edges
from pycubing.solver.solver2x2 import PIPELINE_2x2, orient_top_until_solve
from pycubing.utils import convert_3x3_moves_to_2x2, convert_3x3_moves_to_NxN
from pycubing.solver.solverNxN import PIPELINE_NxN, PIPELINE_NxN_3x3_STAGE, pll_parity

def solve(cube: Cube, mutate_original: bool = False) -> list[str]:
    if not mutate_original:
        cube = deepcopy(cube)
    match cube.N:
        case 1:
            return []
        case 2:
            cube_3x3 = cube.get_3x3()
            moves = convert_3x3_moves_to_2x2(PIPELINE_2x2(cube_3x3))
            if mutate_original:
                cube.parse(moves)
            moves += orient_top_until_solve(cube)
            return moves
        case 3:
            return PIPELINE_3x3(cube)
        case N:
            moves_to_3x3 = PIPELINE_NxN(cube)
            cube_3x3 = cube.get_3x3()
            moves_to_possible_parity = convert_3x3_moves_to_NxN(PIPELINE_NxN_3x3_STAGE(cube_3x3), N)
            cube.parse(moves_to_possible_parity)
            try:
                final_moves = convert_3x3_moves_to_NxN(solve_pll_edges(cube_3x3), N)
            except ParityException:
                final_moves = pll_parity(cube)
                final_moves += convert_3x3_moves_to_NxN(solve_pll_edges(cube.get_3x3()), N)
            if mutate_original:
                cube.parse(final_moves)
            return moves_to_3x3 + moves_to_possible_parity + final_moves
