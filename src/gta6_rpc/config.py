"""Configuration loading, atomic saving, and change detection."""
from __future__ import annotations
import json,os,tempfile
from pathlib import Path
from typing import Any
from .models import AppConfig,PlayedTime,RotationConfig,AssetConfig,ButtonConfig,TerminalConfig,LoggingConfig
BASE_DIR=Path(__file__).resolve().parents[2]; CONFIG_PATH=BASE_DIR/"config.json"; EXAMPLE_PATH=BASE_DIR/"config.json.example"
def _duration(d:dict[str,Any])->int:
    try: h,m,s=int(d.get("hours",0)),int(d.get("minutes",0)),int(d.get("seconds",0))
    except (TypeError,ValueError) as ex: raise ValueError("played_time values must be integers.") from ex
    if min(h,m,s)<0 or m>=60 or s>=60: raise ValueError("played_time has invalid hours/minutes/seconds.")
    return h*3600+m*60+s
def load_raw_config(path:Path=CONFIG_PATH)->dict[str,Any]:
    try: data=json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError: raise
    except json.JSONDecodeError as ex: raise ValueError(f"Configuration JSON invalid at line {ex.lineno}, column {ex.colno}.") from ex
    if not isinstance(data,dict): raise ValueError("Configuration root must be a JSON object.")
    return data
def build_config(d:dict[str,Any])->AppConfig:
    pt=d.get("played_time",{}); rot=d.get("activity_rotation",{}); a=d.get("assets",{}); t=d.get("terminal",{}); l=d.get("logging",{})
    bs=tuple(ButtonConfig(str(x.get("label","")),str(x.get("url",""))) for x in d.get("buttons",[]) if isinstance(x,dict))
    return AppConfig(str(d.get("client_id","")).strip(),PlayedTime(_duration(pt)),bool(d.get("interactive_setup",True)),float(d.get("update_interval",1)),RotationConfig(bool(rot.get("enabled",True)),float(rot.get("min_seconds",60)),float(rot.get("max_seconds",120))),AssetConfig(str(a.get("large_image","")).strip(),str(a.get("large_text","")),str(a["small_image"]).strip() if a.get("small_image") else None,str(a.get("small_text",""))),bs,TerminalConfig(str(t.get("mode","normal")).lower(),float(t.get("refresh_hz",1))),LoggingConfig(str(l.get("level","INFO")).upper(),str(l.get("file","logs/higer_rpc.log")),int(l.get("max_bytes",1048576)),int(l.get("backup_count",3))),tuple(str(x).strip() for x in d.get("activities",[])),tuple(str(x).strip() for x in d.get("locations",[])),tuple(str(x).strip() for x in d.get("details_suffixes",[])),bool(d.get("config_reload",True)),float(d.get("config_reload_interval",2)))
def load_config(path:Path=CONFIG_PATH)->AppConfig: return build_config(load_raw_config(path))
def config_mtime_ns(path:Path=CONFIG_PATH)->int:
    try:return path.stat().st_mtime_ns
    except FileNotFoundError:return 0
def atomic_write_json(path:Path,data:dict[str,Any])->None:
    path.parent.mkdir(parents=True,exist_ok=True); fd,tmp=tempfile.mkstemp(prefix=".higer-",suffix=".json",dir=path.parent)
    try:
        with os.fdopen(fd,"w",encoding="utf-8") as f: json.dump(data,f,indent=2); f.write("\n"); f.flush(); os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)
