#!/usr/bin/env python3
"""
🌊 SurfAlert — Générateur de données pour le dashboard web.

Réutilise toute la logique de scoring de surf_alert.py, mais au lieu d'envoyer
une alerte Telegram, calcule les scores heure par heure sur 5 jours pour les
5 spots et écrit le résultat dans data.json (lu ensuite par index.html).

Usage : python3 generate_data.py
"""

import json
import os
import time
from datetime import datetime, timedelta

import requests

# On réutilise la config et la logique déjà écrites dans surf_alert.py
from surf_alert import (
    SPOTS, TZ, JOURS_FR,
    compute_score, dir_label, is_offshore, get_sun_times,
)

FORECAST_DAYS = 5  # même fenêtre que les alertes Telegram


# ──────────────────────────────────────────
# FETCH (5 jours, contrairement à surf_alert qui en demande 3)
# ──────────────────────────────────────────
def _get_json(url, params, label="API", headers=None):
    """GET robuste : timeout 30s, 4 tentatives, pause entre essais (Open-Meteo lent en CI)."""
    last_err = None
    for attempt in range(4):
        try:
            r = requests.get(url, params=params, timeout=30, headers=headers)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            last_err = e
            print(f"  ⏳ {label} : tentative {attempt + 1}/4 ({e})")
            time.sleep(3)
    raise last_err


def fetch_marine(lat, lon):
    return _get_json("https://marine-api.open-meteo.com/v1/marine", {
        "latitude": lat, "longitude": lon,
        "hourly": "wave_height,wave_period,wave_direction,"
                  "swell_wave_height,swell_wave_period,swell_wave_direction",
        "timezone": "Europe/Paris",
        "forecast_days": FORECAST_DAYS,
    }, label="marine")


def fetch_weather(lat, lon):
    return _get_json("https://api.open-meteo.com/v1/forecast", {
        "latitude": lat, "longitude": lon,
        "hourly": "wind_speed_10m,wind_direction_10m,weather_code,cloud_cover",
        "timezone": "Europe/Paris",
        "forecast_days": FORECAST_DAYS,
        "wind_speed_unit": "kmh",
    }, label="weather")


# ──────────────────────────────────────────
# ANALYSE 5 JOURS (toutes les heures, pas seulement les pics)
# ──────────────────────────────────────────
def analyze_spot(spot_cfg):
    lat, lon = spot_cfg["lat"], spot_cfg["lon"]
    marine = fetch_marine(lat, lon)
    weather = fetch_weather(lat, lon)

    times = marine["hourly"]["time"]
    sun_cache = {}  # une seule paire lever/coucher par date
    hours = []

    for i, ts in enumerate(times):
        dt = datetime.fromisoformat(ts).replace(tzinfo=TZ)

        if dt.date() not in sun_cache:
            sunrise, sunset = get_sun_times(lat, lon, dt.date())
            sun_cache[dt.date()] = (
                sunrise.hour + sunrise.minute / 60,
                sunset.hour + sunset.minute / 60,
            )
        sr_h, ss_h = sun_cache[dt.date()]

        wave_h    = marine["hourly"]["wave_height"][i] or 0
        wave_p    = marine["hourly"]["wave_period"][i] or 0
        swell_dir = marine["hourly"]["swell_wave_direction"][i] or 0
        wind_spd  = weather["hourly"]["wind_speed_10m"][i] or 0
        wind_dir  = weather["hourly"]["wind_direction_10m"][i] or 0
        cloud     = weather["hourly"]["cloud_cover"][i] or 0

        hour_dec = dt.hour + dt.minute / 60
        score, breakdown = compute_score(
            wave_h, wave_p, swell_dir,
            wind_spd, wind_dir,
            hour_dec, sr_h, ss_h, cloud,
            spot_cfg["h_ideal"], spot_cfg["swell_opt"], spot_cfg["swell_tol"],
        )

        # On ne garde que les heures de jour (le surf de nuit, on oublie)
        is_daytime = sr_h - 0.5 <= hour_dec <= ss_h + 0.5

        hours.append({
            "time": dt.isoformat(),
            "score": score,
            "wave_h": round(wave_h, 1),
            "wave_p": round(wave_p),
            "swell_dir": round(swell_dir),
            "swell_label": dir_label(swell_dir),
            "wind_spd": round(wind_spd),
            "wind_dir": round(wind_dir),
            "wind_label": dir_label(wind_dir),
            "offshore": is_offshore(wind_dir),
            "cloud": round(cloud),
            "light": round(breakdown["Lumière"]),
            "daytime": is_daytime,
        })

    return hours


