"""
A script to solve Sudoku puzzles. The puzzles must be hard coded for now. WIP
"""
import copy

starting_grid = [
    [6, 0, 1, 4, 7, 8, 0, 2, 9],
    [0, 0, 8, 5, 0, 1, 0, 0, 4],
    [5, 4, 0, 0, 0, 6, 0, 0, 1],
    [3, 0, 4, 1, 5, 2, 8, 9, 6],
    [1, 6, 0, 0, 4, 0, 0, 5, 0],
    [8, 0, 0, 7, 0, 0, 0, 0, 0],
    [0, 1, 3, 0, 8, 0, 9, 0, 0],
    [9, 0, 6, 0, 0, 7, 0, 0, 0],
    [7, 0, 2, 3, 0, 0, 0, 1, 5]
]

grid = copy.deepcopy(starting_grid)


def print_sudoku_grid():
    for line in grid:
        print(line)


def possible(x, y, n):
    """Returns True if it is possible to place the digit n at position (x, y) on the grid"""
    for i in range(0, 9):
        if grid[y][i] == n or grid[i][x] == n:
            return False
    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    for i in range(0, 3):
        for j in range(0, 3):
            if grid[y0 + i][x0 + j] == n:
                return False
    return True
