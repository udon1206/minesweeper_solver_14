from ortools.sat.python.cp_model import CpModel, IntVar


def add_quad_rule(model: CpModel, mines: list[list[IntVar]]) -> None:
    rows = len(mines)
    cols = len(mines[0])
    for r in range(rows - 1):
        for c in range(cols - 1):
            model.AddBoolOr(
                mines[r][c],
                mines[r + 1][c],
                mines[r][c + 1],
                mines[r + 1][c + 1],
            )
