import re
from typing import Any


REDACTED = "[REDACTED]"

_SENSITIVE_FIELDS = frozenset(
    {
        "api_key",
        "apikey",
        "authorization",
        "cookie",
        "credentials",
        "openai_api_key",
        "password",
        "passwd",
        "proxy_authorization",
        "secret",
        "set_cookie",
    }
)

_SENSITIVE_SUFFIXES = (
    "_access_token",
    "_api_key",
    "_client_secret",
    "_password",
    "_refresh_token",
    "_secret",
    "_token",
)

_CREDENTIAL_ASSIGNMENT = re.compile(
    r"""(?ix)
    (?P<label>
        ["']?
        (?:api[_-]?key|access[_-]?token|refresh[_-]?token|client[_-]?secret|
           openai[_-]?api[_-]?key|proxy[_-]?authorization|set[_-]?cookie|
           authorization|credentials|password|passwd|cookie|secret|token)
        ["']?\s*[:=]\s*
    )
    (?P<quote>["']?)
    (?!\[REDACTED\])
    (?P<value>[^"'\s,;}\]]+)
    (?P=quote)
    """
)

_TOKEN_PATTERNS = (
    re.compile(r"(?i)\b(Bearer|Basic)\s+[A-Za-z0-9._~+/=-]+"),
    re.compile(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{8,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
)


def redact_text(value: str) -> str:
    redacted = _CREDENTIAL_ASSIGNMENT.sub(_redact_assignment, value)
    for pattern in _TOKEN_PATTERNS:
        if pattern.groups:
            redacted = pattern.sub(lambda match: f"{match.group(1)} {REDACTED}", redacted)
        else:
            redacted = pattern.sub(REDACTED, redacted)
    return redacted


def redact_data(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: REDACTED if _is_sensitive_field(str(key)) else redact_data(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [redact_data(item) for item in value]
    if isinstance(value, tuple):
        return tuple(redact_data(item) for item in value)
    if isinstance(value, str):
        return redact_text(value)
    return value


def _is_sensitive_field(field: str) -> bool:
    snake_case = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", field)
    normalized = re.sub(r"[^a-z0-9]+", "_", snake_case.lower()).strip("_")
    return normalized in _SENSITIVE_FIELDS or normalized.endswith(_SENSITIVE_SUFFIXES)


def _redact_assignment(match: re.Match[str]) -> str:
    quote = match.group("quote")
    return f"{match.group('label')}{quote}{REDACTED}{quote}"
