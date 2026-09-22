"""Drift-resistant elapsed time and Discord timestamp utilities."""
from __future__ import annotations
import re, time

def format_duration(seconds: int | float) -> str:
    total=max(0,int(seconds)); h,r=divmod(total,3600); m,s=divmod(r,60)
    return f"{h}h {m:02d}m {s:02d}s" if h else (f"{m}m {s:02d}s" if m else f"{s}s")

def parse_duration(raw: str) -> int:
    raw=raw.strip().lower()
    if not raw: raise ValueError("Time is empty.")
    if ":" in raw:
        p=raw.split(":")
        if not all(x.isdigit() for x in p): raise ValueError("Use hh:mm:ss or mm:ss.")
        v=list(map(int,p))
        if len(v)==3:
            h,m,s=v
            if m>=60 or s>=60: raise ValueError("Minutes and seconds must be below 60.")
            return h*3600+m*60+s
        if len(v)==2:
            m,s=v
            if s>=60: raise ValueError("Seconds must be below 60.")
            return m*60+s
        raise ValueError("Use hh:mm:ss or mm:ss.")
    matches=re.findall(r"(\d+)\s*([hms])",raw)
    if matches and "".join(v+u for v,u in matches)==raw.replace(" ",""):
        total=0; seen=set()
        for v,u in matches:
            if u in seen: raise ValueError("Do not repeat h, m, or s units.")
            seen.add(u); total+=int(v)*{"h":3600,"m":60,"s":1}[u]
        return total
    if raw.isdigit(): return int(raw)
    raise ValueError("Invalid time. Examples: 127:43:29, 12:34:56, 12h 34m 56s")

class MonotonicElapsedTimer:
    def __init__(self, initial_elapsed:int, *, monotonic=time.monotonic):
        if initial_elapsed<0: raise ValueError("Initial elapsed time cannot be negative.")
        self.initial_elapsed=int(initial_elapsed); self._clock=monotonic; self._origin=monotonic()
    def elapsed_float(self)->float: return max(0.0,self.initial_elapsed+self._clock()-self._origin)
    def elapsed(self)->int: return int(self.elapsed_float())
    @staticmethod
    def discord_start_timestamp(initial_elapsed:int, *, wall_time=time.time)->int:
        if initial_elapsed<0: raise ValueError("Initial elapsed time cannot be negative.")
        return int(wall_time())-int(initial_elapsed)
