from typing import Optional
from ortools.sat.python import cp_model
from minesweeper_solver_14.rule.default_rule import add_default_rule
from minesweeper_solver_14.rule.lie import add_lie_rule
from minesweeper_solver_14.rule.quad import add_quad_rule
from minesweeper_solver_14.rule.triple import add_triple_rule
from minesweeper_solver_14.rule.connect import add_connect_rule
from minesweeper_solver_14.rule.out import add_out_rule
from minesweeper_solver_14.rule.dual import add_dual_rule


def judge_minesweeper_solve(
    grid: list[list[int]],
    confirm_mines: list[list[int]],
    all_mines_count: int,
    is_quad: bool = False,
    is_connect: bool = False,
    coffeences: Optional[list[list[int]]] = None,
    is_lie: bool = False,
    is_triple: bool = False,
    is_out: bool = False,
    is_dual: bool = False,
) -> bool:
    # Get the dimensions of the grid
    rows = len(grid)
    cols = len(grid[0])

    # Create the model
    model = cp_model.CpModel()

    # Create a matrix of Boolean variables for mine placement
    mines = [
        [model.NewBoolVar(f"mine_{r}_{c}") for c in range(cols)] for r in range(rows)
    ]
    if is_lie:
        add_lie_rule(model, grid, mines, confirm_mines, all_mines_count)
    else:
        add_default_rule(model, grid, mines, confirm_mines, all_mines_count, coffeences)
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
    # Create the solver and solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    # Output the solution
    return str(status) == str(cp_model.FEASIBLE) or str(status) == str(cp_model.OPTIMAL)
