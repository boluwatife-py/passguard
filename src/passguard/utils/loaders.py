import gzip
from pathlib import Path
from typing import Set


def load_common_passwords() -> Set[str]:
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

#TODO: Cache the common passwords to memory