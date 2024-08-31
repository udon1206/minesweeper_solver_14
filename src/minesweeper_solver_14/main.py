from minesweeper_solver_14.environment import create_environment_from_json
from pathlib import Path

from minesweeper_solver_14.solve_mine_sweeper14 import solve_minesweeper14

if __name__ == "__main__":
    input_path = Path(__file__).resolve().parent / "input" / "case.json"
    environment = create_environment_from_json(str(input_path))
    result = solve_minesweeper14(
        grid=environment.get_grid(),
        all_mines_count=environment.all_mines_count,
        coffeences=environment.coffeences,
        is_quad=environment.is_quad,
        is_connect=environment.is_connect,
        is_lie=environment.is_lie,
        is_triple=environment.is_triple,
    )
    print(result)
