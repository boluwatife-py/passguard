"""Utility functions for PassGuard.

Modules:
    - loaders: Data loading utilities (gzip decompression, caching)
    - normalize: Text normalization for comparison
"""

from .loaders import load_common_passwords
from .normalize import normalize_text, extract_email_local_part

__all__ = [
    "load_common_passwords",
    "normalize_text",
    "extract_email_local_part",
]
