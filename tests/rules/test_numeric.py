import pytest
from passguard.rules.numeric import NumericOnlyRule
from passguard.results import Severity, Issue
from passguard.context import Context


class TestNumericOnlyRule:
    def test_rule_attributes(self):
        rule = NumericOnlyRule()
        assert rule.code == "numeric_only"
        assert rule.severity == Severity.HIGH

    def test_password_numeric_only(self):
        rule = NumericOnlyRule()
        context = Context()
        issue = rule.check("123456", context)
        assert isinstance(issue, Issue)
        assert issue.code == "numeric_only"
        assert "entirely numeric" in issue.message

    def test_password_has_letters(self):
        rule = NumericOnlyRule()
        context = Context()
        issue = rule.check("123abc", context)
        assert issue is None

    def test_password_has_symbols(self):
        rule = NumericOnlyRule()
        context = Context()
        issue = rule.check("123!", context)
        assert issue is None

    def test_empty_password(self):
        rule = NumericOnlyRule()
        context = Context()
        issue = rule.check("", context)
        assert issue is None  # Empty is not numeric only

    def test_single_digit(self):
        rule = NumericOnlyRule()
        context = Context()
        issue = rule.check("5", context)
        assert isinstance(issue, Issue)