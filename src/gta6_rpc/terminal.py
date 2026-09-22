"""HIGER terminal presentation."""
from __future__ import annotations
import sys,time
from dataclasses import dataclass
from .models import AppConfig,PresenceState
from .timer import format_duration
@dataclass
class TerminalUI:
 mode:str="normal";refresh_hz:float=1
 def _show(self):return self.mode!="quiet"
 def banner(self):
  if self._show():print("\n╔══════════════════════════════════════════╗\n║             HIGER RPC SYSTEM             ║\n║       GTA VI DISCORD RICH PRESENCE       ║\n╚══════════════════════════════════════════╝")
 def info(self,s):
  if self._show():print(s)
 def status(self,c:AppConfig,s:PresenceState):
  if self._show():print(f"\rHIGER | {format_duration(max(0,int(time.time())-s.start_timestamp))} | {s.current_activity} | {s.current_location}    ",end="",flush=True)
 def error(self,s):print(f"✗ HIGER: {s}",file=sys.stderr)
 def stop(self):
  if self._show():print("\n✓ HIGER stopped safely.")
