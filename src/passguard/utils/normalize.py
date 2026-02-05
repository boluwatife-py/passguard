"""Text normalization utilities."""
import re

# Simple leetspeak mapping for basic substitutions
_LEET_MAP = str.maketrans({
    "0": "o",
    "1": "l",
    "3": "e",
    "4": "a",
    "5": "s",
    "7": "t",
    "@": "a",
    "$": "s",
})


def normalize_text(value: str) -> str:
    """
    Normalize text for comparison in context-aware rules.

    Steps:
    1. Lowercase
    2. Strip whitespace
    3. Apply simple leetspeak substitutions
    4. Remove non-alphanumeric characters

    Example:
        "B0lu123!" -> "bolu123"
    """
    if not value:
        return ""

    # Lowercase and strip whitespace
    value = value.lower().strip()

    # Translate leetspeak
    value = value.translate(_LEET_MAP)

    # Remove non-alphanumeric characters
    value = re.sub(r"[^a-z0-9]", "", value)

    return value


def extract_email_local_part(email: str) -> str:
    """
    Extract and normalize the local part of an email (before @).

    Example:
        "Bolu.Akingbade@gmail.com" -> "boluakingbade"
    """
    if not email:
        return ""

    local_part = email.split("@")[0]
    return normalize_text(local_part)
