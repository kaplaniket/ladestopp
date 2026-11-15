#!/usr/bin/env python3
"""Zugang beenden (im Branch gh-pages, danach committen und pushen).
Tekin erzeugt auf zugang.html unter „Zugang beenden“ einen Sperrcode (SHA-256 der E-Mail).
  python3 zugang.py sperren SPERRCODE
  python3 zugang.py freigeben SPERRCODE"""
import json, re, sys
cmd, h = sys.argv[1], sys.argv[2].strip().lower()
assert re.fullmatch(r"[0-9a-f]{64}", h), "Sperrcode muss 64 Hex-Zeichen haben"
d = json.load(open("users.json")); d.setdefault("revoked", [])
if cmd == "sperren" and h not in d["revoked"]: d["revoked"].append(h)
if cmd == "freigeben": d["revoked"] = [x for x in d["revoked"] if x != h]
json.dump(d, open("users.json", "w")); print(len(d["revoked"]), "gesperrt")
