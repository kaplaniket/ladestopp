#!/usr/bin/env python3
"""Neue Version ausrollen: python3 release.py 1.0.1 "Was ist neu" ["Noch was"]"""
import datetime, json, re, sys
ver, notes = sys.argv[1], sys.argv[2:]
assert re.fullmatch(r"\d+\.\d+\.\d+", ver), "Version wie 1.2.3"
s = open("index.html").read()
s = re.sub(r'const APP_VERSION="[^"]*";', f'const APP_VERSION="{ver}";', s)
open("index.html", "w").write(s)
json.dump({"version": ver, "date": datetime.date.today().isoformat(), "notes": notes},
          open("version.json", "w"), ensure_ascii=False)
print("Version", ver, "gesetzt. Jetzt committen, pushen und taggen: git tag v" + ver)
