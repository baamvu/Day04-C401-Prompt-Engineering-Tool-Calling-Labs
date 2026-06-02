---
name: json_format
track: bonus
kind: local_formatter
provider: null
requires_env: []
inputs: [json_string, indent]
outputs: [formatted, valid, keys, depth]
side_effect: false
requires_confirmation: false
---
# json_format

Parses, validates, and formats JSON strings. Returns formatted JSON,
validity status, top-level keys, and nesting depth. No API key needed.
Useful for checking JSON syntax or pretty-printing JSON data.
