from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from minesweeper_solver_14.environment import Environment
from minesweeper_solver_14.solve_mine_sweeper14 import Result, solve_minesweeper14

app = FastAPI()


origins = ["http://127.0.0.1:5173", "http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/solve")
async def solve(environment: Environment) -> Result:
    return solve_minesweeper14(
        grid_array=environment.grid_array,
        all_mines_count=environment.all_mines_count,
        rule_grid=environment.rule_grid,
        is_quad=environment.is_quad,
        is_connect=environment.is_connect,
        is_triple=environment.is_triple,
        is_out=environment.is_out,
        is_dual=environment.is_dual,
        is_snake=environment.is_snake,
        is_balance=environment.is_balance,
    )
