from __future__ import annotations

import re


def text_statistics(text: str = "") -> dict:
    if not text or not text.strip():
        return {
            "tool": "text_stats",
            "error": "empty_text",
            "message": "No text provided.",
            "word_count": 0,
            "char_count": 0,
            "char_count_no_spaces": 0,
            "sentence_count": 0,
            "paragraph_count": 0,
            "reading_time_minutes": 0.0,
        }

    text = text.strip()
    words = text.split()
    word_count = len(words)
    char_count = len(text)
    char_count_no_spaces = len(text.replace(" ", "").replace("\n", "").replace("\t", ""))
    sentences = re.split(r'[.!?]+', text)
    sentence_count = len([s for s in sentences if s.strip()])
    paragraphs = [p for p in text.split("\n\n") if p.strip()]
    paragraph_count = max(len(paragraphs), 1)
    reading_time = round(word_count / 200, 1)

    return {
        "tool": "text_stats",
        "word_count": word_count,
        "char_count": char_count,
        "char_count_no_spaces": char_count_no_spaces,
        "sentence_count": sentence_count,
        "paragraph_count": paragraph_count,
        "reading_time_minutes": reading_time,
    }
