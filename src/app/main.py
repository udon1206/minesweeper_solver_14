from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from minesweeper_solver_14.environment import Environment
from minesweeper_solver_14.solve_mine_sweeper14 import Result, solve_minesweeper14

app = FastAPI()


origins = [
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    price: float
    tax: Union[float, None] = None


@app.post("/solve")
async def solve(environment: Environment) -> Result:
    return solve_minesweeper14(
        grid=environment.get_grid(),
        all_mines_count=environment.all_mines_count,
        coffeences=environment.coffeences,
        is_quad=environment.is_quad,
        is_connect=environment.is_connect,
        is_lie=environment.is_lie,
        is_triple=environment.is_triple,
    )
