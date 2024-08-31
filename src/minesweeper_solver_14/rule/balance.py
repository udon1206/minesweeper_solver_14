from ortools.sat.python.cp_model import (
    CpModel,
    IntVar,
)


def add_balance_rule(
    model: CpModel,
    mines: list[list[IntVar]],
    rows: int,
    cols: int,
    all_mines_count: int,
) -> None:
    print("add_balance_rule")
    one_line_mines_count = all_mines_count // rows
    for r in range(rows):
        model.Add(sum(mines[r]) == one_line_mines_count)
    for c in range(cols):
        model.Add(sum([mines[r][c] for r in range(rows)]) == one_line_mines_count)
