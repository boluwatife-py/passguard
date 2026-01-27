import pytest
from pydantic import BaseModel, ValidationError, field_validator
from passguard.integrations.pydantic import PasswordField, PasswordStr
from passguard.policy import PasswordPolicy
from passguard.rules.length import MinLengthRule


class TestPasswordField:
    def test_password_field_creation(self):
        field = PasswordField()
        assert isinstance(field.policy, PasswordPolicy)
        assert field.min_score == 100

    def test_password_field_with_custom_policy(self):
        policy = PasswordPolicy()
        policy.add_rule(MinLengthRule(min_length=5))
        field = PasswordField(policy=policy, min_score=50)
        assert field.policy == policy
        assert field.min_score == 50

    def test_valid_password(self):
        validator_func = PasswordField.make_validator()

        class Model(BaseModel):
            username: str
            password: str

            @field_validator('password')
            @classmethod
            def validate_password(cls, v, info):
                return validator_func(v, info)

        model = Model(username="user", password="StrongPass123!")
        assert model.password == "StrongPass123!"

    def test_invalid_password(self):
        validator_func = PasswordField.make_validator()

        class Model(BaseModel):
            username: str
            password: str

            @field_validator('password')
            @classmethod
            def validate_password(cls, v, info):
                return validator_func(v, info)

        with pytest.raises(ValidationError) as exc_info:
            Model(username="user", password="weak")

        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert "Password must be at least 8 characters long" in str(errors[0]['msg'])

    def test_password_with_context(self):
        validator_func = PasswordField.make_validator(context_fields=["username"])

        class Model(BaseModel):
            username: str
            password: str

            @field_validator('password')
            @classmethod
            def validate_password(cls, v, info):
                return validator_func(v, info)

        with pytest.raises(ValidationError):
            Model(username="user", password="mypassworduser")

    def test_custom_policy_respected(self):
        """Test that custom policy is actually used."""
        test_policy = PasswordPolicy()
        test_policy.add_rule(MinLengthRule(min_length=5))

        validator_func = PasswordField.make_validator(policy=test_policy)

        class Model(BaseModel):
            password: str

            @field_validator('password')
            @classmethod
            def validate_password(cls, v, info):
                return validator_func(v, info)

        # With custom policy (only length rule), short password should pass
        model = Model(password="valid")
        assert model.password == "valid"

    def test_min_score_enforcement(self):
        """Test that min_score threshold is enforced."""
        test_policy = PasswordPolicy()
        test_policy.add_rule(MinLengthRule(min_length=5))

        validator_func = PasswordField.make_validator(policy=test_policy, min_score=100)

        class Model(BaseModel):
            password: str

            @field_validator('password')
            @classmethod
            def validate_password(cls, v, info):
                return validator_func(v, info)

        # Password passes the rule (score=100), meets min_score
        model = Model(password="valid")
        assert model.password == "valid"

    def test_context_fields_extraction(self):
        """Test that context fields are properly extracted."""
        test_policy = PasswordPolicy()
        test_policy.add_rule(MinLengthRule(min_length=5))

        validator_func = PasswordField.make_validator(
            policy=test_policy,
            context_fields=["username", "email"]
        )

        class Model(BaseModel):
            username: str
            email: str
            password: str

            @field_validator('password')
            @classmethod
            def validate_password(cls, v, info):
                return validator_func(v, info)

        # Password doesn't contain context info - should pass
        model = Model(username="john", email="john@test.com", password="validpw")
        assert model.password == "validpw"


class TestPasswordStr:
    def test_password_str_valid(self):
        class Model(BaseModel):
            password: PasswordStr

        model = Model(password="StrongPass123!")
        assert isinstance(model.password, PasswordStr)
        assert model.password == "StrongPass123!"

    def test_password_str_invalid(self):
        class Model(BaseModel):
            password: PasswordStr

        with pytest.raises(ValidationError):
            Model(password="weak")