# ──────────────────────────────────────────
# MARÉES (sans clé : on déduit les pleines/basses mers de la hauteur d'eau Open-Meteo)
# Une mesure par RÉGION : les horaires de marée diffèrent le long de la côte.
# ──────────────────────────────────────────
def fetch_sea_level(lat, lon):
    j = _get_json("https://marine-api.open-meteo.com/v1/marine", {
        "latitude": lat, "longitude": lon,
        "hourly": "sea_level_height_msl",
        "timezone": "Europe/Paris",
        "forecast_days": FORECAST_DAYS,
    }, label="marées")
    return j["hourly"]["time"], j["hourly"]["sea_level_height_msl"]


def compute_extremes(times, h):
    extremes = []
    for i in range(1, len(h) - 1):
        a, b, c = h[i - 1], h[i], h[i + 1]
        if a is None or b is None or c is None:
            continue
        is_high = b > a and b >= c
        is_low = b < a and b <= c
        if not (is_high or is_low):
            continue
        # interpolation parabolique → heure précise de l'extremum (sous l'heure pleine)
        denom = a - 2 * b + c
        offset = 0.5 * (a - c) / denom if denom != 0 else 0.0
        offset = max(-0.5, min(0.5, offset))
        peak_time = (datetime.fromisoformat(times[i]).replace(tzinfo=TZ)
                     + timedelta(minutes=round(offset * 60)))
        extremes.append({
            "time": peak_time.isoformat(),
            "type": "haute" if is_high else "basse",
        })
    return extremes


LIVE_DATA_URL = "https://loupeirrot.github.io/swelleo/data.json"


def load_previous():
    """Récupère le data.json déjà en ligne — filet pour réutiliser la dernière
    donnée connue si un spot ou une région échoue ce run."""
    try:
        r = requests.get(LIVE_DATA_URL, timeout=20)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"  ⏳ data.json précédent indisponible ({e})")
        return {}


TIDE_HALF = timedelta(hours=6, minutes=12, seconds=37)  # demi-cycle de marée (~12h25 complet)


def project_tides(prev_extremes):
    """Marée = phénomène cyclique : on projette les extrema connus vers l'avant pour
    couvrir la fenêtre de prévision (approximation, en attendant une vraie mesure)."""
    if not prev_extremes:
        return []
    exs = sorted(prev_extremes, key=lambda e: e["time"])
    t = datetime.fromisoformat(exs[-1]["time"])
    typ = exs[-1]["type"]
    start = datetime.now(TZ) - timedelta(hours=6)
    horizon = datetime.now(TZ) + timedelta(days=FORECAST_DAYS)
    while t > start:                      # recule l'ancre avant le début de la fenêtre
        t -= TIDE_HALF
        typ = "basse" if typ == "haute" else "haute"
    out = []
    while t <= horizon:                   # puis projette en avant, en alternant haute/basse
        if t >= start:
            out.append({"time": t.isoformat(), "type": typ, "est": True})
        t += TIDE_HALF
        typ = "basse" if typ == "haute" else "haute"
    return out


def fetch_tides_by_region(prev_tides=None):
    """Une série de marées par région, au barycentre des spots de la région."""
    regions = {}
    for cfg in SPOTS.values():
        regions.setdefault(cfg["region"], []).append((cfg["lat"], cfg["lon"]))
    tides = {}
    for region, pts in regions.items():
        lat = sum(p[0] for p in pts) / len(pts)
        lon = sum(p[1] for p in pts) / len(pts)
        try:
            times, h = fetch_sea_level(lat, lon)
            tides[region] = compute_extremes(times, h)
        except Exception as e:
            if prev_tides and prev_tides.get(region):
                tides[region] = project_tides(prev_tides[region])
                print(f"  ↩︎ marées {region} : recalculées par cycle depuis la dernière donnée")
            else:
                print(f"  ❌ marées {region} indisponibles : {e}")
    return tides


