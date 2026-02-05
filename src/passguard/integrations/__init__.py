"""Framework integrations for PassGuard.

Modules:
    - pydantic: Pydantic v2 integration (PasswordField, PasswordStr)
"""

try:
    from .pydantic import PasswordField, PasswordStr
    __all__ = ["PasswordField", "PasswordStr"]
except ImportError:
    __all__ = []
