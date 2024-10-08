from ortools.sat.python import cp_model
from minesweeper_solver_14.rule.default_rule import add_default_rule
from minesweeper_solver_14.rule.lie import add_lie_rule
from minesweeper_solver_14.rule.quad import add_quad_rule
from minesweeper_solver_14.rule.triple import add_triple_rule
from minesweeper_solver_14.rule.connect import add_connect_rule
from minesweeper_solver_14.rule.out import add_out_rule
from minesweeper_solver_14.rule.dual import add_dual_rule
from minesweeper_solver_14.rule.snake import add_snake_rule
from minesweeper_solver_14.rule.balance import add_balance_rule
from minesweeper_solver_14.rule.wall import add_wall_rule
from minesweeper_solver_14.rule.neutral import add_neutral_rule
from minesweeper_solver_14.rule.vanilla import add_vanilla_rule
from minesweeper_solver_14.rule.xross import add_xross_rule
from minesweeper_solver_14.rule.partial import add_partial_rule
from minesweeper_solver_14.rule.eye import add_eye_rule
from minesweeper_solver_14.rule.multiple import add_multiple_rule


def judge_minesweeper_solve(
    grid_array: list[list[list[int]]],
    confirm_mines: list[list[int]],
    all_mines_count: int,
    rule_grid: list[list[str]],
    is_quad: bool = False,
    is_connect: bool = False,
    is_triple: bool = False,
    is_out: bool = False,
    is_dual: bool = False,
    is_snake: bool = False,
    is_balance: bool = False,
) -> bool:
    grid = [[sum(row) for row in grid] for grid in grid_array]
    # Get the dimensions of the grid
    rows = len(grid)
    cols = len(grid[0])

    # Create the model
    model = cp_model.CpModel()

    # Create a matrix of Boolean variables for mine placement
    mines = [
        [model.NewBoolVar(f"mine_{r}_{c}") for c in range(cols)] for r in range(rows)
    ]

    add_default_rule(model, grid, mines, confirm_mines, all_mines_count)

    add_lie_rule(model, grid, mines, rule_grid)
    add_neutral_rule(model, mines, grid, rule_grid)
    add_xross_rule(model, grid, mines, rule_grid)
    add_partial_rule(model, mines, grid, rows, cols, rule_grid)
    add_eye_rule(model, mines, grid, rows, cols, rule_grid)
    add_wall_rule(model, mines, grid_array, rows, cols, rule_grid)
    add_multiple_rule(model, mines, grid, rule_grid)
    add_vanilla_rule(model, grid, mines, rule_grid)

    if is_quad:
        add_quad_rule(model, mines)
    if is_connect:
        add_connect_rule(model, mines, rows, cols)
    if is_triple:
        add_triple_rule(model, mines)
    if is_out:
        add_out_rule(model, mines, rows, cols)
    if is_dual:
        add_dual_rule(model, mines, rows, cols)
    if is_snake:
        add_snake_rule(model, mines, rows, cols)
    if is_balance:
        add_balance_rule(model, mines, rows, cols, all_mines_count)

    # Create the solver and solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Output the solution
    return str(status) == str(cp_model.FEASIBLE) or str(status) == str(cp_model.OPTIMAL)
