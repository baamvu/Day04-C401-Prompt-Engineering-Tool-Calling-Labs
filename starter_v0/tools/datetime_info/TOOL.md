---
name: datetime_info
track: bonus
kind: local_formatter
provider: null
requires_env: []
inputs: [timezone]
outputs: [date, time, day_of_week, timestamp, iso_format]
side_effect: false
requires_confirmation: false
---
# datetime_info

Returns current date, time, day of week, and timestamp. No API key needed.
Useful for answering "hôm nay là ngày mấy?", "mấy giờ rồi?", or getting
the current date for context in research queries.
