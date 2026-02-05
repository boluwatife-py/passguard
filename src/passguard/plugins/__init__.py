"""Plugin system for PassGuard.

Allows registration and discovery of custom rules and providers.

Usage:
    from passguard.plugins import register_rule
    
    @register_rule
    class MyCustomRule(PasswordRule):
        code = "my_rule"
        def check(self, password, context):
            ...
"""

PLUGINS: list[type] = []


def register_rule(rule_class: type) -> type:
    """Register a custom rule to be used in policies.
    
    Args:
        rule_class: A class inheriting from PasswordRule
        
    Returns:
        The rule class (allows use as decorator)
    """
    PLUGINS.append(rule_class)
    return rule_class


def get_registered_rules() -> list[type]:
    """Get all registered plugin rules."""
    return PLUGINS.copy()


__all__ = [
    "register_rule",
    "get_registered_rules",
    "PLUGINS",
]
