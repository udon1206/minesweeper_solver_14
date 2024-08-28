from ortools.sat.python.cp_model import CpModel, IntVar


# 参考: https://qiita.com/semiexp/items/f38d015c55195186d267
# 天才すぎる
def add_connect_rule(
    model: CpModel, mines: list[list[IntVar]], rows: int, cols: int
) -> None:
    connect_labels = [
        [model.NewIntVar(0, rows * cols - 1, f"connect_{r}_{c}") for c in range(cols)]
        for r in range(rows)
    ]

    # 0 は 1 つだけという制約のためにいれる
    zero_labels = [
        [model.NewBoolVar(f"zero_{r}_{c}") for c in range(cols)] for r in range(rows)
    ]

    # 0 の場合は zero_labels が立つ
    for r in range(rows):
        for c in range(cols):
            model.Add(connect_labels[r][c] == 0).OnlyEnforceIf(zero_labels[r][c])
            model.Add(connect_labels[r][c] != 0).OnlyEnforceIf(zero_labels[r][c].Not())

    # 0 は 1 つだけ
    model.Add(sum(sum(row) for row in zero_labels) == 1)

    neighbors: dict[tuple[int, int], list[tuple[int, int]]] = {}
    for r in range(rows):
        for c in range(cols):
            neighbors[(r, c)] = [
                (i, j)
                for i in range(max(0, r - 1), min(rows, r + 2))
                for j in range(max(0, c - 1), min(cols, c + 2))
                if (i, j) != (r, c)
            ]

    less_labels = [
        [
            [model.NewBoolVar(f"less_{r}_{c}_{i}_{j}") for (i, j) in neighbors[(r, c)]]
            for c in range(cols)
        ]
        for r in range(rows)
    ]

    for r in range(rows):
        for c in range(cols):
            for (i, j), less_label in zip(neighbors[(r, c)], less_labels[r][c]):
                model.Add((connect_labels[r][c] > connect_labels[i][j])).OnlyEnforceIf(
                    less_label
                )
                model.Add(mines[i][j] == 1).OnlyEnforceIf(less_label)
            model.AddBoolOr(zero_labels[r][c], *less_labels[r][c], mines[r][c].Not())
