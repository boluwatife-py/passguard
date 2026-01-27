from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, List


class Severity(str, Enum):
    """
    Severity indicates how serious a validation issue is.

    This is intentionally small and opinionated for v1.
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class Issue:
    """
    A single password validation issue.

    - `code` is a stable, machine-readable identifier
    - `message` is human-readable and safe to show to users
    - `severity` allows consumers to prioritize issues
    """
    code: str
    message: str
    severity: Severity

    def to_dict(self) -> dict:
        """
        Serialize issue to a JSON-safe dict.
        """
        return {
            "code": self.code,
            "message": self.message,
            "severity": self.severity.value,
        }


@dataclass
class ValidationResult:
    """
    The result of evaluating a password.

    This object is intentionally rich:
    - Useful for APIs
    - Useful for frontend UX
    - Useful for logging and auditing
    """
    valid: bool
    score: int
    issues: List[Issue] = field(default_factory=list)

    def __post_init__(self) -> None:
        # Defensive guarantees
        if not 0 <= self.score <= 100:
            raise ValueError("score must be between 0 and 100")

        # If marked valid, issues should not contain critical errors
        if self.valid:
            for issue in self.issues:
                if issue.severity == Severity.CRITICAL:
                    raise ValueError(
                        "valid=True result cannot contain CRITICAL issues"
                    )

    @property
    def has_critical_issues(self) -> bool:
        return any(
            issue.severity == Severity.CRITICAL
            for issue in self.issues
        )

    @property
    def issue_codes(self) -> set[str]:
        return {issue.code for issue in self.issues}

    def to_dict(self) -> dict:
        """
        Serialize result to a JSON-safe dict.
        """
        return {
            "valid": self.valid,
            "score": self.score,
            "issues": [issue.to_dict() for issue in self.issues],
        }

    @classmethod
    def from_issues(
        cls,
        issues: Iterable[Issue],
        score: int,
        *,
        min_score: int = 100,
    ) -> "ValidationResult":
        """
        Construct a ValidationResult from a list of issues.

        `valid` is derived automatically.
        """
        issue_list = list(issues)

        has_critical = any(
            issue.severity == Severity.CRITICAL
            for issue in issue_list
        )

        valid = not has_critical and score >= min_score

        return cls(
            valid=valid,
            score=score,
            issues=issue_list,
        )
