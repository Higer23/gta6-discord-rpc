"""Discord Rich Presence payload generation."""

from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

from .models import AppConfig, PresenceState


class PresenceBuilder:
    def __init__(self, config: AppConfig) -> None:
        self.config = config

    def build(self, state: PresenceState) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "state": f"{state.current_location} • {state.current_suffix}",
            "details": state.current_activity,
            "large_image": self.config.assets.large_image,
            "large_text": self.config.assets.large_text,
            "start": state.start_timestamp,
        }
        if self.config.assets.small_image:
            payload["small_image"] = self.config.assets.small_image
            payload["small_text"] = self.config.assets.small_text
        buttons = []
        for button in self.config.buttons[:2]:
            parsed = urlparse(button.url)
            if button.label.strip() and parsed.scheme in {"http", "https"} and parsed.netloc:
                buttons.append({"label": button.label[:32], "url": button.url})
        if buttons:
            payload["buttons"] = buttons
        return payload
