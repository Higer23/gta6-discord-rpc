"""Strict configuration validation for HIGER RPC."""
from __future__ import annotations
import re
from urllib.parse import urlparse
from .models import AppConfig
ASSET_RE=re.compile(r"^[A-Za-z0-9_.-]{1,128}$"); LOG_LEVELS={"DEBUG","INFO","WARNING","ERROR","CRITICAL"}; MODES={"normal","quiet","errors"}
def validate_config(c:AppConfig)->list[str]:
    e=[]
    if not c.client_id or not c.client_id.isdigit(): e.append("client_id must be a numeric Discord application ID.")
    if c.update_interval<=0 or c.update_interval>3600: e.append("update_interval must be between 0 and 3600 seconds.")
    if c.rotation.min_seconds<=0 or c.rotation.max_seconds<=0: e.append("rotation times must be greater than 0.")
    if c.rotation.min_seconds>c.rotation.max_seconds: e.append("rotation_min_seconds must be smaller than rotation_max_seconds.")
    if not c.assets.large_image or not ASSET_RE.fullmatch(c.assets.large_image): e.append("assets.large_image is missing or invalid.")
    if c.assets.small_image and not ASSET_RE.fullmatch(c.assets.small_image): e.append("assets.small_image contains invalid characters.")
    if not c.activities: e.append("activities must contain at least one activity.")
    if not c.locations: e.append("locations must contain at least one location.")
    if not c.details_suffixes: e.append("details_suffixes must contain at least one value.")
    if len(c.buttons)>2: e.append("Discord Rich Presence supports at most 2 buttons.")
    for i,b in enumerate(c.buttons,1):
        p=urlparse(b.url)
        if not b.label.strip(): e.append(f"buttons[{i}].label cannot be empty.")
        if len(b.label)>32: e.append(f"buttons[{i}].label must be 32 characters or fewer.")
        if p.scheme not in {"http","https"} or not p.netloc: e.append(f"buttons[{i}].url is not a valid HTTP(S) URL.")
    if c.logging.level not in LOG_LEVELS: e.append("logging.level is invalid.")
    if c.logging.max_bytes<=0 or c.logging.backup_count<0: e.append("logging rotation values are invalid.")
    if c.terminal.mode not in MODES: e.append("terminal.mode must be normal, quiet, or errors.")
    if c.terminal.refresh_hz<=0 or c.terminal.refresh_hz>10: e.append("terminal.refresh_hz must be between 0 and 10.")
    if c.config_reload_interval<0.5 or c.config_reload_interval>3600: e.append("config_reload_interval must be between 0.5 and 3600 seconds.")
    return e
def validate_or_raise(c:AppConfig)->None:
    e=validate_config(c)
    if e: raise ValueError("Configuration error:\n"+"\n".join(f" - {x}" for x in e))
