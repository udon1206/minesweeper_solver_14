from typing import Optional
from ortools.sat.python.cp_model import CpModel, IntVar


def add_lie_rule(
    model: CpModel,
    grid: list[list[int]],
    mines: list[list[IntVar]],
    confirm_mines: list[list[int]],
    all_mines_count: int,
    coffeences: Optional[list[list[int]]] = None,
) -> None:
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
                plus = model.NewBoolVar(f"plus_{r}_{c}")
                minus = model.NewBoolVar(f"minus_{r}_{c}")
                model.Add(sum(neighbors) == grid[r][c] + 1).OnlyEnforceIf(plus)
                model.Add(sum(neighbors) == grid[r][c] - 1).OnlyEnforceIf(minus)
                model.AddBoolOr(plus, minus)
            if confirm_mines[r][c] != -1:
                model.Add(mines[r][c] == confirm_mines[r][c])
    model.Add(sum(sum(row) for row in mines) == all_mines_count)
