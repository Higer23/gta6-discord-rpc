"""Monotonic timer and Discord timestamp helpers."""

from __future__ import annotations

import re
import time

_DURATION_RE = re.compile(r"^(?:(\d+)h\s*)?(?:(\d+)m\s*)?(?:(\d+)s\s*)?$")


def format_duration(seconds: int | float) -> str:
    total = max(0, int(seconds))
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}h {minutes:02d}m {secs:02d}s"
    if minutes:
        return f"{minutes}m {secs:02d}s"
    return f"{secs}s"


def parse_duration(raw: str) -> int:
    raw = raw.strip().lower()
    if not raw:
        raise ValueError("Time is empty.")
    if ":" in raw:
        parts = raw.split(":")
        if not all(part.isdigit() for part in parts):
            raise ValueError("Use hh:mm:ss or mm:ss.")
        values = [int(part) for part in parts]
        if len(values) == 3:
            h, m, s = values
            if m >= 60 or s >= 60:
                raise ValueError("Minutes and seconds must be below 60.")
            return h * 3600 + m * 60 + s
        if len(values) == 2:
            m, s = values
            if s >= 60:
                raise ValueError("Seconds must be below 60.")
            return m * 60 + s
        raise ValueError("Use hh:mm:ss or mm:ss.")
    matches = re.findall(r"(\d+)\s*([hms])", raw)
    if matches and "".join(value + unit for value, unit in matches) == raw.replace(" ", ""):
        total = 0
        seen: set[str] = set()
        for value, unit in matches:
            if unit in seen:
                raise ValueError("Do not repeat h, m, or s units.")
            seen.add(unit)
            total += int(value) * {"h": 3600, "m": 60, "s": 1}[unit]
        return total
    if raw.isdigit():
        return int(raw)
    raise ValueError("Invalid time. Examples: 12:34:56, 12:34, 12h 34m 56s")


class MonotonicElapsedTimer:
    def __init__(self, initial_elapsed: int, *, monotonic=time.monotonic) -> None:
        if initial_elapsed < 0:
            raise ValueError("Initial elapsed time cannot be negative.")
        self.initial_elapsed = int(initial_elapsed)
        self._monotonic = monotonic
        self._origin = monotonic()

    def elapsed(self) -> int:
        return max(0, int(self.initial_elapsed + (self._monotonic() - self._origin)))

    @staticmethod
    def discord_start_timestamp(initial_elapsed: int, *, wall_time=time.time) -> int:
        if initial_elapsed < 0:
            raise ValueError("Initial elapsed time cannot be negative.")
        return int(wall_time()) - int(initial_elapsed)
