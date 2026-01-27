from __future__ import annotations
from dataclasses import dataclass, field
from typing import Type, List, Optional

from .rules.base import PasswordRule
from .rules.length import MinLengthRule
from .rules.character import UppercaseRule, LowercaseRule, DigitRule, SymbolRule
from .rules.numeric import NumericOnlyRule
from .rules.common import CommonPasswordRule
from .rules.context import ContextRule


@dataclass
class PasswordPolicy:
    """
    Code-first password policy configuration.

    This controls:
    - Which rules are enabled
    - Rule-specific thresholds
    - Severity overrides
    """

    rules: List[PasswordRule] = field(default_factory=list)
    print(rules)

    @classmethod
    def default(cls) -> "PasswordPolicy":
        """
        Returns a sensible default policy for v1.
        """
        return cls(
            rules=[
                MinLengthRule(min_length=8),
                UppercaseRule(),
                LowercaseRule(),
                DigitRule(),
                SymbolRule(),
                NumericOnlyRule(),
                CommonPasswordRule(),
                ContextRule(),  # Checks username, email, names in password
            ]
        )

    def add_rule(self, rule: PasswordRule) -> None:
        """
        Add a custom rule to the policy.
        """
        self.rules.append(rule)

    def remove_rule(self, rule_type: Type[PasswordRule]) -> None:
        """
        Remove a rule by its class type.
        """
        self.rules = [r for r in self.rules if not isinstance(r, rule_type)]

    def get_rule(self, rule_type: Type[PasswordRule]) -> Optional[PasswordRule]:
        """
        Retrieve a specific rule instance by its class type.
        """
        for rule in self.rules:
            if isinstance(rule, rule_type):
                return rule
        return None
