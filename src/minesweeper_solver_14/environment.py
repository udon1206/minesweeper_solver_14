from typing import Optional
from pydantic import BaseModel
import json


class Environment(BaseModel):
    grid_array: list[list[list[int]]]
    all_mines_count: int
    coffeences: Optional[list[list[int]]] = None
    is_quad: bool = False
    is_connect: bool = False
    is_lie: bool = False
    is_triple: bool = False
    is_out: bool = False

    # grid の成分の和を返す
    def get_grid(self) -> list[list[int]]:
        ret: list[list[int]] = []
        for grid in self.grid_array:
            ret.append([sum(row) for row in grid])
        return ret


def create_environment_from_json(json_file_path: str) -> Environment:
    with open(json_file_path, "r") as f:
        json_data = json.load(f)
    return Environment(
        grid_array=json_data.get("grid_array"),
        all_mines_count=json_data.get("all_mines_count"),
        coffeences=json_data.get("coffeences"),
        is_quad=json_data.get("rule").get("is_quad"),
        is_connect=json_data.get("rule").get("is_connect"),
        is_lie=json_data.get("rule").get("is_lie"),
        is_triple=json_data.get("rule").get("is_triple"),
    )
