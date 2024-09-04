from ortools.sat.python.cp_model import CpModel, IntVar


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


def create_partial_rule_dict() -> dict[int, list[int]]:
    ret: dict[int, list[int]] = {}
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
        key = len(key_list)
        if key not in ret:
            ret[key] = []
        ret[key].append(S)
    return ret


def add_partial_rule(
    model: CpModel,
    mines: list[list[IntVar]],
    grid: list[list[int]],
    rows: int,
    cols: int,
) -> None:
    partial_rule_dict = create_partial_rule_dict()
    dr: list[int] = [-1, -1, -1, 0, 1, 1, 1, 0]
    dc: list[int] = [-1, 0, 1, 1, 1, 0, -1, -1]
    for r in range(rows):
        for c in range(cols):
            partial = [
                mines[r + dr[i]][c + dc[i]]
                for i in range(8)
                if 0 <= r + dr[i] < rows and 0 <= c + dc[i] < cols
            ]
            key = grid[r][c]
            if key < 0:
                continue
            if key not in partial_rule_dict:
                print(f"key: {key}")
            assert key in partial_rule_dict
            rule_list: list[list[int]] = []
            for S in partial_rule_dict[key]:
                ok_flag = True
                for i in range(8):
                    if ((S >> i) & 1) and not (
                        0 <= r + dr[i] < rows and 0 <= c + dc[i] < cols
                    ):
                        ok_flag = False
                        break
                if not ok_flag:
                    continue
                rule = [
                    (S >> i) & 1
                    for i in range(8)
                    if 0 <= r + dr[i] < rows and 0 <= c + dc[i] < cols
                ]
                rule_list.append(rule)
            model.AddAllowedAssignments(partial, rule_list)
