from __future__ import annotations
from typing import Optional

from .base import PasswordRule
from ..results import Issue, Severity


class MinLengthRule(PasswordRule):
    """
    Rule that enforces a minimum password length.

    This rule ensures passwords are at least a specified number of characters long
    to provide basic resistance against brute-force attacks.
    """

    code = "too_short"
    severity = Severity.MEDIUM

    def __init__(self, min_length: int = 8, severity: Optional[Severity] = None) -> None:
        super().__init__(severity)
        self.min_length = min_length

    def check(self, password: str, context) -> Issue | None:
        """
        Check if the password meets the minimum length requirement.

        Args:
            password: The password to validate
            context: Normalized user context (not used in this rule)

        Returns:
            Issue if password is too short, otherwise None
        """
        if len(password) < self.min_length:
            return Issue(
                code=self.code,
                message=f"Password must be at least {self.min_length} characters long.",
                severity=self.severity,
            )
        return None