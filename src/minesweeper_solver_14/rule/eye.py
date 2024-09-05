from ortools.sat.python.cp_model import CpModel, IntVar

from minesweeper_solver_14.util.add_or_expressions import add_or_expressions


def add_eye_rule(
    model: CpModel,
    mines: list[list[IntVar]],
    grid: list[list[int]],
    rows: int,
    cols: int,
    rule_grid: list[list[str]],
) -> None:
    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]
    for r in range(rows):
        for c in range(cols):
            if rule_grid[r][c] != "E":
                continue
            if grid[r][c] < 0:
                continue
            neighbors = []
            for a in range(grid[r][c]):
                if not (0 <= r + dr[0] * a < rows and 0 <= c + dc[0] * a < cols):
                    continue
                for b in range(grid[r][c] - a):
                    if not (0 <= r + dr[1] * b < rows and 0 <= c + dc[1] * b < cols):
                        continue
                    for cc in range(grid[r][c] - a - b):
                        if not (
                            0 <= r + dr[2] * cc < rows and 0 <= c + dc[2] * cc < cols
                        ):
                            continue
                        d = grid[r][c] - 1 - a - b - cc
                        if not (
                            0 <= r + dr[3] * d < rows and 0 <= c + dc[3] * d < cols
                        ):
                            continue
                        zeros = [
                            mines[r + dr[i] * j][c + dc[i] * j]
                            for i in range(4)
                            for j in range([a + 1, b + 1, cc + 1, d + 1][i])
                        ]
                        ones = [
                            mines[r + dr[i] * cof][c + dc[i] * cof]
                            for i, cof in enumerate([a + 1, b + 1, cc + 1, d + 1])
                            if 0 <= r + dr[i] * cof < rows
                            and 0 <= c + dc[i] * cof < cols
                        ]
                        neighbors.append((ones, zeros))
            add_or_expressions(
                model=model,
                exprs=[
                    [
                        (sum(ones) == len(ones), []),
                        (sum(zeros) == 0, []),
                    ]
                    for ones, zeros in neighbors
                ],
            )
