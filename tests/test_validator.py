import pytest
from passguard.validator import PasswordValidator
from passguard.policy import PasswordPolicy
from passguard.results import ValidationResult, Severity, Issue
from passguard.context import Context


class TestPasswordValidator:
    def test_validator_with_default_policy(self):
        validator = PasswordValidator()
        assert isinstance(validator.policy, PasswordPolicy)
        assert len(validator.policy.rules) == 8

    def test_validator_with_custom_policy(self):
        policy = PasswordPolicy()
        validator = PasswordValidator(policy=policy)
        assert validator.policy == policy

    def test_evaluate_strong_password(self):
        validator = PasswordValidator()
        result = validator.evaluate("StrongPass123!", {"username": "user", "email": "user@test.com"})
        assert result.valid is True
        assert result.score == 100
        assert len(result.issues) == 0

    def test_evaluate_weak_password(self):
        validator = PasswordValidator()
        result = validator.evaluate("weak", {"username": "user"})
        assert result.valid is False
        assert result.score < 100
        assert len(result.issues) > 0

    def test_evaluate_with_context(self):
        validator = PasswordValidator()
        # Password contains username
        result = validator.evaluate("mypassworduser", {"username": "user"})
        assert result.valid is False
        assert any(issue.code == "contains_context" for issue in result.issues)

    def test_evaluate_min_score(self):
        # Create a policy with only one rule
        policy = PasswordPolicy()
        from passguard.rules.length import MinLengthRule
        policy.add_rule(MinLengthRule(min_length=5))
        validator = PasswordValidator(policy=policy)

        # Password "short" is exactly 5 chars, meets the rule, score=100
        # min_score=80, so should be valid
        result = validator.evaluate("short", min_score=80)
        assert result.valid is True
        assert result.score == 100

        # min_score=120 is higher than score=100, so should be invalid
        result = validator.evaluate("short", min_score=120)
        assert result.valid is False
        assert result.score == 100

    def test_evaluate_empty_context(self):
        validator = PasswordValidator()
        result = validator.evaluate("password123")
        assert isinstance(result, ValidationResult)

    def test_evaluate_with_none_context_data(self):
        validator = PasswordValidator()
        result = validator.evaluate("password123", context_data=None)
        assert isinstance(result, ValidationResult)

    def test_disable_single_rule(self):
        validator = PasswordValidator(disable_rules=["numeric_only"])
        # Numeric only passwords should now pass
        result = validator.evaluate("123456")
        # Should not have the numeric_only issue
        assert not any(issue.code == "numeric_only" for issue in result.issues)

    def test_disable_multiple_rules(self):
        validator = PasswordValidator(disable_rules=["numeric_only", "common_password"])
        # Check that these rules are disabled
        rule_codes = {rule.code for rule in validator.policy.rules}
        assert "numeric_only" not in rule_codes
        assert "common_password" not in rule_codes

    def test_disable_rules_count(self):
        default_validator = PasswordValidator()
        initial_count = len(default_validator.policy.rules)

        validator = PasswordValidator(disable_rules=["numeric_only", "common_password"])
        assert len(validator.policy.rules) == initial_count - 2

    def test_disable_nonexistent_rule(self):
        # Disabling a rule that doesn't exist should not raise an error
        validator = PasswordValidator(disable_rules=["nonexistent_rule"])
        assert len(validator.policy.rules) == 8  # All rules still present

    def test_disable_all_rules(self):
        all_rule_codes = ["too_short", "missing_uppercase", "missing_lowercase", "missing_digit",
                          "missing_symbol", "numeric_only", "common_password", "contains_context"]
        validator = PasswordValidator(disable_rules=all_rule_codes)
        assert len(validator.policy.rules) == 0

    def test_disable_with_custom_policy(self):
        policy = PasswordPolicy()
        from passguard.rules.length import MinLengthRule
        from passguard.rules.numeric import NumericOnlyRule
        policy.add_rule(MinLengthRule(min_length=8))
        policy.add_rule(NumericOnlyRule())

        validator = PasswordValidator(policy=policy, disable_rules=["numeric_only"])
        assert len(validator.policy.rules) == 1
        assert validator.policy.rules[0].code == "too_short"

    def test_disable_rules_affects_evaluation(self):
        # Without disabling, numeric password should fail
        validator_default = PasswordValidator()
        result_default = validator_default.evaluate("123456")
        assert any(issue.code == "numeric_only" for issue in result_default.issues)

        # With disabling, numeric password should pass more rules
        validator_disabled = PasswordValidator(disable_rules=["numeric_only"])
        result_disabled = validator_disabled.evaluate("123456")
        assert not any(issue.code == "numeric_only" for issue in result_disabled.issues)
        assert result_disabled.score > result_default.score