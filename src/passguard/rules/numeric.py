from __future__ import annotations
import re
from typing import Optional

from .base import PasswordRule
from ..results import Issue, Severity


class NumericOnlyRule(PasswordRule):
    """
    Rule that prevents passwords that are entirely numeric.

    This rule discourages weak passwords that consist only of numbers,
    which are easily guessable and provide little security.
    """

    code = "numeric_only"
    severity = Severity.HIGH

    def __init__(self, severity: Optional[Severity] = None) -> None:
        super().__init__(severity)

    def check(self, password: str, context) -> Issue | None:
        """
        Check if the password consists only of numeric characters.

        Args:
            password: The password to validate
            context: Normalized user context (not used in this rule)

        Returns:
            Issue if password is entirely numeric, otherwise None
        """
        if re.match(r"^\d+$", password):
            return Issue(
                code=self.code,
                message="Password cannot be entirely numeric.",
                severity=self.severity,
            )
        return None