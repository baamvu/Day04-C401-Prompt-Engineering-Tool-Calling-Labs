---
name: summarize
track: bonus
kind: local_formatter
provider: null
requires_env: []
inputs: [text, max_sentences]
outputs: [summary, sentence_count, original_length]
side_effect: false
requires_confirmation: false
---
# summarize

Extracts key sentences from provided text to create a short summary.
Runs locally, no API key needed. Use when the user provides text directly
and asks to summarize it. Do NOT use for URLs (use `fetch` instead) or
for topics (use `lookup` instead).
