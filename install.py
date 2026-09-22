"""Small cross-platform dependency installer for first-time users."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    requirements = Path(__file__).with_name("requirements.txt")
    command = [sys.executable, "-m", "pip", "install", "-r", str(requirements)]
    print("Installing GTA VI RPC dependencies...")
    return subprocess.call(command)


if __name__ == "__main__":
    raise SystemExit(main())
