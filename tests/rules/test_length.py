import pytest
from passguard.rules.length import MinLengthRule
from passguard.results import Severity, Issue
from passguard.context import Context


class TestMinLengthRule:
    def test_rule_attributes(self):
        rule = MinLengthRule()
        assert rule.code == "too_short"
        assert rule.severity == Severity.MEDIUM

    def test_custom_severity(self):
        rule = MinLengthRule(severity=Severity.HIGH)
        assert rule.severity == Severity.HIGH

    def test_password_too_short(self):
        rule = MinLengthRule(min_length=8)
        context = Context()
        issue = rule.check("short", context)
        assert isinstance(issue, Issue)
        assert issue.code == "too_short"
        assert "8 characters" in issue.message
        assert issue.severity == Severity.MEDIUM

    def test_password_meets_minimum(self):
        rule = MinLengthRule(min_length=8)
        context = Context()
        issue = rule.check("longenough", context)
        assert issue is None

    def test_password_exactly_minimum(self):
        rule = MinLengthRule(min_length=8)
        context = Context()
        issue = rule.check("12345678", context)
        assert issue is None

    def test_custom_min_length(self):
        rule = MinLengthRule(min_length=12)
        context = Context()
        issue = rule.check("short", context)
        assert isinstance(issue, Issue)
        assert "12 characters" in issue.message