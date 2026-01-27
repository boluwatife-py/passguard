import pytest
from unittest.mock import patch
from passguard.rules.common import CommonPasswordRule
from passguard.results import Severity, Issue
from passguard.context import Context


class TestCommonPasswordRule:
    def test_rule_attributes(self):
        rule = CommonPasswordRule()
        assert rule.code == "common_password"
        assert rule.severity == Severity.HIGH

    @patch('passguard.rules.common.load_common_passwords')
    def test_password_is_common(self, mock_load):
        mock_load.return_value = {"password", "123456", "qwerty"}
        rule = CommonPasswordRule()
        context = Context()
        issue = rule.check("password", context)
        assert isinstance(issue, Issue)
        assert issue.code == "common_password"
        assert "too common" in issue.message

    @patch('passguard.rules.common.load_common_passwords')
    def test_password_not_common(self, mock_load):
        mock_load.return_value = {"password", "123456"}
        rule = CommonPasswordRule()
        context = Context()
        issue = rule.check("unique_password", context)
        assert issue is None


    @patch('passguard.rules.common.load_common_passwords')
    def test_empty_common_list(self, mock_load):
        mock_load.return_value = set()
        rule = CommonPasswordRule()
        context = Context()
        issue = rule.check("password", context)
        assert issue is None