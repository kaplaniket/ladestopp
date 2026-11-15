#!/usr/bin/env python3
"""Zerlegt data/stations.json in 1x1-Grad-Kacheln (data/t/LAT_LON.json) plus operators.json."""
import json, math, os, shutil, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "data", "stations.json")
OUT = os.path.join(HERE, "data")

d = json.load(open(SRC))
tiles = {}
for s in d["stations"]:
    k = f'{math.floor(s["lat"])}_{math.floor(s["lon"])}'
    tiles.setdefault(k, []).append([s["lat"], s["lon"], s["op"], s["name"], s["addr"],
                                    s["kw"], s["n"], s["plugs"], s.get("hours", "")])
tdir = os.path.join(OUT, "t")
shutil.rmtree(tdir, ignore_errors=True)
os.makedirs(tdir)
for k, v in tiles.items():
    json.dump(v, open(os.path.join(tdir, k + ".json"), "w"), ensure_ascii=False, separators=(",", ":"))
ops = Counter(s["op"] for s in d["stations"] if s["op"]).most_common(600)
json.dump({"stand": d.get("stand", ""), "ops": ops}, open(os.path.join(OUT, "operators.json"), "w"),
          ensure_ascii=False, separators=(",", ":"))
print(len(tiles), "Kacheln,", len(d["stations"]), "Standorte, Stand", d.get("stand"))
