"""Fault-tolerant adapter around pypresence."""

from __future__ import annotations

import logging
import time
from typing import Any

logger = logging.getLogger(__name__)


class DiscordRPCClient:
    """Owns Discord RPC connection lifecycle and retry behavior."""

    def __init__(self, client_id: str, *, quiet: bool = False, min_retry: float = 5.0, max_retry: float = 30.0) -> None:
        self.client_id = client_id
        self.quiet = quiet
        self.min_retry = min_retry
        self.max_retry = max_retry
        self._rpc: Any | None = None
        self._retry_delay = min_retry
        self.connected = False

    def _print(self, message: str) -> None:
        if not self.quiet:
            print(message)

    def connect(self, *, wait: bool = True) -> bool:
        while True:
            try:
                from pypresence import Presence
                self._rpc = Presence(self.client_id)
                self._rpc.connect()
                self.connected = True
                self._retry_delay = self.min_retry
                logger.info("Discord RPC connected.")
                self._print("✓ Discord RPC connected.")
                return True
            except Exception as exc:
                self.connected = False
                logger.warning("RPC connection failed: %r", exc)
                self._print(f"⚠ Discord RPC unavailable: {exc} — retrying in {self._retry_delay:g}s")
                if not wait:
                    return False
                delay = self._retry_delay
                self._retry_delay = min(self._retry_delay * 1.5, self.max_retry)
                time.sleep(delay)

    def update(self, payload: dict[str, Any]) -> bool:
        if self._rpc is None or not self.connected:
            self.connect()
        try:
            self._rpc.update(**payload)
            return True
        except Exception as exc:
            logger.warning("RPC update failed: %r", exc)
            if self._is_pipe_closed(exc):
                self.connected = False
                self._print("⚠ Discord RPC disconnected")
                self._safe_close()
                self._print("↻ Reconnecting...")
                self.connect()
                return False
            self._print(f"⚠ RPC update skipped: {exc}")
            return False

    @staticmethod
    def _is_pipe_closed(exc: Exception) -> bool:
        try:
            from pypresence import exceptions
            pipe_closed = getattr(exceptions, "PipeClosed", ())
            return isinstance(exc, pipe_closed) if pipe_closed else False
        except Exception:
            return "pipe" in str(exc).lower() and "closed" in str(exc).lower()

    def clear(self) -> None:
        if self._rpc is None:
            return
        try:
            self._rpc.clear()
        except Exception as exc:
            logger.debug("RPC clear failed during shutdown: %r", exc)

    def _safe_close(self) -> None:
        if self._rpc is None:
            return
        try:
            self._rpc.close()
        except Exception as exc:
            logger.debug("RPC close failed: %r", exc)
        finally:
            self._rpc = None
            self.connected = False

    def close(self) -> None:
        self.clear()
        self._safe_close()
        logger.info("Discord RPC closed.")
