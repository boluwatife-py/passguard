"""
PassGuard - Comprehensive password validation library for Python.

Main Classes:
    - PasswordValidator: Main validator class for password evaluation
    - PasswordPolicy: Configuration for validation rules
    - ValidationResult: Result object with validation details
    - Issue: Individual validation issue
    - Severity: Issue severity levels
    - Context: Normalized user context for validation

Pydantic Integration:
    - PasswordField: Pydantic field validator for passwords
    - PasswordStr: Pydantic-compatible password string type

Example:
    >>> from passguard import PasswordValidator
    >>> validator = PasswordValidator()
    >>> result = validator.evaluate(
    ...     "MyPassword123!",
    ...     context_data={"username": "john", "email": "john@example.com"}
    ... )
    >>> print(result.valid, result.score)
"""

from .validator import PasswordValidator
from .policy import PasswordPolicy
from .results import ValidationResult, Issue, Severity
from .context import Context

# Pydantic integration - optional
try:
    from .integrations.pydantic import PasswordField, PasswordStr
    __all__ = [
        "PasswordValidator",
        "PasswordPolicy",
        "ValidationResult",
        "Issue",
        "Severity",
        "Context",
        "PasswordField",
        "PasswordStr",
    ]
except ImportError:
    # Pydantic not installed, export without it
    __all__ = [
        "PasswordValidator",
        "PasswordPolicy",
        "ValidationResult",
        "Issue",
        "Severity",
        "Context",
    ]

__version__ = "0.1.0"
__author__ = "PassGuard Contributors"
__license__ = "MIT"
