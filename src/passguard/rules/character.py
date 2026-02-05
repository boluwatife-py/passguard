"""Character set rules (uppercase, lowercase, digits, symbols)."""
from __future__ import annotations
import re


from .base import PasswordRule
from ..results import Issue, Severity


class UppercaseRule(PasswordRule):
    """
    Rule that requires at least one uppercase letter in the password.

    This enforces password complexity by ensuring the password contains
    uppercase characters, making it harder to guess.
    """

    code = "missing_uppercase"
    severity = Severity.MEDIUM

    def check(self, password: str, context) -> Issue | None:
        """
        Check if the password contains at least one uppercase letter.

        Args:
            password: The password to validate
            context: Normalized user context (not used in this rule)

        Returns:
            Issue if no uppercase letter found, otherwise None
        """
        if not re.search(r"[A-Z]", password):
            return Issue(
                code=self.code,
                message="Password must contain at least one uppercase letter.",
                severity=self.severity,
            )
        return None


class LowercaseRule(PasswordRule):
    """
    Rule that requires at least one lowercase letter in the password.

    This enforces password complexity by ensuring the password contains
    lowercase characters, making it harder to guess.
    """

    code = "missing_lowercase"
    severity = Severity.MEDIUM

    def check(self, password: str, context) -> Issue | None:
        """
        Check if the password contains at least one lowercase letter.

        Args:
            password: The password to validate
            context: Normalized user context (not used in this rule)

        Returns:
            Issue if no lowercase letter found, otherwise None
        """
        if not re.search(r"[a-z]", password):
            return Issue(
                code=self.code,
                message="Password must contain at least one lowercase letter.",
                severity=self.severity,
            )
        return None


class DigitRule(PasswordRule):
    """
    Rule that requires at least one digit in the password.

    This enforces password complexity by ensuring the password contains
    numeric characters, making it harder to guess.
    """

    code = "missing_digit"
    severity = Severity.MEDIUM

    def check(self, password: str, context) -> Issue | None:
        """
        Check if the password contains at least one digit.

        Args:
            password: The password to validate
            context: Normalized user context (not used in this rule)

        Returns:
            Issue if no digit found, otherwise None
        """
        if not re.search(r"\d", password):
            return Issue(
                code=self.code,
                message="Password must contain at least one digit.",
                severity=self.severity,
            )
        return None


class SymbolRule(PasswordRule):
    """
    Rule that requires at least one symbol (special character) in the password.

    This enforces password complexity by ensuring the password contains
    non-alphanumeric characters, making it harder to guess.
    """

    code = "missing_symbol"
    severity = Severity.MEDIUM

    def check(self, password: str, context) -> Issue | None:
        """
        Check if the password contains at least one symbol.

        Args:
            password: The password to validate
            context: Normalized user context (not used in this rule)

        Returns:
            Issue if no symbol found, otherwise None
        """
        if not re.search(r"[^a-zA-Z0-9]", password):
            return Issue(
                code=self.code,
                message="Password must contain at least one symbol (special character).",
                severity=self.severity,
            )
        return None

