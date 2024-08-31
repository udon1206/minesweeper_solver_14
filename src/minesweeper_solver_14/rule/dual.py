from ortools.sat.python.cp_model import (
    CpModel,
    IntVar,
)


def add_dual_rule(
    model: CpModel, mines: list[list[IntVar]], rows: int, cols: int
) -> None:
    print("add_dual_rule")
    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]
    for r in range(rows):
        for c in range(cols):
            mines_list = [
                mines[r + dr[i]][c + dc[i]]
                for i in range(4)
                if 0 <= r + dr[i] < rows and 0 <= c + dc[i] < cols
            ]
            model.Add(sum(mines_list) == 1).OnlyEnforceIf(mines[r][c])
