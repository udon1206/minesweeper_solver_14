from ortools.sat.python.cp_model import CpModel, IntVar


# 一旦チェスボードの場合のみ対応
def add_multiple_rule(
    model: CpModel,
    mines: list[list[IntVar]],
    grid: list[list[int]],
    rule_grid: list[list[str]],
) -> None:
    rows = len(mines)
    cols = len(mines[0])
    for r in range(rows):
        for c in range(cols):
            if rule_grid[r][c] != "M":
                continue
            if grid[r][c] >= 0:
                dr = [-1, 0, 1, 0, 1, 1, -1, -1]
                dc = [0, 1, 0, -1, 1, -1, 1, -1]

                neighbors = [
                    mines[r + dr[i]][c + dc[i]]
                    * (1 if (r + dr[i] + c + dc[i]) % 2 == 0 else 2)
                    for i in range(8)
                    if 0 <= r + dr[i] < rows and 0 <= c + dc[i] < cols
                ]

                model.Add(sum(neighbors) == grid[r][c])
