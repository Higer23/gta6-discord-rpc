"""Resilient pypresence adapter with bounded retry cooldown."""
from __future__ import annotations
import logging,time
from typing import Any
logger=logging.getLogger("higer_rpc.rpc")
class DiscordRPCClient:
 def __init__(self,client_id:str,*,quiet=False,min_retry=5.0,max_retry=60.0,clock=time.monotonic):
  self.client_id=client_id;self.quiet=quiet;self.min_retry=min_retry;self.max_retry=max_retry;self.clock=clock;self._rpc:Any=None;self.connected=False;self._retry_delay=min_retry;self._next_retry=0.0
 def _out(self,s):
  if not self.quiet:print(s)
 def connect(self,*,wait=False)->bool:
  now=self.clock()
  if not wait and now<self._next_retry:return False
  while True:
   try:
    from pypresence import Presence
    self._rpc=Presence(self.client_id);self._rpc.connect();self.connected=True;self._retry_delay=self.min_retry;self._next_retry=0;logger.info("RPC connected");self._out("✓ Discord RPC connected");return True
   except Exception as ex:
    self.connected=False;self._rpc=None;logger.warning("RPC connection failed: %r",ex)
    if not wait:self._next_retry=now+self._retry_delay;self._retry_delay=min(self._retry_delay*1.5,self.max_retry);return False
    self._out(f"⚠ Discord RPC unavailable; retrying in {self._retry_delay:g}s");time.sleep(self._retry_delay);self._retry_delay=min(self._retry_delay*1.5,self.max_retry)
 def reconnect(self)->bool:self._safe_close();return self.connect(wait=False)
 def update(self,payload:dict[str,Any])->bool:
  if not self.connected and not self.reconnect():return False
  try:self._rpc.update(**payload);return True
  except Exception as ex:logger.warning("RPC update failed: %r",ex);self.connected=False;self._safe_close();self._next_retry=self.clock()+self._retry_delay;self._out("⚠ Discord RPC disconnected; retry scheduled");return False
 def clear(self):
  if self._rpc:
   try:self._rpc.clear()
   except Exception as ex:logger.debug("RPC clear failed: %r",ex)
 def _safe_close(self):
  if self._rpc:
   try:self._rpc.close()
   except Exception:pass
  self._rpc=None;self.connected=False
 def close(self):self.clear();self._safe_close();logger.info("RPC closed")
