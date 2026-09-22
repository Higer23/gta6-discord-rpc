"""High-level application orchestration."""

from __future__ import annotations

import logging

from .activities import ActivityGenerator
from .config import CONFIG_PATH, EXAMPLE_PATH, load_config
from .logger import configure_logging
from .models import PresenceState
from .presence import PresenceBuilder
from .rpc_client import DiscordRPCClient
from .scheduler import UpdateScheduler
from .setup import run_setup
from .terminal import TerminalUI
from .timer import MonotonicElapsedTimer
from .validation import validate_or_raise

logger = logging.getLogger(__name__)


def _ensure_config() -> None:
    if not CONFIG_PATH.exists():
        run_setup(CONFIG_PATH, example_path=EXAMPLE_PATH)


def run() -> None:
    rpc: DiscordRPCClient | None = None
    ui = TerminalUI()
    try:
        _ensure_config()
        config = load_config()
        validate_or_raise(config)
        configure_logging(config.logging)
        ui.quiet = config.terminal.quiet
        ui.banner()
        ui.configuration_summary(config)
        timer = MonotonicElapsedTimer(config.played_time.total_seconds)
        start_timestamp = timer.discord_start_timestamp(config.played_time.total_seconds)
        state = PresenceState(config.played_time.total_seconds, start_timestamp)
        activities = ActivityGenerator(config)
        activities.choose(state)
        builder = PresenceBuilder(config)
        rpc = DiscordRPCClient(config.client_id, quiet=config.terminal.quiet)
        if not rpc.connect():
            raise RuntimeError("Unable to initialize Discord RPC.")
        if not config.terminal.quiet:
            print("✓ Timer initialized")
        rpc.update(builder.build(state))
        if not config.terminal.quiet:
            print("✓ Presence active")
        scheduler = UpdateScheduler(config.update_interval)
        scheduler.run(lambda: (activities.ensure_current(state), rpc.update(builder.build(state)), ui.status(config, state)), lambda: False)
    except KeyboardInterrupt:
        print("

Stopping GTA VI RPC...")
        logger.info("Stopped by user.")
    except Exception as exc:
        logger.exception("Fatal application error: %r", exc)
        ui.error(str(exc))
    finally:
        if rpc is not None:
            rpc.close()
        ui.stop()
