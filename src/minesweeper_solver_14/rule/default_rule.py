from ortools.sat.python.cp_model import CpModel, IntVar


def add_default_rule(
    model: CpModel,
    grid: list[list[int]],
    mines: list[list[IntVar]],
    confirm_mines: list[list[int]],
    all_mines_count: int,
) -> None:
    rows = len(grid)
    cols = len(grid[0])
    for r in range(rows):
        for c in range(cols):
            if confirm_mines[r][c] != -1:
                model.Add(mines[r][c] == confirm_mines[r][c])
    model.Add(sum(sum(row) for row in mines) == all_mines_count)
