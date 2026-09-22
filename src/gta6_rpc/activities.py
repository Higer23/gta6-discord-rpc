"""Safe activity and location rotation."""
from __future__ import annotations
import random,time
from dataclasses import dataclass
from typing import Callable
from .models import AppConfig,PresenceState
@dataclass
class ActivityGenerator:
    config:AppConfig
    rng:random.Random
    clock:Callable[[],float]=time.monotonic
    def choose(self,state:PresenceState,*,now:float|None=None)->None:
        state.current_activity=self.rng.choice(self.config.activities); state.current_location=self.rng.choice(self.config.locations); state.current_suffix=self.rng.choice(self.config.details_suffixes)
        current=self.clock() if now is None else now
        state.next_rotation=current+self.rng.uniform(self.config.rotation.min_seconds,self.config.rotation.max_seconds) if self.config.rotation.enabled else float("inf")
    def ensure_current(self,state:PresenceState,*,now:float|None=None)->bool:
        current=self.clock() if now is None else now
        if not state.current_activity or (self.config.rotation.enabled and current>=state.next_rotation): self.choose(state,now=current); return True
        return False
