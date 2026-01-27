import pytest
from passguard.rules.character import UppercaseRule, LowercaseRule, DigitRule, SymbolRule
from passguard.results import Severity, Issue
from passguard.context import Context


class TestUppercaseRule:
    def test_rule_attributes(self):
        rule = UppercaseRule()
        assert rule.code == "missing_uppercase"
        assert rule.severity == Severity.MEDIUM

    def test_password_missing_uppercase(self):
        rule = UppercaseRule()
        context = Context()
        issue = rule.check("lowercaseonly", context)
        assert isinstance(issue, Issue)
        assert issue.code == "missing_uppercase"
        assert "uppercase letter" in issue.message

    def test_password_has_uppercase(self):
        rule = UppercaseRule()
        context = Context()
        issue = rule.check("HasUpper", context)
        assert issue is None


class TestLowercaseRule:
    def test_rule_attributes(self):
        rule = LowercaseRule()
        assert rule.code == "missing_lowercase"
        assert rule.severity == Severity.MEDIUM

    def test_password_missing_lowercase(self):
        rule = LowercaseRule()
        context = Context()
        issue = rule.check("UPPERCASEONLY", context)
        assert isinstance(issue, Issue)
        assert issue.code == "missing_lowercase"
        assert "lowercase letter" in issue.message

    def test_password_has_lowercase(self):
        rule = LowercaseRule()
        context = Context()
        issue = rule.check("hasLower", context)
        assert issue is None


class TestDigitRule:
    def test_rule_attributes(self):
        rule = DigitRule()
        assert rule.code == "missing_digit"
        assert rule.severity == Severity.MEDIUM

    def test_password_missing_digit(self):
        rule = DigitRule()
        context = Context()
        issue = rule.check("NoDigits", context)
        assert isinstance(issue, Issue)
        assert issue.code == "missing_digit"
        assert "digit" in issue.message

    def test_password_has_digit(self):
        rule = DigitRule()
        context = Context()
        issue = rule.check("Has1Digit", context)
        assert issue is None


class TestSymbolRule:
    def test_rule_attributes(self):
        rule = SymbolRule()
        assert rule.code == "missing_symbol"
        assert rule.severity == Severity.MEDIUM

    def test_password_missing_symbol(self):
        rule = SymbolRule()
        context = Context()
        issue = rule.check("NoSymbols123", context)
        assert isinstance(issue, Issue)
        assert issue.code == "missing_symbol"
        assert "symbol" in issue.message

    def test_password_has_symbol(self):
        rule = SymbolRule()
        context = Context()
        issue = rule.check("Has!Symbol", context)
        assert issue is None

    def test_various_symbols(self):
        rule = SymbolRule()
        context = Context()
        symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        for symbol in symbols:
            issue = rule.check(f"password{symbol}", context)
            assert issue is None, f"Symbol {symbol} should be accepted"