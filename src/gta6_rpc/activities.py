"""Activity selection and rotation scheduling."""

from __future__ import annotations

import random
import time
from dataclasses import dataclass

from .models import AppConfig, PresenceState


@dataclass
class ActivityGenerator:
    config: AppConfig
    rng: random.Random = random.Random()

    def choose(self, state: PresenceState, *, now: float | None = None) -> None:
        state.current_activity = self.rng.choice(self.config.activities)
        state.current_location = self.rng.choice(self.config.locations)
        state.current_suffix = self.rng.choice(self.config.details_suffixes)
        current = time.monotonic() if now is None else now
        if self.config.rotation.enabled:
            delay = self.rng.uniform(self.config.rotation.min_seconds, self.config.rotation.max_seconds)
            state.next_rotation = current + delay
        else:
            state.next_rotation = float("inf")

    def ensure_current(self, state: PresenceState, *, now: float | None = None) -> None:
        current = time.monotonic() if now is None else now
        if not state.current_activity or (self.config.rotation.enabled and current >= state.next_rotation):
            self.choose(state, now=current)
