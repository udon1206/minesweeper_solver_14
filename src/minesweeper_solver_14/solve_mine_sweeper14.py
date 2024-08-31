from typing import Optional

from pydantic import BaseModel

from minesweeper_solver_14.judge_mine_sweeper_solve import judge_minesweeper_solve


class Status(BaseModel):
    r: int
    c: int
    flag: bool


class Result(BaseModel):
    is_feasible: bool
    finished: bool
    result: list[Status]


def solve_minesweeper14(
    grid: list[list[int]],
    all_mines_count: int,
    coffeences: Optional[list[list[int]]] = None,
    is_quad: bool = False,
    is_connect: bool = False,
    is_lie: bool = False,
    is_triple: bool = False,
    is_out: bool = False,
) -> Result:
    rows = len(grid)
    cols = len(grid[0])
    confirm_mines = [[-1 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == -3:
                confirm_mines[i][j] = 1
            elif grid[i][j] != -1:
                confirm_mines[i][j] = 0

    result = Result(is_feasible=True, result=[], finished=False)

    done = False
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
                    is_out,
                ):
                    result.result.append(Status(r=i, c=j, flag=bool(val ^ 1)))
                    confirm_mines[i][j] = val ^ 1
                    done = True
                    break
                else:
                    confirm_mines[i][j] = -1

    if sum(confirm_mines, []).count(1) == all_mines_count:
        result.finished = True

    if not done:
        result.is_feasible = False

    return result
