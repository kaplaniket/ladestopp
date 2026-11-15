#!/usr/bin/env python3
"""Zugänge verwalten (im Branch gh-pages, danach committen und pushen).
Den Prüfwert erzeugt Tekin auf zugang.html (E-Mail + Passwort werden nur auf dem Handy berechnet).
  python3 zugang.py add PRUEFWERT
  python3 zugang.py remove PRUEFWERT"""
import json, re, sys
cmd, h = sys.argv[1], sys.argv[2].strip().lower()
assert re.fullmatch(r"[0-9a-f]{64}", h), "Prüfwert muss 64 Hex-Zeichen haben"
d = json.load(open("users.json"))
if cmd == "add" and h not in d["users"]: d["users"].append(h)
if cmd == "remove": d["users"] = [x for x in d["users"] if x != h]
json.dump(d, open("users.json", "w"), indent=0)
print(len(d["users"]), "Zugänge")
