from puzzle_solver import PuzzleSolver, run_puzzle_solver
from pprint import pprint
import re
import numpy as np


delimiter = "\n"


class DayPuzzleSolver(PuzzleSolver):
    def __init__(self, input_file, delimiter):
        PuzzleSolver.__init__(self, input_file, delimiter)

    def _get_instructions(self, raw_input):

        def get_range_from_string(string):
            return list(map(int, string.split(',')))

        instructions = []
        for instruction in raw_input:
            split = re.search(r'([a-z ]+)([0-9,]+)([a-z ]+)([0-9,]+)', instruction)
            instructions.append({
                "action": split.group(1).strip(),
                "start": get_range_from_string(split.group(2)),
                "end": get_range_from_string(split.group(4))
            })
        return instructions

    def _get_grid(self, dimensions, value):
        if value == True:
            return np.ones(dimensions, dtype=bool)
        if value == False:
            return np.zeros(dimensions, dtype=bool)
        if value == "0":
            return np.zeros(dimensions, dtype=int)

    def _get_resulting_grid(self, raw_input, default_value, execute_action):
        instructions = self._get_instructions(raw_input)
        grid = self._get_grid((1000, 1000), default_value)

        for instruction in instructions:
            action = instruction["action"]
            s1, s2 = instruction["start"]
            e1, e2 = list(map(lambda x: x + 1, instruction["end"]))

            grid[s1:e1, s2:e2] = execute_action(action, grid, s1, s2, e1, e2)

        return 1 * grid

    def solve_part_1(self, raw_input):

        def execute_action(action, grid, s1, s2, e1, e2):
            if action == "turn on":
                return self._get_grid((e1-s1, e2-s2), True)
            if action == "turn off":
                return self._get_grid((e1-s1, e2-s2), False)
            if action == "toggle":
                return ~grid[s1:e1, s2:e2]

        grid = self._get_resulting_grid(raw_input, False, execute_action)
        return grid.sum()

    def solve_part_2(self, raw_input):

        def execute_action(action, grid, s1, s2, e1, e2):
            if action == "turn off":
                result = -1 + grid[s1:e1, s2:e2]
                result[result < 0] = 0
                return result
            if action == "turn on":
                return 1 + grid[s1:e1, s2:e2]
            if action == "toggle":
                return 2 + grid[s1:e1, s2:e2]

        grid = self._get_resulting_grid(raw_input, "0", execute_action)
        return grid.sum()


if __name__ == '__main__':
    run_puzzle_solver(DayPuzzleSolver, delimiter)