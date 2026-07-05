"""Security utilities (placeholder for future auth)."""

from typing import Any


def sanitize_metadata(data: dict[str, Any]) -> dict[str, Any]:
    """Remove sensitive fields from metadata before returning to client."""
    sensitive = {"password", "secret", "key", "token", "credentials"}
    return {
        k: v
        for k, v in data.items()
        if not any(s in k.lower() for s in sensitive)
    }
