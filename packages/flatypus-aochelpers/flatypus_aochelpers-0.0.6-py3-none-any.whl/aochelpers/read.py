import sys
from pathlib import Path


def read(relative="", filename="input.txt") -> str:
    """Reads a file from the same directory as the file this function is called from."""
    file = sys.argv[0]
    current_dir = Path(file).parent
    path = current_dir / relative / filename
    with open(path, 'r') as f:
        return f.read()
