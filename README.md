# PassGuard

A comprehensive, production-ready password validation library for Python with customizable rules, context-aware validation, and Pydantic integration.

## Features

- **🔐 Flexible Rule System**: Built-in rules for length, character requirements, common password detection, and more
- **🎯 Context-Aware Validation**: Prevent passwords containing usernames, emails, or personal information
- **📊 Rich Validation Results**: Detailed feedback with issue codes, severity levels, and validation scores
- **🎨 Customizable Policies**: Create your own validation policies or modify the default one
- **🐍 Pydantic Integration**: First-class support for Pydantic v2 models with validators and custom types
- **♻️ Pluggable Architecture**: Easy to extend with custom rules and providers
- **⚡ High Performance**: Efficient validation with minimal dependencies

## Installation

```bash
pip install passguard
```

With Pydantic support:

```bash
pip install passguard[pydantic]
```

## Quick Start

### Basic Usage

```python
from passguard import PasswordValidator

# Create a validator with default policy
validator = PasswordValidator()

# Evaluate a password
result = validator.evaluate(
    "MySecurePass123!",
    context_data={"username": "john", "email": "john@example.com"}
)

# Check results
if result.valid:
    print(f"✓ Password is valid (score: {result.score})")
else:
    print(f"✗ Password has issues:")
    for issue in result.issues:
        print(f"  - {issue.code}: {issue.message} ({issue.severity})")
```

### Custom Policy

```python
from passguard.policy import PasswordPolicy
from passguard.rules.length import MinLengthRule
from passguard.rules.character import UppercaseRule, DigitRule

# Create a custom policy
policy = PasswordPolicy()
policy.add_rule(MinLengthRule(min_length=12))
policy.add_rule(UppercaseRule())
policy.add_rule(DigitRule())

# Use it in the validator
validator = PasswordValidator(policy=policy)
result = validator.evaluate("MyPassword123")
```

### Disable Specific Rules

```python
# Disable rules you don't want to enforce
validator = PasswordValidator(
    disable_rules=["common_password", "numeric_only"]
)

result = validator.evaluate("password123")
```

### Pydantic Integration

#### With Field Validator

```python
from pydantic import BaseModel, field_validator
from passguard.integrations.pydantic import PasswordField
from passguard.policy import PasswordPolicy

policy = PasswordPolicy.default()

validator_func = PasswordField.make_validator(
    policy=policy,
    min_score=80,
    context_fields=["username", "email"]
)

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, v, info):
        return validator_func(v, info)

# Use it
try:
    user = RegisterRequest(
        username="john",
        email="john@example.com",
        password="SecurePass123!"
    )
except ValidationError as e:
    print(e)
```

#### With PasswordStr Type

```python
from pydantic import BaseModel
from passguard.integrations.pydantic import PasswordStr

class RegisterRequest(BaseModel):
    username: str
    password: PasswordStr

# Password is automatically validated
user = RegisterRequest(
    username="john",
    password="SecurePass123!"
)
```

## Built-in Rules

### Length Rules

- **`MinLengthRule`**: Enforces minimum password length (default: 8)

### Character Rules

- **`UppercaseRule`**: Requires at least one uppercase letter
- **`LowercaseRule`**: Requires at least one lowercase letter
- **`DigitRule`**: Requires at least one digit
- **`SymbolRule`**: Requires at least one special character

### Common Patterns

- **`NumericOnlyRule`**: Prevents entirely numeric passwords
- **`CommonPasswordRule`**: Checks against a list of common/weak passwords
- **`ContextRule`**: Prevents passwords containing personal information (username, email, names)

## API Reference

### PasswordValidator

Main validator class for password evaluation.

```python
validator = PasswordValidator(
    policy=None,           # Custom PasswordPolicy (default: PasswordPolicy.default())
    disable_rules=None     # List of rule codes to disable
)

result = validator.evaluate(
    password,              # str: Password to validate
    context_data=None,     # dict: User info (username, email, first_name, etc.)
    min_score=100          # int: Minimum score threshold (0-100)
)
```

### ValidationResult

Result object containing validation outcome and details.

```python
result = ValidationResult(
    valid: bool,           # Overall validation status
    score: int,            # Validation score (0-100)
    issues: List[Issue]    # List of validation issues
)

# Methods
result.to_dict()          # Serialize to JSON-safe dict
result.has_critical_issues  # Property: True if any CRITICAL issues
result.issue_codes        # Property: Set of issue codes
```

### Issue

Individual validation issue.

```python
issue = Issue(
    code: str,            # Machine-readable identifier
    message: str,         # Human-readable message
    severity: Severity    # LOW, MEDIUM, HIGH, or CRITICAL
)

issue.to_dict()          # Serialize to JSON-safe dict
```

### PasswordPolicy

Configuration for which rules to enforce.

```python
# Get default policy
policy = PasswordPolicy.default()

# Create custom policy
policy = PasswordPolicy()

# Manage rules
policy.add_rule(rule)          # Add a rule
policy.remove_rule(RuleClass)  # Remove all rules of a type
policy.get_rule(RuleClass)     # Get rule instance by type
```

### Context

Normalized user context used in validation.

```python
context = Context(
    username=None,
    email=None,
    first_name=None,
    second_name=None,
    full_name=None
)

# Create from dictionary
context = Context.from_mapping({
    "username": "john",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
})
```

