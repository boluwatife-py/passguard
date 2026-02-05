"""Pydantic integration module."""
from __future__ import annotations

from typing import Any, Optional, Annotated

from pydantic import AfterValidator

from ..validator import PasswordValidator
from ..policy import PasswordPolicy


# Global registry to store field configurations
_PASSWORD_FIELD_CONFIGS: dict[str, dict[str, Any]] = {}


class PasswordField:
    """
    Pydantic-compatible password field with Passguard validation.

    Usage:
        from pydantic import BaseModel
        from passguard.integrations.pydantic import PasswordField
        from passguard.policy import PasswordPolicy

        policy = PasswordPolicy.default()
        
        class RegisterRequest(BaseModel):
            username: str
            email: str
            password: str = PasswordField(
                policy=policy,
                min_score=80,
                context_fields=["username", "email"]
            )
    """

    def __init__(
        self,
        *,
        min_score: int = 100,
        policy: Optional[PasswordPolicy] = None,
        context_fields: Optional[list[str]] = None,
    ) -> None:
        """
        Args:
            min_score: Minimum score (0-100) required for password to be valid
            policy: Optional custom PasswordPolicy. Defaults to PasswordPolicy.default()
            context_fields: Optional list of field names to extract as context
                           (e.g., username, email)
        """
        self.policy = policy or PasswordPolicy.default()
        self.min_score = min_score
        self.context_fields = context_fields or []

    def __set_name__(self, owner: type, name: str) -> None:
        """Called when the descriptor is assigned to a class attribute."""
        # Store this field's configuration for later use
        _PASSWORD_FIELD_CONFIGS[f"{owner.__module__}.{owner.__qualname__}.{name}"] = {
            "policy": self.policy,
            "min_score": self.min_score,
            "context_fields": self.context_fields,
        }

    def __call__(self, value: str) -> str:
        """Allow PasswordField to be used in Field() default."""
        return value

    @staticmethod
    def make_validator(
        policy: Optional[PasswordPolicy] = None,
        min_score: int = 100,
        context_fields: Optional[list[str]] = None,
    ):
        """
        Create a field validator for password validation.
        
        Returns a function that can be used with Pydantic's field_validator.
        """
        actual_policy = policy or PasswordPolicy.default()
        actual_context_fields = context_fields or []

        def validate_password_field(value: str, info: Any) -> str:
            """Validate password using Passguard rules."""
            if not isinstance(value, str):
                raise TypeError("Password must be a string")

            context_data = {}
            if info.data:
                fields = (
                    actual_context_fields
                    if actual_context_fields
                    else info.data.keys()
                )

                for field in fields:
                    if field != info.field_name and field in info.data:
                        context_data[field] = info.data[field]

            # Use the provided policy
            validator = PasswordValidator(policy=actual_policy)

            result = validator.evaluate(
                value,
                context_data=context_data,
                min_score=min_score,
            )

            if not result.valid:
                # Convert passguard issues → pydantic error
                raise ValueError(
                    "; ".join(issue.message for issue in result.issues)
                )

            return value

        return validate_password_field


class PasswordFieldAnnotation:
    """
    Annotation helper to use with Pydantic's Annotated type.
    
    Usage:
        from typing import Annotated
        from pydantic import BaseModel
        from passguard.integrations.pydantic import PasswordFieldAnnotation
        from passguard.policy import PasswordPolicy
        
        policy = PasswordPolicy.default()
        
        class RegisterRequest(BaseModel):
            username: str
            password: Annotated[
                str, 
                PasswordFieldAnnotation(policy=policy, min_score=80)
            ]
    """

    def __init__(
        self,
        *,
        min_score: int = 100,
        policy: Optional[PasswordPolicy] = None,
        context_fields: Optional[list[str]] = None,
    ) -> None:
        self.policy = policy or PasswordPolicy.default()
        self.min_score = min_score
        self.context_fields = context_fields or []


def validate_password(value: str) -> str:
    """Validate password using default policy."""
    if not isinstance(value, str):
        raise TypeError("Password must be a string")

    validator = PasswordValidator(policy=PasswordPolicy.default())

    result = validator.evaluate(
        value,
        context_data={},
        min_score=100,
    )

    if not result.valid:
        raise ValueError(
            "; ".join(issue.message for issue in result.issues)
        )

    return value


PasswordStr = Annotated[str, AfterValidator(validate_password)]
