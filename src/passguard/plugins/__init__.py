PLUGINS: list[type] = []

def register_rule(rule_class: type):
    """Register a custom rule to be used in policies."""
    PLUGINS.append(rule_class)
