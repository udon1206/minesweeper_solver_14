from ortools.sat.python.cp_model import CpModel, IntVar

from minesweeper_solver_14.util.add_or_expressions import add_or_expressions


# 一旦チェスボードの場合のみ対応
def add_neutral_rule(
    model: CpModel,
    mines: list[list[IntVar]],
    grid: list[list[int]],
    rule_grid: list[list[str]],
) -> None:
    rows = len(mines)
    cols = len(mines[0])
    for r in range(rows):
        for c in range(cols):
            if rule_grid[r][c] != "N":
                continue
            if grid[r][c] >= 0:
                dr1 = [-1, -1, 1, 1]
                dc1 = [-1, 1, 1, -1]

                dr2 = [-1, 0, 1, 0]
                dc2 = [0, 1, 0, -1]

                neighbors1 = [
                    mines[r + dr1[i]][c + dc1[i]]
                    for i in range(4)
                    if 0 <= r + dr1[i] < rows and 0 <= c + dc1[i] < cols
                ]
                neighbors2 = [
                    mines[r + dr2[i]][c + dc2[i]]
                    for i in range(4)
                    if 0 <= r + dr2[i] < rows and 0 <= c + dc2[i] < cols
                ]
                add_or_expressions(
                    model,
                    [
                        [
                            (sum(neighbors1) - sum(neighbors2) == grid[r][c], []),
                        ],
                        [
                            (sum(neighbors2) - sum(neighbors1) == grid[r][c], []),
                        ],
                    ],
                )
