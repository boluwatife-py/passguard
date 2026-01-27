import pytest
from passguard.policy import PasswordPolicy
from passguard.rules.length import MinLengthRule
from passguard.rules.character import UppercaseRule, LowercaseRule, DigitRule, SymbolRule
from passguard.rules.numeric import NumericOnlyRule
from passguard.rules.common import CommonPasswordRule
from passguard.rules.context import ContextRule


class TestPasswordPolicy:
    def test_default_policy(self):
        policy = PasswordPolicy.default()
        assert len(policy.rules) == 8

        # Check that all expected rules are present
        rule_types = [type(rule) for rule in policy.rules]
        expected_types = [
            MinLengthRule, UppercaseRule, LowercaseRule, DigitRule, SymbolRule,
            NumericOnlyRule, CommonPasswordRule, ContextRule
        ]
        for expected_type in expected_types:
            assert expected_type in rule_types

    def test_policy_creation_empty(self):
        policy = PasswordPolicy()
        assert policy.rules == []

    def test_add_rule(self):
        policy = PasswordPolicy()
        rule = MinLengthRule(min_length=10)
        policy.add_rule(rule)
        assert len(policy.rules) == 1
        assert policy.rules[0] == rule

    def test_remove_rule_by_type(self):
        policy = PasswordPolicy.default()
        initial_count = len(policy.rules)
        policy.remove_rule(MinLengthRule)
        assert len(policy.rules) == initial_count - 1
        assert not any(isinstance(r, MinLengthRule) for r in policy.rules)

    def test_remove_rule_not_present(self):
        policy = PasswordPolicy()
        policy.remove_rule(MinLengthRule)  # Should not raise
        assert len(policy.rules) == 0

    def test_get_rule_existing(self):
        policy = PasswordPolicy.default()
        rule = policy.get_rule(MinLengthRule)
        assert isinstance(rule, MinLengthRule)
        assert rule.min_length == 8

    def test_get_rule_not_existing(self):
        policy = PasswordPolicy()
        rule = policy.get_rule(MinLengthRule)
        assert rule is None