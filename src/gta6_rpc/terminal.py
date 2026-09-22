"""Human-friendly terminal output."""

from __future__ import annotations

import sys
import time
from dataclasses import dataclass

from .models import AppConfig, PresenceState
from .timer import format_duration


@dataclass
class TerminalUI:
    quiet: bool = False

    def print(self, message: str = "") -> None:
        if not self.quiet:
            print(message)

    def banner(self) -> None:
        self.print()
        self.print("╔══════════════════════════════════════════╗")
        self.print("║       GTA VI DISCORD RICH PRESENCE       ║")
        self.print("╚══════════════════════════════════════════╝")

    def status(self, config: AppConfig, state: PresenceState) -> None:
        if self.quiet:
            return
        line = (
            f"⏱ {format_duration(max(0, int(time.time()) - state.start_timestamp))}"
            f" | 🎮 {state.current_activity}"
            f" | 📍 {state.current_location}"
        )
        print("" + " " * 110 + "" + line, end="", flush=True)

    def stop(self) -> None:
        if not self.quiet:
            print()
            print("✓ RPC closed safely.")

    def error(self, message: str) -> None:
        if not self.quiet:
            print(f"✗ {message}", file=sys.stderr)

    def configuration_summary(self, config: AppConfig) -> None:
        self.print("✓ Configuration loaded")
        self.print(f"  Update interval: {config.update_interval:g}s")
        self.print("  Rotation: " + ("enabled" if config.rotation.enabled else "disabled"))
