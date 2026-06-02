from __future__ import annotations

import json


def _get_depth(obj, current=0):
    if isinstance(obj, dict):
        if not obj:
            return current
        return max(_get_depth(v, current + 1) for v in obj.values())
    if isinstance(obj, list):
        if not obj:
            return current
        return max(_get_depth(item, current + 1) for item in obj)
    return current


def format_json(json_string: str = "", indent: int = 2) -> dict:
    if not json_string or not json_string.strip():
        return {
            "tool": "json_format",
            "error": "empty_input",
            "message": "No JSON string provided.",
            "valid": False,
            "formatted": "",
            "keys": [],
            "depth": 0,
        }

    try:
        parsed = json.loads(json_string)
    except json.JSONDecodeError as exc:
        return {
            "tool": "json_format",
            "error": "invalid_json",
            "message": f"Invalid JSON: {exc.msg} at line {exc.lineno} col {exc.colno}",
            "valid": False,
            "formatted": "",
            "keys": [],
            "depth": 0,
        }

    formatted = json.dumps(parsed, ensure_ascii=False, indent=indent)
    keys = list(parsed.keys()) if isinstance(parsed, dict) else []
    depth = _get_depth(parsed)

    return {
        "tool": "json_format",
        "valid": True,
        "formatted": formatted,
        "keys": keys,
        "depth": depth,
        "type": type(parsed).__name__,
        "item_count": len(parsed) if isinstance(parsed, (dict, list)) else None,
    }
