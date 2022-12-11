import re

import aocd


def simple_expr(expr: str) -> int:
    expr = expr.strip()

    if re.match(r"^\d+$", expr) is not None:
        return int(expr)
    else:
        res = re.match(r"^([\d\s*+]+)([*+])\s*(\d+)$", expr)
        if res is None:
            raise ValueError(f"cannot process {expr}")
        else:
            if res.group(2) == "+":
                return simple_expr(res.group(1)) + int(res.group(3))
            else:
                return simple_expr(res.group(1)) * int(res.group(3))


def test_simple_expr():
    assert simple_expr("1+2") == 3
    assert simple_expr("1+2*3") == 9
    assert simple_expr("1+ 2*3") == 9
    assert simple_expr("   1 *   2 +   3   ") == 5


def simple_expr_v2(expr: str) -> int:
    expr = expr.strip()

    if re.match(r"^\d+$", expr) is not None:
        return int(expr)
    else:
        while True:
            res = re.search(r"(\d+\s*\+\s*\d+)", expr)
            if res is None:
                break

            expr = (
                expr[: res.span()[0]] + str(simple_expr(res.group())) + expr[res.span()[1] :]
            )

        return simple_expr(expr)


def test_simple_expr_v2():
    assert simple_expr_v2("1 + 2 * 3 + 4 * 5 + 6") == 231


def full_expr(expr: str, simple_expr_func=simple_expr) -> str:
    expr = expr.strip()

    while True:
        res = re.search(r"\(([\d\s*+]+)\)", expr)
        if res is None:
            break

        expr = (
            expr[: res.span()[0]]
            + full_expr(res.group().lstrip("(").rstrip(")"), simple_expr_func)
            + expr[res.span()[1] :]
        )

    return str(simple_expr_func(expr))


def test_full_expr():
    assert full_expr("1+(2*3)") == "7"
    assert full_expr("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == "12240"
    assert full_expr("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == "13632"


def test_full_expr_v2():
    assert full_expr("1 + (2 * 3) + (4 * (5 + 6))", simple_expr_v2) == "51"
    assert full_expr("5 + (8 * 3 + 9 + 3 * 4 * 3)", simple_expr_v2) == "1445"
    assert full_expr("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", simple_expr_v2) == "669060"


def day18(data: str, simple_expr_func) -> int:
    return sum(int(full_expr(line, simple_expr_func)) for line in data.splitlines())


def main():
    print(f"day 18 part 1: {day18(aocd.get_data(day=18, year=2020), simple_expr)}")
    print(f"day 18 part 2: {day18(aocd.get_data(day=18, year=2020), simple_expr_v2)}")


if __name__ == "__main__":
    main()
