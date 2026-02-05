"""Data loaders for PassGuard."""
import gzip
from functools import lru_cache

from pathlib import Path
from typing import Set


@lru_cache(maxsize=1)
def load_common_passwords() -> Set[str]:
    """Load common passwords from gzip file (cached)."""
    data_dir = Path(__file__).parent.parent / "data"
    file_path = data_dir / "common-passwords.txt.gz"
    passwords = set()
    try:
        with gzip.open(file_path, "rt", encoding="utf-8") as f:
            for line in f:
                password = line.strip().lower()
                if password:
                    passwords.add(password)
    except FileNotFoundError:
        pass

    return passwords

