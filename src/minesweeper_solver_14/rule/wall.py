from ortools.sat.python.cp_model import CpModel, IntVar
import copy


def run_length_encoding(s: str) -> list[tuple[str, int]]:
    result = []
    current_char = s[0]
    current_count = 1
    for i in range(1, len(s)):
        if s[i] == current_char:
            current_count += 1
        else:
            result.append((current_char, current_count))
            current_char = s[i]
            current_count = 1
    result.append((current_char, current_count))
    return result


def convert_key_list_to_key(key_list: list[int]) -> str:
    sorted_key_list = copy.deepcopy(key_list)
    sorted_key_list.sort()
    return "".join([str(k) for k in sorted_key_list])


def create_wall_rule_dict() -> dict[str, list[int]]:
    ret: dict[str, list[int]] = {}
    for S in range(1 << 8):
        s = ""
        for i in range(8):
            s += "1" if S & (1 << i) else "0"
        rle = run_length_encoding(s)
        key_list = []
        for i in range(len(rle)):
            if rle[i][0] == "1":
                key_list.append(rle[i][1])
        if (S != (1 << 8) - 1) and ((S >> 7) & 1) == 1 and (S & 1) == 1:
            tmp = key_list[-1]
            key_list.pop()
            key_list[0] += tmp
        key = convert_key_list_to_key(key_list)
        if key not in ret:
            ret[key] = []
        ret[key].append(S)
    return ret


def add_wall_rule(
    model: CpModel,
    mines: list[list[IntVar]],
    grid_array: list[list[list[int]]],
    rows: int,
    cols: int,
) -> None:
    wall_rule_dict = create_wall_rule_dict()
    dr: list[int] = [-1, -1, -1, 0, 1, 1, 1, 0]
    dc: list[int] = [-1, 0, 1, 1, 1, 0, -1, -1]
    for r in range(rows):
        for c in range(cols):
            wall = [
                mines[r + dr[i]][c + dc[i]]
                for i in range(8)
                if 0 <= r + dr[i] < rows and 0 <= c + dc[i] < cols
            ]
            if len(grid_array[r][c]) == 0 or grid_array[r][c][0] < 0:
                continue
            key = convert_key_list_to_key(grid_array[r][c])
            if key not in wall_rule_dict:
                print(f"key: {key}")
            assert key in wall_rule_dict
            rule_list: list[list[int]] = []
            for S in wall_rule_dict[key]:
                rule = [
                    (S >> i) & 1
                    for i in range(8)
                    if 0 <= r + dr[i] < rows and 0 <= c + dc[i] < cols
                ]
                rule_list.append(rule)
            model.AddAllowedAssignments(wall, rule_list)
