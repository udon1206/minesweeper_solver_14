from typing import Optional
from minesweeper_solver_14.environment import create_environment_from_json
from minesweeper_solver_14.judge_mine_sweeper_solve import judge_minesweeper_solve
from pathlib import Path


def solve_minesweeper14(
    grid: list[list[int]],
    all_mines_count: int,
    coffeences: Optional[list[list[int]]] = None,
    is_quad: bool = False,
    is_connect: bool = False,
    is_lie: bool = False,
    is_triple: bool = False,
) -> None:
    rows = len(grid)
    cols = len(grid[0])
    confirm_mines = [[-1 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != -1:
                confirm_mines[i][j] = 0
    while True:
        done = False
        confirm_zero = False
        for i in range(rows):
            for j in range(cols):
                if confirm_mines[i][j] != -1:
                    continue
                for val in range(2):
                    confirm_mines[i][j] = val
                    if not judge_minesweeper_solve(
                        grid,
                        confirm_mines,
                        all_mines_count,
                        is_quad,
                        is_connect,
                        coffeences,
                        is_lie,
                        is_triple,
                    ):
                        print(f"( {i + 1}, {chr(ord('A') + j)} ): {val ^ 1}")
                        confirm_mines[i][j] = val ^ 1
                        if confirm_mines[i][j] == 0:
                            confirm_zero = True
                        done = True
                        break
                if done:
                    break
                else:
                    confirm_mines[i][j] = -1
            if done:
                break
        if sum(confirm_mines, []).count(1) == all_mines_count:
            return
        if not done:
            print("Huu...")
            break
        if confirm_zero:
            print("Val: ", end="")
            val = int(input())
            grid[i][j] = val
    return


if __name__ == "__main__":
    input_path = Path(__file__).resolve().parent / "input" / "case.json"
    environment = create_environment_from_json(str(input_path))
    solve_minesweeper14(
        grid=environment.get_grid(),
        all_mines_count=environment.all_mines_count,
        coffeences=environment.coffeences,
        is_quad=environment.is_quad,
        is_connect=environment.is_connect,
        is_lie=environment.is_lie,
        is_triple=environment.is_triple,
    )
