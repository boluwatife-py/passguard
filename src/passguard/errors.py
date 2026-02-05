"""Custom exceptions for passguard."""
class PassGuardError(Exception):
    """Base exception for passguard."""

class PasswordTooWeakError(PassGuardError):
    """Raised when a password fails validation and must stop processing."""

class PolicyError(PassGuardError):
    """Raised if policy config is invalid."""
