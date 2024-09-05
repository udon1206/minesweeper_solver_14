from pydantic import BaseModel


class Environment(BaseModel):
    grid_array: list[list[list[int]]]
    all_mines_count: int
    rule_grid: list[list[str]]
    is_quad: bool = False
    is_connect: bool = False
    is_triple: bool = False
    is_out: bool = False
    is_dual: bool = False
    is_snake: bool = False
    is_balance: bool = False

    # grid の成分の和を返す
    def get_grid(self) -> list[list[int]]:
        ret: list[list[int]] = []
        for grid in self.grid_array:
            ret.append([sum(row) for row in grid])
        return ret
