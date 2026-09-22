"""Configuration and user-input validation."""

from __future__ import annotations

import re
from urllib.parse import urlparse

from .models import AppConfig

ASSET_RE = re.compile(r"^[A-Za-z0-9_.-]{1,128}$")
LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


def validate_config(config: AppConfig) -> list[str]:
    errors: list[str] = []
    if not config.client_id or not config.client_id.isdigit():
        errors.append("client_id must be a numeric Discord application ID.")
    if config.update_interval <= 0:
        errors.append("update_interval must be greater than 0 seconds.")
    if config.rotation.min_seconds <= 0 or config.rotation.max_seconds <= 0:
        errors.append("rotation times must be greater than 0 seconds.")
    if config.rotation.min_seconds > config.rotation.max_seconds:
        errors.append("rotation_min_seconds must be smaller than rotation_max_seconds.")
    if not config.assets.large_image:
        errors.append("assets.large_image cannot be empty.")
    elif not ASSET_RE.fullmatch(config.assets.large_image):
        errors.append("assets.large_image contains invalid characters.")
    if config.assets.small_image and not ASSET_RE.fullmatch(config.assets.small_image):
        errors.append("assets.small_image contains invalid characters.")
    if not config.activities:
        errors.append("activities must contain at least one activity.")
    if not config.locations:
        errors.append("locations must contain at least one location.")
    if not config.details_suffixes:
        errors.append("details_suffixes must contain at least one value.")
    for index, button in enumerate(config.buttons, 1):
        parsed = urlparse(button.url)
        if not button.label.strip():
            errors.append(f"buttons[{index}].label cannot be empty.")
        if len(button.label) > 32:
            errors.append(f"buttons[{index}].label must be 32 characters or fewer.")
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            errors.append(f"buttons[{index}].url is not a valid HTTP(S) URL.")
    if len(config.buttons) > 2:
        errors.append("Discord Rich Presence supports at most 2 buttons.")
    if config.logging.level not in LOG_LEVELS:
        errors.append(f"logging.level must be one of: {', '.join(sorted(LOG_LEVELS))}.")
    if config.logging.max_bytes <= 0:
        errors.append("logging.max_bytes must be greater than 0.")
    if config.logging.backup_count < 0:
        errors.append("logging.backup_count cannot be negative.")
    return errors


def validate_or_raise(config: AppConfig) -> None:
    errors = validate_config(config)
    if errors:
        raise ValueError("Configuration error:
" + "
".join(f" - {item}" for item in errors))
