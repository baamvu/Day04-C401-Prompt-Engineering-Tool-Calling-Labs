from __future__ import annotations

import re


def _split_sentences(text: str) -> list[str]:
    text = text.strip()
    if not text:
        return []
    parts = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in parts if s.strip()]
    return sentences


def summarize_text(text: str = "", max_sentences: int = 3) -> dict:
    if not text or not text.strip():
        return {
            "tool": "summarize",
            "error": "empty_text",
            "message": "No text provided to summarize.",
            "summary": "",
            "sentence_count": 0,
            "original_length": 0,
        }

    sentences = _split_sentences(text)
    if not sentences:
        return {
            "tool": "summarize",
            "error": "no_sentences",
            "message": "Could not extract any sentences from the text.",
            "summary": "",
            "sentence_count": 0,
            "original_length": len(text),
        }

    max_sentences = max(1, min(max_sentences, len(sentences)))
    selected = sentences[:max_sentences]
    summary = " ".join(selected)

    return {
        "tool": "summarize",
        "summary": summary,
        "sentence_count": len(selected),
        "original_length": len(text),
        "original_sentence_count": len(sentences),
    }
