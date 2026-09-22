"""Interactive first-run setup."""

from __future__ import annotations

import json
from pathlib import Path

from .timer import format_duration, parse_duration


def run_setup(path: Path, *, example_path: Path) -> None:
    if not example_path.exists():
        raise FileNotFoundError(f"Missing configuration template: {example_path}")
    data = json.loads(example_path.read_text(encoding="utf-8"))
    print("
No configuration found. Let's create your configuration.
")
    client_id = input(f"Discord Client ID [{data.get('client_id', '')}]: ").strip()
    if client_id:
        data["client_id"] = client_id
    print("Played time examples: 127:43:29, 12:34:56, 12h 34m 56s")
    raw = input("Played time [keep example]: ").strip()
    if raw:
        total = parse_duration(raw)
        hours, remainder = divmod(total, 3600)
        minutes, seconds = divmod(remainder, 60)
        data["played_time"] = {"hours": hours, "minutes": minutes, "seconds": seconds}
        print(f"✓ Played time: {format_duration(total)}")
    path.write_text(json.dumps(data, indent=2) + "
", encoding="utf-8")
    print(f"✓ Configuration saved to {path}")
