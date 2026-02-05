"""Common password rules."""
from __future__ import annotations
from typing import Optional

from .base import PasswordRule
from ..results import Issue, Severity
from ..utils.loaders import load_common_passwords


class CommonPasswordRule(PasswordRule):
    """
    Rule that checks if the password is in a list of commonly used passwords.

    This rule prevents the use of passwords that are known to be weak
    and frequently used, reducing the risk of credential stuffing attacks.
    """

    code = "common_password"
    severity = Severity.HIGH

    def __init__(self, severity: Optional[Severity] = None) -> None:
        super().__init__(severity)
        self._common_passwords = load_common_passwords()

    def check(self, password: str, context) -> Issue | None:
        """
        Check if the password is in the common passwords list.

        Args:
            password: The password to validate
            context: Normalized user context (not used in this rule)

        Returns:
            Issue if password is common, otherwise None
        """
        if password.lower() in self._common_passwords:
            return Issue(
                code=self.code,
                message="Password is too common and easily guessable.",
                severity=self.severity,
            )
        return None
