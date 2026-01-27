from __future__ import annotations

from typing import Iterable

from .base import PasswordRule
from ..context import Context
from ..results import Issue, Severity
from ..utils.normalize import normalize_text


class ContextRule(PasswordRule):
    """
    Prevents passwords from containing any user-identifying information.

    This rule is intentionally strict:
    - Full matches are rejected
    - Partial matches are rejected
    - Case-insensitive
    - Leetspeak-aware
    """

    code = "contains_context"
    severity = Severity.HIGH

    def _context_values(self, context: Context) -> Iterable[str]:
        if context.username:
            yield context.username

        if context.email:
            yield context.email
            if "@" in context.email:
                local, domain = context.email.split("@", 1)
                yield local
                for part in domain.split("."):
                    yield part

        if context.first_name:
            yield context.first_name

        if context.second_name:
            yield context.second_name

        if context.full_name:
            yield context.full_name
            for part in context.full_name.split():
                yield part

    def check(self, password: str, context: Context) -> Issue | None:
        if not password:
            return None

        normalized_password = normalize_text(password)
        if not normalized_password:
            return None

        for value in self._context_values(context):
            normalized_value = normalize_text(value)
            if not normalized_value:
                continue

            # Reject ANY overlap (partial or full)
            if (
                normalized_value in normalized_password
                or normalized_password in normalized_value
            ):
                return Issue(
                    code=self.code,
                    message="Password cannot contain personal information.",
                    severity=self.severity,
                )

        return None
