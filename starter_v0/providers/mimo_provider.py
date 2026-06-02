from __future__ import annotations

import os

from providers.openai_provider import OpenAIProvider


class MiMoProvider(OpenAIProvider):
    """MiMo uses an OpenAI-compatible Chat Completions surface."""

    def __init__(self) -> None:
        super().__init__(
            api_key_env="MIMO_API_KEY",
            base_url=os.getenv("MIMO_BASE_URL", "https://token-plan-sgp.xiaomimimo.com/v1"),
            default_model=os.getenv("MIMO_MODEL", "mimo-v2.5"),
        )
