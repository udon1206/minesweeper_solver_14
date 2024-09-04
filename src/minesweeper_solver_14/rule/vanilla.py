from typing import Optional
from ortools.sat.python.cp_model import CpModel, IntVar


def add_vanilla_rule(
    model: CpModel,
    grid: list[list[int]],
    mines: list[list[IntVar]],
    coffeences: Optional[list[list[int]]] = None,
) -> None:
    if coffeences is None:
        coffeences = [[1 for _ in range(len(grid[0]))] for _ in range(len(grid))]

    rows = len(grid)
    cols = len(grid[0])
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] >= 0:  # -1 represents an unknown cell
                neighbors = [
                    mines[i][j] * coffeences[i][j]
                    for i in range(max(0, r - 1), min(rows, r + 2))
                    for j in range(max(0, c - 1), min(cols, c + 2))
                    if (i, j) != (r, c)
                ]
                model.Add(sum(neighbors) == grid[r][c])
