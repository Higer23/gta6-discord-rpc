"""Discord presence payload builder and deduplication signature."""
from __future__ import annotations
import json
from typing import Any
from urllib.parse import urlparse
from .models import AppConfig,PresenceState
class PresenceBuilder:
    def __init__(self,config:AppConfig): self.config=config
    def build(self,state:PresenceState)->dict[str,Any]:
        p={"state":f"{state.current_location} • {state.current_suffix}","details":state.current_activity,"large_image":self.config.assets.large_image,"large_text":self.config.assets.large_text,"start":state.start_timestamp}
        if self.config.assets.small_image:p.update(small_image=self.config.assets.small_image,small_text=self.config.assets.small_text)
        buttons=[]
        for b in self.config.buttons[:2]:
            u=urlparse(b.url)
            if b.label.strip() and u.scheme in {"http","https"} and u.netloc:buttons.append({"label":b.label[:32],"url":b.url})
        if buttons:p["buttons"]=buttons
        return p
    @staticmethod
    def signature(payload:dict[str,Any])->str:return json.dumps(payload,sort_keys=True,separators=(",",":"))
