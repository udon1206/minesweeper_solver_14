from ortools.sat.python.cp_model import (
    CpModel,
    IntVar,
    _NotBooleanVariable,
    BoundedLinearExpression,
)
from minesweeper_solver_14.util.add_or_expressions import add_or_expressions


def add_out_rule(
    model: CpModel, mines: list[list[IntVar]], rows: int, cols: int
) -> None:
    add_out_rule_1(model=model, mines=mines, rows=rows, cols=cols)
    add_out_rule_2(model=model, mines=mines, rows=rows, cols=cols)


# 安全なマスは連結していて、連結成分数は 1 である
def add_out_rule_1(
    model: CpModel, mines: list[list[IntVar]], rows: int, cols: int
) -> None:
    connect_labels = [
        [
            model.NewIntVar(0, rows * cols - 1, f"out1_connect_{r}_{c}")
            for c in range(cols)
        ]
        for r in range(rows)
    ]

    # 0 は 1 つだけという制約のためにいれる
    zero_labels = [
        [model.NewBoolVar(f"out1_zero_{r}_{c}") for c in range(cols)]
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
                            [mines[r][c].Not()],
                        ),
                        (
                            mines[i][j] == 0,
                            [mines[r][c].Not()],
                        ),
                    ]
                )
                exprs.append(
                    [
                        (
                            zero_labels[r][c] == 1,
                            [mines[r][c].Not()],
                        )
                    ]
                )
            add_or_expressions(model=model, exprs=exprs)


# 安全なマスは連結していて、連結成分数は 1 である
def add_out_rule_2(
    model: CpModel, mines: list[list[IntVar]], rows: int, cols: int
) -> None:
    connect_labels = [
        [
            model.NewIntVar(0, rows * cols - 1, f"out2_connect_2_{r}_{c}")
            for c in range(cols)
        ]
        for r in range(rows)
    ]

    zero_labels = [
        [model.NewBoolVar(f"out2_zero_2_{r}_{c}") for c in range(cols)]
        for r in range(rows)
    ]

    # 0 の場合は zero_labels が立つ
    for r in range(rows):
        for c in range(cols):
            model.Add(connect_labels[r][c] == 0).OnlyEnforceIf(zero_labels[r][c])
            model.Add(connect_labels[r][c] != 0).OnlyEnforceIf(zero_labels[r][c].Not())

    # 0 は、外と隣接している場合のみ
    for r in range(rows):
        for c in range(cols):
            if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                model.Add(zero_labels[r][c] == 1)
            else:
                model.Add(zero_labels[r][c] == 0)

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
