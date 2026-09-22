"""Configuration loading and first-run setup."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import AppConfig, AssetConfig, ButtonConfig, LoggingConfig, PlayedTime, RotationConfig, TerminalConfig

BASE_DIR = Path(__file__).resolve().parents[2]
CONFIG_PATH = BASE_DIR / "config.json"
EXAMPLE_PATH = BASE_DIR / "config.json.example"


def _duration_from_parts(data: dict[str, Any]) -> int:
    try:
        hours = int(data.get("hours", 0))
        minutes = int(data.get("minutes", 0))
        seconds = int(data.get("seconds", 0))
    except (TypeError, ValueError) as exc:
        raise ValueError("played_time values must be integers.") from exc
    if min(hours, minutes, seconds) < 0:
        raise ValueError("played_time values cannot be negative.")
    return hours * 3600 + minutes * 60 + seconds


def load_raw_config(path: Path = CONFIG_PATH) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Configuration JSON is invalid at line {exc.lineno}, column {exc.colno}.") from exc
    if not isinstance(data, dict):
        raise ValueError("Configuration root must be a JSON object.")
    return data


def save_default_config(path: Path = CONFIG_PATH) -> None:
    if path.exists():
        return
    path.write_text(EXAMPLE_PATH.read_text(encoding="utf-8"), encoding="utf-8")


def build_config(data: dict[str, Any]) -> AppConfig:
    played = data.get("played_time", {})
    rotation = data.get("activity_rotation", {})
    assets = data.get("assets", {})
    terminal = data.get("terminal", {})
    logging_data = data.get("logging", {})
    buttons = tuple(
        ButtonConfig(str(item.get("label", "")), str(item.get("url", "")))
        for item in data.get("buttons", [])
        if isinstance(item, dict)
    )
    return AppConfig(
        client_id=str(data.get("client_id", "")).strip(),
        played_time=PlayedTime(_duration_from_parts(played)),
        interactive_setup=bool(data.get("interactive_setup", True)),
        update_interval=float(data.get("update_interval", 1.0)),
        rotation=RotationConfig(
            enabled=bool(rotation.get("enabled", True)),
            min_seconds=float(rotation.get("min_seconds", 60)),
            max_seconds=float(rotation.get("max_seconds", 120)),
        ),
        assets=AssetConfig(
            large_image=str(assets.get("large_image", "")).strip(),
            large_text=str(assets.get("large_text", "")),
            small_image=str(assets["small_image"]).strip() if assets.get("small_image") else None,
            small_text=str(assets.get("small_text", "")),
        ),
        buttons=buttons,
        terminal=TerminalConfig(quiet=bool(terminal.get("quiet", False))),
        logging=LoggingConfig(
            level=str(logging_data.get("level", "INFO")).upper(),
            file=str(logging_data.get("file", "logs/gta6_rpc.log")),
            max_bytes=int(logging_data.get("max_bytes", 1_048_576)),
            backup_count=int(logging_data.get("backup_count", 3)),
        ),
        activities=tuple(str(x).strip() for x in data.get("activities", [])),
        locations=tuple(str(x).strip() for x in data.get("locations", [])),
        details_suffixes=tuple(str(x).strip() for x in data.get("details_suffixes", [])),
    )


def load_config(path: Path = CONFIG_PATH) -> AppConfig:
    return build_config(load_raw_config(path))
