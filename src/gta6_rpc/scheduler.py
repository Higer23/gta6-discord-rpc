"""Interruptible drift-resistant scheduler."""
from __future__ import annotations
import time
from dataclasses import dataclass
from threading import Event
from typing import Callable
@dataclass
class UpdateScheduler:
    interval:float; stop_event:Event; clock:Callable[[],float]=time.monotonic; max_catch_up:float=5.0
    def run(self,callback:Callable[[],None])->None:
        if self.interval<=0:raise ValueError("Scheduler interval must be greater than zero.")
        next_tick=self.clock()
        while not self.stop_event.is_set():
            delay=next_tick-self.clock()
            if delay>0:self.stop_event.wait(delay);continue
            callback();next_tick+=self.interval;now=self.clock()
            if now-next_tick>self.max_catch_up:next_tick=now+self.interval
