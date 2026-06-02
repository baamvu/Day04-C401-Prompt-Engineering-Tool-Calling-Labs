from __future__ import annotations

import ast
import math
import operator

SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

SAFE_FUNCTIONS = {
    "abs": abs,
    "round": round,
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log10": math.log10,
    "log2": math.log2,
    "ceil": math.ceil,
    "floor": math.floor,
    "pi": math.pi,
    "e": math.e,
}


def _eval_node(node):
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant: {node.value!r}")
    if isinstance(node, ast.BinOp):
        op = SAFE_OPERATORS.get(type(node.op))
        if op is None:
            raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
        return op(_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp):
        op = SAFE_OPERATORS.get(type(node.op))
        if op is None:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        return op(_eval_node(node.operand))
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            func = SAFE_FUNCTIONS.get(node.func.id)
            if func is None:
                raise ValueError(f"Unsupported function: {node.func.id}")
            args = [_eval_node(arg) for arg in node.args]
            return func(*args)
        raise ValueError("Unsupported call")
    if isinstance(node, ast.Name):
        val = SAFE_FUNCTIONS.get(node.id)
        if val is not None:
            return val
        raise ValueError(f"Unknown name: {node.id}")
    raise ValueError(f"Unsupported expression type: {type(node).__name__}")


def calculate(expression: str = "") -> dict:
    if not expression or not expression.strip():
        return {
            "tool": "calculator",
            "error": "empty_expression",
            "message": "No expression provided.",
            "expression": expression,
            "result": None,
        }

    expr = expression.strip()
    try:
        tree = ast.parse(expr, mode="eval")
        result = _eval_node(tree)
        return {
            "tool": "calculator",
            "expression": expr,
            "result": result,
        }
    except (ValueError, ZeroDivisionError, TypeError, SyntaxError) as exc:
        return {
            "tool": "calculator",
            "error": type(exc).__name__,
            "message": str(exc),
            "expression": expr,
            "result": None,
        }
