---
name: text_stats
track: bonus
kind: local_formatter
provider: null
requires_env: []
inputs: [text]
outputs: [word_count, char_count, sentence_count, paragraph_count, reading_time_minutes]
side_effect: false
requires_confirmation: false
---
# text_stats

Analyzes text and returns statistics: word count, character count, sentence count,
paragraph count, and estimated reading time. No API key needed.
