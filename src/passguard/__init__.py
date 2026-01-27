# In passguard/__init__.py
# only import pydantic integration if available
try:
    from .integrations import pydantic
except ImportError:
    pass
