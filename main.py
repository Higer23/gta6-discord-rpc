"""HIGER RPC entry point."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/"src"))
from gta6_rpc.app import run
if __name__=="__main__":run()
