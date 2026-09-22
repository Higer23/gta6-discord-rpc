"""HIGER application lifecycle and orchestration."""
from __future__ import annotations
import logging,random,signal,time
from threading import Event
from .activities import ActivityGenerator
from .config import CONFIG_PATH,EXAMPLE_PATH,config_mtime_ns,load_config
from .logger import configure_logging
from .models import PresenceState
from .presence import PresenceBuilder
from .rpc_client import DiscordRPCClient
from .scheduler import UpdateScheduler
from .setup import run_setup
from .terminal import TerminalUI
from .timer import MonotonicElapsedTimer
from .validation import validate_or_raise
logger=logging.getLogger("higer_rpc.app")
def _ensure_config():
 if not CONFIG_PATH.exists():run_setup(CONFIG_PATH,EXAMPLE_PATH)
def run()->None:
 stop=Event();rpc=None;ui=TerminalUI()
 def shutdown(*_):stop.set()
 for sig in (signal.SIGINT,signal.SIGTERM):
  try:signal.signal(sig,shutdown)
  except (ValueError,AttributeError):pass
 try:
  _ensure_config();config=load_config();validate_or_raise(config);configure_logging(config.logging);ui=TerminalUI(config.terminal.mode,config.terminal.refresh_hz);ui.banner();ui.info("✓ HIGER configuration loaded")
  timer=MonotonicElapsedTimer(config.played_time.total_seconds);state=PresenceState(config.played_time.total_seconds,timer.discord_start_timestamp(config.played_time.total_seconds));activities=ActivityGenerator(config,random.Random());activities.choose(state);builder=PresenceBuilder(config);rpc=DiscordRPCClient(config.client_id,quiet=config.terminal.mode!="normal");rpc.connect(wait=False);state.last_config_mtime_ns=config_mtime_ns()
  last_reload=0.0;last_sig=""
  def tick():
   nonlocal config,activities,builder,last_reload,last_sig
   now=time.monotonic()
   if config.config_reload and now-last_reload>=config.config_reload_interval:
    last_reload=now;mt=config_mtime_ns()
    if mt and mt!=state.last_config_mtime_ns:
     try:
      fresh=load_config();validate_or_raise(fresh);config=fresh;activities=ActivityGenerator(config,random.Random());builder=PresenceBuilder(config);state.last_config_mtime_ns=mt;last_sig="";ui.info("\n✓ HIGER configuration reloaded")
     except Exception as ex:logger.warning("Config reload rejected: %r",ex)
   if activities.ensure_current(state):last_sig=""
   payload=builder.build(state);sig=builder.signature(payload)
   if sig!=last_sig:
    if rpc.update(payload):last_sig=sig
   elif not rpc.connected:rpc.reconnect()
   ui.status(config,state)
  UpdateScheduler(config.update_interval,stop).run(tick)
 except Exception as ex:logger.exception("HIGER fatal error");ui.error(str(ex))
 finally:
  if rpc:rpc.close()
  ui.stop()
