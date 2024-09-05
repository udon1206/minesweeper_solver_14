from ortools.sat.python.cp_model import CpModel, IntVar


def add_vanilla_rule(
    model: CpModel,
    grid: list[list[int]],
    mines: list[list[IntVar]],
    rule_grid: list[list[str]],
) -> None:

    rows = len(grid)
    cols = len(grid[0])
    for r in range(rows):
        for c in range(cols):
            if rule_grid[r][c] != "V":
                continue
            if grid[r][c] >= 0:  # -1 represents an unknown cell
                neighbors = [
                    mines[i][j]
                    for i in range(max(0, r - 1), min(rows, r + 2))
                    for j in range(max(0, c - 1), min(cols, c + 2))
                    if (i, j) != (r, c)
                ]
                model.Add(sum(neighbors) == grid[r][c])