## Validation Scores

PassGuard calculates a validation score based on the percentage of rules passed:

- **100**: All rules passed
- **75**: 75% of rules passed
- **50**: 50% of rules passed
- **0**: No rules passed

The `min_score` parameter can be used to enforce a minimum threshold.

## Severity Levels

Issues are categorized by severity:

- **LOW**: Minor suggestions (e.g., could be stronger)
- **MEDIUM**: Standard requirement not met (e.g., missing uppercase)
- **HIGH**: Important security requirement not met (e.g., common password)
- **CRITICAL**: Must-have requirement failed (validation fails if present)

## Creating Custom Rules

Extend the `PasswordRule` base class:

```python
from passguard.rules.base import PasswordRule
from passguard.results import Issue, Severity

class MyCustomRule(PasswordRule):
    code = "my_custom_rule"
    severity = Severity.MEDIUM

    def __init__(self, severity=None):
        super().__init__(severity)
        # Your initialization

    def check(self, password: str, context) -> Issue | None:
        """
        Validate password against this rule.

        Returns:
            Issue if validation fails, None if passes
        """
        if some_condition(password):
            return Issue(
                code=self.code,
                message="Your error message",
                severity=self.severity
            )
        return None

# Use it
policy = PasswordPolicy()
policy.add_rule(MyCustomRule())
```

## Text Normalization

PassGuard normalizes text for comparison in context-aware rules:

1. **Lowercase**: All text converted to lowercase
2. **Whitespace stripping**: Leading/trailing spaces removed
3. **Leetspeak substitution**: `0→o`, `1→l`, `3→e`, `4→a`, `5→s`, `7→t`, `@→a`, `$→s`
4. **Non-alphanumeric removal**: Special characters stripped

This ensures that variations of personal information are caught (e.g., "J0hn" matches "john").

## Configuration

The default policy enforces:

- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- At least one special character
- Cannot be entirely numeric
- Cannot be a common/weak password
- Cannot contain personal information

Customize any of these by creating your own policy.

## Examples

### Strict Policy

```python
from passguard.policy import PasswordPolicy
from passguard.rules.length import MinLengthRule
from passguard.rules.character import UppercaseRule, LowercaseRule, DigitRule, SymbolRule

policy = PasswordPolicy()
policy.add_rule(MinLengthRule(min_length=16))
policy.add_rule(UppercaseRule())
policy.add_rule(LowercaseRule())
policy.add_rule(DigitRule())
policy.add_rule(SymbolRule())

validator = PasswordValidator(policy=policy)
```

### Lenient Policy

```python
from passguard.policy import PasswordPolicy
from passguard.rules.length import MinLengthRule
from passguard.rules.context import ContextRule

policy = PasswordPolicy()
policy.add_rule(MinLengthRule(min_length=6))
policy.add_rule(ContextRule())

validator = PasswordValidator(policy=policy)
```

### API Endpoint with Validation

```python
from fastapi import FastAPI, HTTPException
from passguard import PasswordValidator

app = FastAPI()
validator = PasswordValidator()

@app.post("/register")
def register(username: str, password: str):
    result = validator.evaluate(
        password,
        context_data={"username": username}
    )

    if not result.valid:
        raise HTTPException(
            status_code=400,
            detail={
                "valid": result.valid,
                "score": result.score,
                "issues": [issue.to_dict() for issue in result.issues]
            }
        )

    return {"message": "User registered successfully"}
```

## Testing

Run the test suite:

```bash
pytest tests/
```

With coverage:

```bash
pytest tests/ --cov=src/passguard
```

## Project Structure

```
passguard/
├── src/passguard/
│   ├── __init__.py
│   ├── validator.py          # Main PasswordValidator class
│   ├── policy.py             # PasswordPolicy configuration
│   ├── results.py            # ValidationResult, Issue, Severity
│   ├── context.py            # User context normalization
│   ├── errors.py             # Custom exceptions
│   ├── rules/                # Built-in password rules
│   │   ├── base.py           # PasswordRule base class
│   │   ├── length.py         # MinLengthRule
│   │   ├── character.py      # Character requirement rules
│   │   ├── numeric.py        # NumericOnlyRule
│   │   ├── common.py         # CommonPasswordRule
│   │   └── context.py        # ContextRule
│   ├── integrations/         # Framework integrations
│   │   └── pydantic.py       # Pydantic v2 integration
│   ├── providers/            # External data providers
│   ├── utils/                # Utility functions
│   │   ├── loaders.py        # Data loading (gzip)
│   │   └── normalize.py      # Text normalization
│   └── data/                 # Data files
│       └── common-passwords.txt.gz
└── tests/                    # Test suite
```

## Performance

PassGuard is optimized for performance:

- Common password checks use efficient set lookups
- Lazy loading of data files with caching
- Minimal object allocation
- Pure Python with no C extensions required

Typical validation takes < 1ms on modern hardware.

## Contributing

Contributions are welcome! Please ensure:

1. All tests pass: `pytest tests/`
2. Code is properly typed: `mypy src/passguard/`
3. Code is well-documented with docstrings
4. New rules include comprehensive tests

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

## Support

For issues, feature requests, or questions, please open an issue on GitHub.

---

**Built with ❤️ for secure password validation**
