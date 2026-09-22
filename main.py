"""Entry point for the GTA VI Discord Rich Presence application."""

from __future__ import annotations

import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from gta6_rpc.app import run


if __name__ == "__main__":
    run()
