#!/usr/bin/env python3
"""Wandelt das Ladesäulenregister der Bundesnetzagentur (CSV) in data/stations.json um."""
import csv, io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "data", "register.csv")
DST = os.path.join(HERE, "data", "stations.json")

def num(s):
    s = (s or "").strip().replace(".", "").replace(",", ".") if "," in (s or "") else (s or "").strip()
    try:
        return float(re.findall(r"[\d.]+", s)[0])
    except Exception:
        return 0.0

def plug_keys(txt):
    t = (txt or "").lower()
    keys = set()
    if "combo" in t or "ccs" in t: keys.add("type2_combo")
    if "chademo" in t: keys.add("chademo")
    if "tesla" in t: keys.add("tesla_supercharger")
    if "schuko" in t: keys.add("schuko")
    if "typ 2" in t and ("steckdose" in t or "kupplung" in t or "fahrzeugkupplung" in t) and "combo" not in t:
        keys.add("type2")
    return keys

def main():
    raw = open(SRC, "rb").read().decode("utf-8-sig", "replace")
    lines = raw.splitlines()
    hi = next(i for i, l in enumerate(lines) if l.startswith("Ladeeinrichtungs-ID;"))
    rd = csv.reader(io.StringIO("\n".join(lines[hi:])), delimiter=";")
    head = next(rd)
    ix = {h: i for i, h in enumerate(head)}
    def g(r, k):
        i = ix.get(k)
        return r[i].strip() if i is not None and i < len(r) else ""
    sites = {}
    for r in rd:
        if len(r) < 17: continue
        if g(r, "Status") and g(r, "Status").lower() not in ("in betrieb", "inbetrieb"): continue
        try:
            lat = float(g(r, "Breitengrad").replace(",", ".")); lon = float(g(r, "Längengrad").replace(",", "."))
        except ValueError:
            continue
        if not (47 < lat < 56 and 5 < lon < 16): continue
        op = g(r, "Betreiber")
        key = (round(lat, 4), round(lon, 4), op.lower())
        s = sites.get(key)
        if not s:
            name = g(r, "Anzeigename (Karte)") or op
            addr = " ".join(x for x in [g(r, "Straße"), g(r, "Hausnummer")] if x)
            ort = " ".join(x for x in [g(r, "Postleitzahl"), g(r, "Ort")] if x)
            s = sites[key] = {"lat": round(lat, 6), "lon": round(lon, 6), "op": op, "name": name,
                              "addr": ", ".join(x for x in [addr, ort] if x), "kw": 0.0, "n": 0,
                              "plugs": {}, "hours": g(r, "Öffnungszeiten"), "pay": g(r, "Bezahlsysteme")}
        s["n"] += int(num(g(r, "Anzahl Ladepunkte")) or 1)
        s["kw"] = max(s["kw"], num(g(r, "Nennleistung Ladeeinrichtung [kW]")))
        for k in range(1, 7):
            st = g(r, f"Steckertypen{k}")
            if not st: continue
            kw = num(g(r, f"Nennleistung Stecker{k}"))
            for pk in plug_keys(st):
                s["plugs"][pk] = max(s["plugs"].get(pk, 0), kw)
    out = []
    for s in sites.values():
        s["kw"] = round(s["kw"], 1)
        s["plugs"] = {k: round(v, 1) for k, v in s["plugs"].items()}
        out.append(s)
    json.dump({"stand": next((l.split(";")[0].split(":")[-1].strip() for l in lines[:12] if "Letzte Aktualisierung" in l), ""),
               "stations": out}, open(DST, "w"), ensure_ascii=False, separators=(",", ":"))
    print(len(out), "Standorte geschrieben")

if __name__ == "__main__":
    main()
