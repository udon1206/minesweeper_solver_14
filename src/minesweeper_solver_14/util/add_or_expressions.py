from ortools.sat.python.cp_model import BoundedLinearExpression, CpModel, IntVar
import uuid

expr = BoundedLinearExpression | bool
only_if = IntVar


def add_or_expressions(
    model: CpModel, exprs: list[list[tuple[expr, list[only_if]]]]
) -> None:
    labels = []
    for _ in exprs:
        labels.append(model.NewBoolVar(str(uuid.uuid4())))
    for label, expr_only_if in zip(labels, exprs):
        for expr, only_if in expr_only_if:
            if isinstance(expr, BoundedLinearExpression):
                model.Add(expr).OnlyEnforceIf(label, *only_if)
    model.AddBoolOr(*labels)
    return
