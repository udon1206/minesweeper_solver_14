from ortools.sat.python.cp_model import CpModel, IntVar


def add_triple_rule(model: CpModel, mines: list[list[IntVar]]) -> None:
    rows = len(mines)
    cols = len(mines[0])

    for r in range(rows):
        for c in range(cols):
            if c + 2 >= cols:
                break
            model.Add(mines[r][c] + mines[r][c + 1] + mines[r][c + 2] <= 2)

    for r in range(rows):
        for c in range(cols):
            if r + 2 >= rows:
                break
            model.Add(mines[r][c] + mines[r + 1][c] + mines[r + 2][c] <= 2)

    for r in range(rows):
        for c in range(cols):
            if r + 2 >= rows or c + 2 >= cols:
                break
            model.Add(mines[r][c] + mines[r + 1][c + 1] + mines[r + 2][c + 2] <= 2)
            model.Add(mines[r][c + 2] + mines[r + 1][c + 1] + mines[r + 2][c] <= 2)
