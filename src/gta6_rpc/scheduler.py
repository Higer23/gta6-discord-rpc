"""Drift-resistant update scheduling."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable


@dataclass
class UpdateScheduler:
    interval: float
    sleep: Callable[[float], None] = time.sleep
    monotonic: Callable[[], float] = time.monotonic
    max_catch_up_seconds: float = 5.0

    def run(self, callback: Callable[[], None], stop: Callable[[], bool]) -> None:
        if self.interval <= 0:
            raise ValueError("Scheduler interval must be greater than zero.")
        next_tick = self.monotonic()
        while not stop():
            now = self.monotonic()
            delay = next_tick - now
            if delay > 0:
                self.sleep(delay)
                continue
            callback()
            next_tick += self.interval
            now = self.monotonic()
            if now - next_tick > self.max_catch_up_seconds:
                next_tick = now + self.interval
