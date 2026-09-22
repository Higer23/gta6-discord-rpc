"""Domain models used by the application."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class PlayedTime:
    total_seconds: int
    def __post_init__(self) -> None:
        if self.total_seconds < 0:
            raise ValueError("Played time cannot be negative.")


@dataclass(frozen=True)
class RotationConfig:
    enabled: bool = True
    min_seconds: float = 60.0
    max_seconds: float = 120.0


@dataclass(frozen=True)
class AssetConfig:
    large_image: str
    large_text: str = ""
    small_image: str | None = None
    small_text: str = ""


@dataclass(frozen=True)
class ButtonConfig:
    label: str
    url: str


@dataclass(frozen=True)
class LoggingConfig:
    level: str = "INFO"
    file: str = "logs/gta6_rpc.log"
    max_bytes: int = 1_048_576
    backup_count: int = 3


@dataclass(frozen=True)
class TerminalConfig:
    quiet: bool = False


@dataclass(frozen=True)
class AppConfig:
    client_id: str
    played_time: PlayedTime
    interactive_setup: bool
    update_interval: float
    rotation: RotationConfig
    assets: AssetConfig
    buttons: tuple[ButtonConfig, ...]
    terminal: TerminalConfig
    logging: LoggingConfig
    activities: tuple[str, ...]
    locations: tuple[str, ...]
    details_suffixes: tuple[str, ...]


@dataclass
class PresenceState:
    total_played_seconds: int
    start_timestamp: int
    current_activity: str = ""
    current_location: str = ""
    current_suffix: str = ""
    next_rotation: float = 0.0
    connected: bool = False
    last_error: str = ""


@dataclass(frozen=True)
class PresencePayload:
    data: dict[str, Any] = field(default_factory=dict)
