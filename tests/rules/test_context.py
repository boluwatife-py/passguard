import pytest
from passguard.rules.context import ContextRule
from passguard.results import Severity, Issue
from passguard.context import Context


class TestContextRule:
    def test_rule_attributes(self):
        rule = ContextRule()
        assert rule.code == "contains_context"
        assert rule.severity == Severity.HIGH

    def test_password_contains_username(self):
        rule = ContextRule()
        context = Context(username="john")
        issue = rule.check("mypasswordjohn", context)
        assert isinstance(issue, Issue)
        assert issue.code == "contains_context"
        assert "personal information" in issue.message

    def test_password_contains_email(self):
        rule = ContextRule()
        context = Context(email="john@example.com")
        issue = rule.check("johnexamplecom", context)
        assert isinstance(issue, Issue)

    def test_password_contains_first_name(self):
        rule = ContextRule()
        context = Context(first_name="Jane")
        issue = rule.check("passwordjane", context)
        assert isinstance(issue, Issue)

    def test_password_contains_full_name(self):
        rule = ContextRule()
        context = Context(full_name="John Doe")
        issue = rule.check("johndoepass", context)
        assert isinstance(issue, Issue)

    def test_password_no_context_match(self):
        rule = ContextRule()
        context = Context(username="john", email="jane@test.com")
        issue = rule.check("unique_password", context)
        assert issue is None

    def test_case_insensitive_and_normalized(self):
        rule = ContextRule()
        context = Context(username="John")
        issue = rule.check("PASSWORDJOHN", context)  # Should normalize
        assert isinstance(issue, Issue)

    def test_leetspeak_normalization(self):
        rule = ContextRule()
        context = Context(username="john")
        issue = rule.check("j0hn", context)  # leetspeak for john
        assert isinstance(issue, Issue)

    def test_empty_context(self):
        rule = ContextRule()
        context = Context()
        issue = rule.check("password", context)
        assert issue is None

    def test_partial_matches_not_allowed(self):
        rule = ContextRule()
        context = Context(username="john")
        issue = rule.check("joh", context)  # partial
        assert isinstance(issue, Issue)