# ──────────────────────────────────────────
# BOUÉES CANDHIS (houle mesurée en temps réel — clé API requise)
# Une bouée active par région ; type 2 = directionnel H13, type 0 = non directionnel.
# ──────────────────────────────────────────
BUOYS_BY_REGION = {
    "Landes": ("06402", 2, "Anglet"),
    "Pays Basque": ("06403", 2, "Saint-Jean-de-Luz"),
    "Gironde": ("03302", 2, "Cap Ferret"),
    "Vendée": ("08504", 0, "Île d'Yeu"),
    # Finistère : aucune bouée active actuellement
}


def _f(v):
    """Convertit en float ; 999.9999 (valeur manquante Candhis) → None."""
    try:
        x = float(v)
        return None if x >= 999 else round(x, 1)
    except Exception:
        return None


def fetch_buoys(key):
    if not key:
        return {}
    hdr = {"Authorization": key}
    by_type = {}
    for region, (code, typ, name) in BUOYS_BY_REGION.items():
        by_type.setdefault(typ, []).append(code)
    measures = {}
    for typ, codes in by_type.items():
        url = (f"https://candhis.cerema.fr/API/v1/getCampListeTR.php"
               f"?type={typ}&camp={','.join(codes)}")
        try:
            j = _get_json(url, {}, label="bouées", headers=hdr)
        except Exception as e:
            print(f"  ❌ bouées type {typ} indisponibles : {e}")
            continue
        for row in (j.get("results") or []):
            d = _f(row[5]) if typ == 2 else None
            temp = _f(row[7]) if typ == 2 else _f(row[6])
            measures[str(row[0])] = {
                "time": row[1], "h": _f(row[2]), "period": _f(row[4]),
                "dir": d, "dir_label": dir_label(d) if d is not None else "", "temp": temp,
            }
    out = {}
    for region, (code, typ, name) in BUOYS_BY_REGION.items():
        m = measures.get(code)
        if m and m["h"] is not None:
            m = dict(m); m["code"] = code; m["name"] = name
            out[region] = m
    return out


def main():
    print(f"[{datetime.now(TZ).strftime('%H:%M')}] Génération des données dashboard...")
    prev = load_previous()
    prev_spots = {s["name"]: s for s in prev.get("spots", [])}
    prev_tides = prev.get("tides", {})
    if not isinstance(prev_tides, dict):
        prev_tides = {}
    spots_data = []

    for spot_name, spot_cfg in SPOTS.items():
        print(f"  → {spot_name}")
        try:
            hours = analyze_spot(spot_cfg)
            spots_data.append({
                "name": spot_name,
                "region": spot_cfg["region"],
                "priority": spot_cfg["priority"],
                "lat": spot_cfg["lat"],
                "lon": spot_cfg["lon"],
                "h_ideal": spot_cfg["h_ideal"],
                "webcam": spot_cfg.get("webcam", ""),
                "hours": hours,
            })
        except Exception as e:
            if spot_name in prev_spots:
                spots_data.append(prev_spots[spot_name])
                print(f"  ↩︎ {spot_name} : dernière donnée connue réutilisée ({e})")
            else:
                print(f"  ❌ Erreur sur {spot_name}: {e}")

    try:
        tides = fetch_tides_by_region(prev_tides)
        total = sum(len(v) for v in tides.values())
        print(f"  → marées : {total} extrema sur {len(tides)} régions")
    except Exception as e:
        tides = {}
        print(f"  ❌ Marées indisponibles : {e}")

    try:
        buoys = fetch_buoys(os.environ.get("CANDHIS_KEY", ""))
        print(f"  → bouées Candhis : {len(buoys)} régions mesurées")
    except Exception as e:
        buoys = {}
        print(f"  ❌ Bouées indisponibles : {e}")

    output = {
        "generated_at": datetime.now(TZ).isoformat(),
        "forecast_days": FORECAST_DAYS,
        "jours_fr": JOURS_FR,
        "tides": tides,
        "buoys": buoys,
        "spots": spots_data,
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✅ data.json écrit ({len(spots_data)} spots).")


if __name__ == "__main__":
    main()
