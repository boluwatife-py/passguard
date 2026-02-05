"""Context module for password validation."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Optional, List

from .utils.normalize import normalize_text, extract_email_local_part


@dataclass(frozen=True)
class Context:
    """
    Normalized, read-only context for password validation.

    Tracks all user-related fields that should not appear in passwords.
    """

    username: Optional[str] = field(default=None)
    email: Optional[str] = field(default=None)
    first_name: Optional[str] = field(default=None)
    second_name: Optional[str] = field(default=None)
    full_name: Optional[str] = field(default=None)

    @classmethod
    def from_mapping(cls, data: Mapping[str, object]) -> "Context":
        """
        Create a Context from arbitrary user-provided data.

        Accepts keys:
        - 'username'
        - 'email'
        - 'first_name' / 'firstname'
        - 'second_name' / 'lastname' / 'surname'
        - 'full_name' / 'name'
        """
        # Helper to pick first present key
        def pick(*keys):
            """Pick first present key."""
            for key in keys:
                if key in data and data[key]:
                    return normalize_text(str(data[key]))
            return None

        return cls(
            username=pick("username"),
            email=pick("email"),
            first_name=pick("first_name", "firstname"),
            second_name=pick("second_name", "lastname", "surname"),
            full_name=pick("full_name", "name"),
        )

    @property
    def email_local_part(self) -> Optional[str]:
        """
        Returns the local-part of the email (before '@'), normalized.
        """
        if not self.email:
            return None
        return extract_email_local_part(self.email)

    @property
    def all_fields(self) -> List[str]:
        """
        Returns a list of all normalized fields that can appear in password.
        """
        fields = [
            self.username,
            self.email,
            self.email_local_part,
            self.first_name,
            self.second_name,
            self.full_name,
        ]
        return [f for f in fields if f]  # skip None

    def contains(self, value: str) -> bool:
        """
        Check if the normalized value appears in any context field.

        Used by context-aware rules.
        """
        normalized = normalize_text(value)
        if not normalized:
            return False

        return any(normalized in field for field in self.all_fields)
