"""Interactive first-run setup."""
from __future__ import annotations
import json
from pathlib import Path
from .timer import parse_duration
def run_setup(path:Path,example_path:Path)->None:
 data=json.loads(example_path.read_text(encoding="utf-8"));print("\nHIGER — first-time setup\n")
 cid=input("Discord Client ID: ").strip()
 if cid:data["client_id"]=cid
 raw=input("Played time [127:43:29]: ").strip()
 if raw:
  total=parse_duration(raw);h,r=divmod(total,3600);m,s=divmod(r,60);data["played_time"]={"hours":h,"minutes":m,"seconds":s}
 path.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8");print(f"✓ HIGER configuration saved: {path}")
