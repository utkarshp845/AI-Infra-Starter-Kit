import json
import os
from dataclasses import dataclass
from typing import Any

import httpx

from app.prompts import ANALYSIS_INSTRUCTIONS, SYSTEM_PROMPT
from app.redaction import redact_data, redact_text


@dataclass(frozen=True)
class LLMConfig:
    provider: str
    api_key: str
    base_url: str
    model: str


def load_config() -> LLMConfig:
    provider = os.getenv("LLM_PROVIDER", "none").strip().lower()
    default_base_url = "http://localhost:11434/v1" if provider == "ollama" else "https://api.openai.com/v1"
    return LLMConfig(
        provider=provider,
        api_key=os.getenv("OPENAI_API_KEY", "").strip(),
        base_url=os.getenv("OPENAI_BASE_URL", default_base_url).strip().rstrip("/"),
        model=os.getenv("MODEL_NAME", "gpt-4o-mini").strip(),
    )


def is_configured(config: LLMConfig) -> bool:
    if config.provider in {"", "none", "disabled", "rule-based"}:
        return False
    if config.provider == "ollama":
        return bool(config.base_url and config.model)
    return bool(config.api_key and config.base_url and config.model)


def analyze_with_llm(
    question: str,
    logs: list[dict[str, Any]],
    rule_based_analysis: dict[str, Any],
    config: LLMConfig | None = None,
) -> tuple[str | None, str | None]:
    config = config or load_config()
    if not is_configured(config):
        return None, "LLM provider is not configured; using rule-based analysis."

    safe_question = redact_text(question)
    safe_logs = redact_data(logs[-50:])
    safe_analysis = redact_data(rule_based_analysis)
    evidence = "\n".join(json.dumps(entry, default=str) for entry in safe_logs)
    user_prompt = f"""
Question:
{safe_question}

Rule-based pre-analysis:
{json.dumps(safe_analysis, indent=2, default=str)}

Recent log evidence:
{evidence}

{ANALYSIS_INSTRUCTIONS}
"""

    headers = {"Content-Type": "application/json"}
    if config.api_key:
        headers["Authorization"] = f"Bearer {config.api_key}"

    payload = {
        "model": config.model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.2,
    }

    try:
        with httpx.Client(timeout=30) as client:
            response = client.post(f"{config.base_url}/chat/completions", headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            return redact_text(str(content).strip()), None
    except Exception as exc:
        return None, f"LLM request failed; using rule-based analysis. Error: {redact_text(str(exc))}"

