import pytest
from passguard.results import Severity, Issue, ValidationResult


class TestSeverity:
    def test_severity_values(self):
        assert Severity.LOW == "low"
        assert Severity.MEDIUM == "medium"
        assert Severity.HIGH == "high"
        assert Severity.CRITICAL == "critical"

    def test_severity_enum_members(self):
        assert len(Severity) == 4
        assert all(isinstance(s, str) for s in Severity)


class TestIssue:
    def test_issue_creation(self):
        issue = Issue(
            code="test_code",
            message="Test message",
            severity=Severity.MEDIUM
        )
        assert issue.code == "test_code"
        assert issue.message == "Test message"
        assert issue.severity == Severity.MEDIUM

    def test_issue_frozen(self):
        issue = Issue("code", "msg", Severity.LOW)
        with pytest.raises(AttributeError):
            issue.code = "new_code" #type: ignore

    def test_issue_to_dict(self):
        issue = Issue("test", "Test issue", Severity.HIGH)
        expected = {
            "code": "test",
            "message": "Test issue",
            "severity": "high"
        }
        assert issue.to_dict() == expected


class TestValidationResult:
    def test_validation_result_creation(self):
        result = ValidationResult(valid=True, score=85, issues=[])
        assert result.valid is True
        assert result.score == 85
        assert result.issues == []

    def test_score_validation(self):
        with pytest.raises(ValueError, match="score must be between 0 and 100"):
            ValidationResult(valid=True, score=150, issues=[])

        with pytest.raises(ValueError, match="score must be between 0 and 100"):
            ValidationResult(valid=True, score=-10, issues=[])

    def test_valid_with_critical_issues(self):
        issue = Issue("critical", "Critical issue", Severity.CRITICAL)
        with pytest.raises(ValueError, match="valid=True result cannot contain CRITICAL issues"):
            ValidationResult(valid=True, score=50, issues=[issue])

    def test_has_critical_issues_property(self):
        result = ValidationResult(valid=False, score=0, issues=[
            Issue("low", "Low", Severity.LOW),
            Issue("high", "High", Severity.HIGH)
        ])
        assert not result.has_critical_issues

        result_critical = ValidationResult(valid=False, score=0, issues=[
            Issue("critical", "Critical", Severity.CRITICAL)
        ])
        assert result_critical.has_critical_issues

    def test_issue_codes_property(self):
        issues = [
            Issue("code1", "Msg1", Severity.LOW),
            Issue("code2", "Msg2", Severity.MEDIUM),
            Issue("code1", "Msg3", Severity.HIGH)  # duplicate code
        ]
        result = ValidationResult(valid=False, score=0, issues=issues)
        assert result.issue_codes == {"code1", "code2"}

    def test_to_dict(self):
        issues = [
            Issue("test", "Test issue", Severity.MEDIUM)
        ]
        result = ValidationResult(valid=False, score=75, issues=issues)
        expected = {
            "valid": False,
            "score": 75,
            "issues": [
                {
                    "code": "test",
                    "message": "Test issue",
                    "severity": "medium"
                }
            ]
        }
        assert result.to_dict() == expected

    def test_from_issues_no_critical(self):
        issues = [
            Issue("low", "Low", Severity.LOW),
            Issue("med", "Medium", Severity.MEDIUM)
        ]
        result = ValidationResult.from_issues(issues, score=80, min_score=70)
        assert result.valid is True
        assert result.score == 80
        assert len(result.issues) == 2

    def test_from_issues_with_critical(self):
        issues = [
            Issue("critical", "Critical", Severity.CRITICAL)
        ]
        result = ValidationResult.from_issues(issues, score=50, min_score=0)
        assert result.valid is False
        assert result.score == 50

    def test_from_issues_below_min_score(self):
        issues = []
        result = ValidationResult.from_issues(issues, score=60, min_score=70)
        assert result.valid is False
        assert result.score == 60