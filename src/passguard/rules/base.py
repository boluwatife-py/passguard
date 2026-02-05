"""Base class for password rules."""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional

from ..context import Context
from ..results import Issue, Severity


class PasswordRule(ABC):
    """
    Base interface for all password rules.

    Each rule:
    - Inspects a password (and optional context)
    - Returns an Issue if it fails
    - Returns None if it passes

    Attributes:
        code (str):
            Unique machine-readable identifier for the rule.
            This is used in API responses, logs, or analytics.

            ⚡ Guidelines:
            - Lowercase letters, underscores only (no spaces)
            - Short, descriptive, stable
            - Do NOT include user-visible messages here

            Examples:
                "too_short"           # Password length is below minimum
                "missing_uppercase"   # Password lacks uppercase letters
                "common_password"     # Password is in the common-password list
                "contains_username"   # Password contains username or parts of name
    """

    code: str            # Unique machine-readable identifier
    severity: Severity   # Severity level for this rule

    def __init__(self, severity: Optional[Severity] = None) -> None:
        if severity:
            self.severity = severity

    @abstractmethod
    def check(self, password: str, context: Context) -> Issue | None:
        """
        Check the password against this rule.

        Args:
            password: The password to validate
            context: Normalized user context

        Returns:
            Issue if the password violates this rule, otherwise None
        """
