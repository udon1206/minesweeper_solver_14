from ortools.sat.python.cp_model import (
    CpModel,
    IntVar,
    _NotBooleanVariable,
    BoundedLinearExpression,
)
from minesweeper_solver_14.util.add_or_expressions import add_or_expressions


def add_snake_rule(
    model: CpModel, mines: list[list[IntVar]], rows: int, cols: int
) -> None:
    add_snake_rule_1(model=model, mines=mines, rows=rows, cols=cols)
    add_snake_rule_2(model=model, mines=mines, rows=rows, cols=cols)


# 爆弾マスは連結していて、連結成分数は 1 である
def add_snake_rule_1(
    model: CpModel, mines: list[list[IntVar]], rows: int, cols: int
) -> None:
    connect_labels = [
        [
            model.NewIntVar(0, rows * cols - 1, f"snake1_connect_{r}_{c}")
            for c in range(cols)
        ]
        for r in range(rows)
    ]

    # 0 は 1 つだけという制約のためにいれる
    zero_labels = [
        [model.NewBoolVar(f"snake1_zero_{r}_{c}") for c in range(cols)]
        for r in range(rows)
    ]

    # 0 の場合は zero_labels が立つ
    for r in range(rows):
        for c in range(cols):
            model.Add(connect_labels[r][c] == 0).OnlyEnforceIf(zero_labels[r][c])
            model.Add(connect_labels[r][c] != 0).OnlyEnforceIf(zero_labels[r][c].Not())

    # 0 は 1 つだけ
    model.Add(sum(sum(row) for row in zero_labels) == 1)

    neighbors: dict[tuple[int, int], list[tuple[int, int]]] = {}
    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]
    for r in range(rows):
        for c in range(cols):
            neighbors[(r, c)] = [
                (r + dr[i], c + dc[i])
                for i in range(4)
                if 0 <= r + dr[i] < rows and 0 <= c + dc[i] < cols
            ]

    for r in range(rows):
        for c in range(cols):
            exprs: list[
                list[
                    tuple[
                        BoundedLinearExpression | bool,
                        list[IntVar | _NotBooleanVariable],
                    ]
                ]
            ] = []
            for i, j in neighbors[(r, c)]:
                exprs.append(
                    [
                        (
                            connect_labels[r][c] > connect_labels[i][j],
                            [mines[r][c]],
                        ),
                        (
                            mines[i][j] == 1,
                            [mines[r][c]],
                        ),
                    ]
                )
                exprs.append(
                    [
                        (
                            zero_labels[r][c] == 1,
                            [mines[r][c]],
                        )
                    ]
                )
            add_or_expressions(model=model, exprs=exprs)


def add_snake_rule_2(
    model: CpModel, mines: list[list[IntVar]], rows: int, cols: int
) -> None:
    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]
    deg_one_labels = [
        [model.NewBoolVar(f"deg_one_label_{r}_{c}") for c in range(cols)]
        for r in range(rows)
    ]
    for r in range(rows):
        for c in range(cols):
            mines_list = [
                mines[r + dr[i]][c + dc[i]]
                for i in range(4)
                if 0 <= r + dr[i] < rows and 0 <= c + dc[i] < cols
            ]
            model.Add(sum(mines_list) <= 2).OnlyEnforceIf(mines[r][c])
            model.Add(sum(mines_list) == 1).OnlyEnforceIf(deg_one_labels[r][c])
            model.Add(sum(mines_list) != 1).OnlyEnforceIf(deg_one_labels[r][c].Not())
