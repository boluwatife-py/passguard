"""Password validator module."""
from __future__ import annotations
from typing import Optional, Sequence

from .context import Context
from .policy import PasswordPolicy
from .results import ValidationResult, Issue



class PasswordValidator:
    """
    Main password validator class.

    Usage:

        # Default policy with all rules
        validator = PasswordValidator()

        # Disable specific rules by code
        validator = PasswordValidator(disable_rules=["numeric_only", "common_password"])

        result = validator.evaluate(
            "MyPassword123!",
            context_data={"username": "bolu", "email": "bolu@gmail.com"}
        )

        result.valid
        result.score
        result.issues
    """

    def __init__(
        self,
        policy: Optional[PasswordPolicy] = None,
        disable_rules: Optional[Sequence[str]] = None,
    ):
        """
        Args:
            policy: Optional custom policy. Defaults to PasswordPolicy.default()
            disable_rules: Optional list of rule codes to turn off from the default policy
        """
        self.policy = policy or PasswordPolicy.default()
        self.disable_rules = set(disable_rules or [])

        if self.disable_rules:
            # Filter out the disabled rules
            self.policy.rules = [
                rule for rule in self.policy.rules if rule.code not in self.disable_rules
            ]
    def evaluate(
        self,
        password: str,
        context_data: Optional[dict] = None,
        min_score: int = 100
    ) -> ValidationResult:
        """
        Evaluate a password against all rules in the policy.

        Args:
            password: The password to validate
            context_data: Optional dict of user info (username, email, names)
            min_score: Minimum score required to consider the password valid

        Returns:
            ValidationResult: structured result with issues and score
        """
        # Build normalized context
        context = Context.from_mapping(context_data or {})

        # Run all rules
        issues: list[Issue] = []
        passed_rules = 0
        total_rules = len(self.policy.rules)

        for rule in self.policy.rules:
            issue = rule.check(password, context)
            if issue:
                issues.append(issue)
            else:
                passed_rules += 1

        # Compute simple score: percentage of rules passed
        score = int((passed_rules / total_rules) * 100) if total_rules else 100


        # Build ValidationResult
        result = ValidationResult.from_issues(
            issues=issues,
            score=score,
            min_score=min_score
        )

        return result
