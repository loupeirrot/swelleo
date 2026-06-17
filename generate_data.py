#!/usr/bin/env python3
"""
🌊 SurfAlert — Générateur de données pour le dashboard web.

Réutilise toute la logique de scoring de surf_alert.py, mais au lieu d'envoyer
une alerte Telegram, calcule les scores heure par heure sur 5 jours pour les
5 spots et écrit le résultat dans data.json (lu ensuite par index.html).

Usage : python3 generate_data.py
"""

import json
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
def fetch_marine(lat, lon):
    r = requests.get("https://marine-api.open-meteo.com/v1/marine", params={
        "latitude": lat, "longitude": lon,
        "hourly": "wave_height,wave_period,wave_direction,"
                  "swell_wave_height,swell_wave_period,swell_wave_direction",
        "timezone": "Europe/Paris",
        "forecast_days": FORECAST_DAYS,
    }, timeout=15)
    r.raise_for_status()
    return r.json()


def fetch_weather(lat, lon):
    r = requests.get("https://api.open-meteo.com/v1/forecast", params={
        "latitude": lat, "longitude": lon,
        "hourly": "wind_speed_10m,wind_direction_10m,weather_code,cloud_cover",
        "timezone": "Europe/Paris",
        "forecast_days": FORECAST_DAYS,
        "wind_speed_unit": "kmh",
    }, timeout=15)
    r.raise_for_status()
    return r.json()


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
# Les 5 spots sont à quelques km → une seule mesure suffit pour toute la zone.
# ──────────────────────────────────────────
ZONE_LAT, ZONE_LON = 43.66, -1.44

def fetch_tides():
    r = requests.get("https://marine-api.open-meteo.com/v1/marine", params={
        "latitude": ZONE_LAT, "longitude": ZONE_LON,
        "hourly": "sea_level_height_msl",
        "timezone": "Europe/Paris",
        "forecast_days": FORECAST_DAYS,
    }, timeout=15)
    r.raise_for_status()
    j = r.json()
    times = j["hourly"]["time"]
    h = j["hourly"]["sea_level_height_msl"]

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


def main():
    print(f"[{datetime.now(TZ).strftime('%H:%M')}] Génération des données dashboard...")
    spots_data = []

    for spot_name, spot_cfg in SPOTS.items():
        print(f"  → {spot_name}")
        try:
            hours = analyze_spot(spot_cfg)
            spots_data.append({
                "name": spot_name,
                "priority": spot_cfg["priority"],
                "lat": spot_cfg["lat"],
                "lon": spot_cfg["lon"],
                "h_ideal": spot_cfg["h_ideal"],
                "hours": hours,
            })
        except Exception as e:
            print(f"  ❌ Erreur sur {spot_name}: {e}")

    try:
        tides = fetch_tides()
        print(f"  → {len(tides)} marées (pleines/basses mers) calculées")
    except Exception as e:
        tides = []
        print(f"  ❌ Marées indisponibles : {e}")

    output = {
        "generated_at": datetime.now(TZ).isoformat(),
        "forecast_days": FORECAST_DAYS,
        "jours_fr": JOURS_FR,
        "tides": tides,
        "spots": spots_data,
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✅ data.json écrit ({len(spots_data)} spots).")


if __name__ == "__main__":
    main()
