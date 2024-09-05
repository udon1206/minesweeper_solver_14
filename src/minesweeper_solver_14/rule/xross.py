from ortools.sat.python.cp_model import CpModel, IntVar


def add_xross_rule(
    model: CpModel,
    grid: list[list[int]],
    mines: list[list[IntVar]],
    rule_grid: list[list[str]],
) -> None:
    rows = len(grid)
    cols = len(grid[0])
    dr = [-2, -1, 0, 0, 0, 0, 0, 1, 2]
    dc = [0, 0, -2, -1, 0, 1, 2, 0, 0]
    for r in range(rows):
        for c in range(cols):
            if rule_grid[r][c] != "X":
                continue
            if grid[r][c] >= 0:  # -1 represents an unknown cell
                neighbors = [
                    mines[r + dr[i]][c + dc[i]]
                    for i in range(len(dr))
                    if 0 <= r + dr[i] < rows and 0 <= c + dc[i] < cols
                ]
                model.Add(sum(neighbors) == grid[r][c])
