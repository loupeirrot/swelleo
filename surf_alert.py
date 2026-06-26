#!/usr/bin/env python3
"""
🌊 SurfAlert — La Nord · La Gravière · Les Estagnots · Santocha · La Piste
Analyse les conditions de surf et envoie des alertes Telegram.
"""

import os
import re
import unicodedata
import requests
from datetime import datetime, timedelta
import pytz
from astral import LocationInfo
from astral.sun import sun

JOURS_FR = ["lundi","mardi","mercredi","jeudi","vendredi","samedi","dimanche"]

def jour_fr(dt):
    return JOURS_FR[dt.weekday()]

# ──────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────
def _load_env_file():
    """Charge un fichier .env local (clé=valeur) s'il existe — sans dépendance externe.
    Le .env n'est jamais publié (il est dans .gitignore)."""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, val = line.partition("=")
                os.environ.setdefault(key.strip(), val.strip())

_load_env_file()

# Secrets lus depuis l'environnement / le fichier .env — jamais en dur dans le code.
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
CHAT_ID = os.environ.get("CHAT_ID", "")
ALERT_THRESHOLD = 7.5      # En dessous : silence total (≥6.5 = GO, 7.5 = forte session)
ALERT_FIRE     = 8.5       # Score "grosse session" sur spots prioritaires (notif sonore)
FORECAST_HOURS = 120       # Fenêtre d'analyse (5 jours)
SITE_URL       = "https://swelleo.com"

# Chaque spot a ses paramètres propres :
#   region     : pour regrouper les spots dans l'appli
#   swell_opt  : direction de houle idéale (degrés)
#   swell_tol  : tolérance angulaire (±°) avant pénalité
#   h_ideal    : plage de hauteur idéale (min, max en mètres)
#   priority   : "fire" = spot d'exception | "standard"
# NB : les réglages des spots hors Landes sont des estimations de départ (à affiner).
SPOTS = {
    # ───────── Landes ─────────
    "🔥 La Nord (Hossegor)": {
        "region": "Landes", "lat": 43.6750, "lon": -1.4380,
        "swell_opt": 215, "swell_tol": 25,   # SO, canalisé par le Gouf
        "h_ideal": (1.5, 4.0), "priority": "fire",
        "webcam": "https://gosurf.fr/webcam/fr/170/Hossegor-Plage-de-la-Nord",
    },
    "🏖 La Gravière (Hossegor)": {
        "region": "Landes", "lat": 43.6673, "lon": -1.4347,
        "swell_opt": 220, "swell_tol": 25,   # SO
        "h_ideal": (1.5, 3.5), "priority": "fire",
        "webcam": "https://gosurf.fr/webcam/fr/21/Hossegor-La-Centrale",
    },
    "🏄 Les Estagnots (Seignosse)": {
        "region": "Landes", "lat": 43.7045, "lon": -1.4289,
        "swell_opt": 240, "swell_tol": 30,   # O/SO
        "h_ideal": (1.2, 3.5), "priority": "standard",
        "webcam": "https://gosurf.fr/webcam/fr/79/Seignosse-Plage-des-Bourdaines-Plage-des-Estagnots",
    },
    "🌊 Santocha (Capbreton)": {
        "region": "Landes", "lat": 43.6464, "lon": -1.4452,
        "swell_opt": 255, "swell_tol": 35,   # O, filtré par le Gouf
        "h_ideal": (0.8, 2.5), "priority": "standard",
        "webcam": "https://gosurf.fr/webcam/fr/83/Capbreton-Plage-du-Santosha-de-La-Piste",
    },
    "🏴 La Piste (Capbreton)": {
        "region": "Landes", "lat": 43.6380, "lon": -1.4460,
        "swell_opt": 250, "swell_tol": 35,   # O/SO
        "h_ideal": (1.0, 3.0), "priority": "standard",
        "webcam": "https://gosurf.fr/webcam/fr/83/Capbreton-Plage-du-Santosha-de-La-Piste",
    },
    # ───────── Pays Basque ─────────
    "🏄 Côte des Basques (Biarritz)": {
        "region": "Pays Basque", "lat": 43.4793, "lon": -1.5658,
        "swell_opt": 290, "swell_tol": 40,   # O/NO, marche petit
        "h_ideal": (0.8, 2.5), "priority": "standard",
        "webcam": "https://gosurf.fr/webcam/fr/7/Biarritz-La-Cote-des-Basques",
    },
    "🌊 Les Cavaliers (Anglet)": {
        "region": "Pays Basque", "lat": 43.5269, "lon": -1.5266,
        "swell_opt": 285, "swell_tol": 35,
        "h_ideal": (1.0, 3.0), "priority": "standard",
        "webcam": "https://gosurf.fr/webcam/fr/150/Anglet-Plage-de-la-Barre",
    },
    "🏖 Hendaye": {
        "region": "Pays Basque", "lat": 43.3760, "lon": -1.7790,
        "swell_opt": 300, "swell_tol": 40,   # abrité, demande de la taille
        "h_ideal": (0.8, 2.5), "priority": "standard",
        "webcam": "https://gosurf.fr/webcam/fr/8/Hendaye-Plage-du-Casino-et-des-Jumeaux",
    },
    # ───────── Gironde ─────────
    "🏄 Lacanau Océan": {
        "region": "Gironde", "lat": 44.9772, "lon": -1.2050,
        "swell_opt": 270, "swell_tol": 40,
        "h_ideal": (1.0, 3.0), "priority": "standard",
        "webcam": "https://gosurf.fr/webcam/fr/9/Lacanau-Plage-de-Lacanau-Ocean",
    },
    "🌊 Le Porge Océan": {
        "region": "Gironde", "lat": 44.8722, "lon": -1.2030,
        "swell_opt": 270, "swell_tol": 40,
        "h_ideal": (1.0, 3.0), "priority": "standard",
        "webcam": "https://www.skaping.com/medoc-plein-sud/le-porge-ocean/live",
    },
    "🏖 Cap Ferret": {
        "region": "Gironde", "lat": 44.6300, "lon": -1.2520,
        "swell_opt": 265, "swell_tol": 40,
        "h_ideal": (1.0, 3.0), "priority": "standard",
        "webcam": "https://www.surf-report.com/webcams/cap-ferret-s1010.html",
    },
    # ───────── Vendée ─────────
    "🌊 La Sauzaie (Brétignolles)": {
        "region": "Vendée", "lat": 46.8350, "lon": -1.9120,
        "swell_opt": 270, "swell_tol": 45,
        "h_ideal": (1.0, 3.0), "priority": "standard",
        "webcam": "https://gosurf.fr/webcam/fr/146/Bretignolles-Sur-Mer-Plage-de-La-Sauzaie",
    },
    "🏄 Les Conches (Longeville)": {
        "region": "Vendée", "lat": 46.4150, "lon": -1.5000,
        "swell_opt": 250, "swell_tol": 45,
        "h_ideal": (1.0, 3.0), "priority": "standard",
        "webcam": "https://viewsurf.com/univers/surf/vue/18682-france-pays-de-la-loire-longeville-sur-mer-bud-bud",
    },
    # ───────── Finistère ─────────
    "🔥 La Torche": {
        "region": "Finistère", "lat": 47.8370, "lon": -4.3490,
        "swell_opt": 270, "swell_tol": 45,   # très exposé
        "h_ideal": (1.0, 3.5), "priority": "fire",
        "webcam": "https://www.winds-up.com/spot-la-torche-windsurf-kitesurf-50-webcam-live.html",
    },
    "🌊 La Palue (Crozon)": {
        "region": "Finistère", "lat": 48.2240, "lon": -4.5660,
        "swell_opt": 280, "swell_tol": 40,   # beach break costaud
        "h_ideal": (1.2, 3.5), "priority": "standard",
        "webcam": "https://www.surf-report.com/webcams/la-palue-s1038.html",
    },
}

TZ = pytz.timezone("Europe/Paris")

# ──────────────────────────────────────────
# FETCH DATA
# ──────────────────────────────────────────
def fetch_marine(lat, lon):
    r = requests.get("https://marine-api.open-meteo.com/v1/marine", params={
        "latitude": lat, "longitude": lon,
        "hourly": "wave_height,wave_period,wave_direction,"
                  "swell_wave_height,swell_wave_period,swell_wave_direction",
        "timezone": "Europe/Paris",
        "forecast_days": 3,
    }, timeout=10)
    r.raise_for_status()
    return r.json()

def fetch_weather(lat, lon):
    r = requests.get("https://api.open-meteo.com/v1/forecast", params={
        "latitude": lat, "longitude": lon,
        "hourly": "wind_speed_10m,wind_direction_10m,weather_code,cloud_cover",
        "timezone": "Europe/Paris",
        "forecast_days": 3,
        "wind_speed_unit": "kmh",
    }, timeout=10)
    r.raise_for_status()
    return r.json()

# ──────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────
def get_sun_times(lat, lon, date):
    loc = LocationInfo(latitude=lat, longitude=lon)
    s = sun(loc.observer, date=date, tzinfo=TZ)
    return s["sunrise"], s["sunset"]

def dir_label(deg):
    dirs = ["N","NE","E","SE","S","SO","O","NO"]
    return dirs[round(deg / 45) % 8]

def is_offshore(wind_dir):
    """Vent de terre pour Hossegor/Capbreton = Est (60-150°)"""
    return 50 <= wind_dir <= 160

# ──────────────────────────────────────────
# SCORING
# ──────────────────────────────────────────
def score_height(h, h_min, h_max):
    """Score adapté à la plage idéale de hauteur du spot."""
    if h < h_min * 0.5:  return 0.0
    if h < h_min:        return 3.0 + (h - h_min * 0.5) / (h_min * 0.5) * 3.0
    if h <= h_max:       return 8.0 + (h - h_min) / (h_max - h_min) * 2.0
    overshoot = h - h_max
    return max(0.0, 10.0 - overshoot * 2.5)

def score_period(p):
    if p < 8:  return 0.0
    if p < 10: return 3.0
    if p < 12: return 6.0
    if p < 14: return 8.5
    return 10.0

def score_direction(d, opt, tol):
    """Score de direction calé sur l'optimum du spot."""
    diff = min(abs(d - opt), 360 - abs(d - opt))
    if diff <= tol:        return 10.0
    if diff <= tol * 1.8:  return 7.0
    if diff <= tol * 3.0:  return 3.5
    if diff <= tol * 4.5:  return 1.5
    return 0.0

def score_wind(speed, direction):
    if is_offshore(direction):
        if speed < 10: return 10.0
        if speed < 20: return 8.0
        if speed < 30: return 5.0
        return 2.0
    else:
        if speed < 5:  return 6.0   # calme = acceptable
        if speed < 12: return 3.0
        if speed < 20: return 1.0
        return 0.0

def score_light(hour_dec, sunrise_h, sunset_h):
    golden_am_end = sunrise_h + 2.0
    golden_pm_start = sunset_h - 2.0
    if sunrise_h - 0.25 <= hour_dec <= golden_am_end:  return 10.0  # golden morning
    if golden_pm_start <= hour_dec <= sunset_h + 0.25: return 10.0  # golden evening
    if hour_dec < sunrise_h or hour_dec > sunset_h:    return 0.0   # nuit
    return 5.0  # lumière neutre

def score_cloud(cover):
    if cover < 20:  return 10.0
    if cover < 50:  return 7.0
    if cover < 75:  return 4.0
    return 1.0

def compute_score(wave_h, wave_p, swell_dir, wind_speed, wind_dir,
                  hour_dec, sunrise_h, sunset_h, cloud,
                  h_ideal, swell_opt, swell_tol):
    h_min, h_max = h_ideal
    s = {
        "Houle":     score_height(wave_h, h_min, h_max),
        "Période":   score_period(wave_p),
        "Direction": score_direction(swell_dir, swell_opt, swell_tol),
        "Vent":      score_wind(wind_speed, wind_dir),
        "Lumière":   score_light(hour_dec, sunrise_h, sunset_h),
        "Ciel":      score_cloud(cloud),
    }
    # Score 100% surf : lumière et ciel ne comptent plus dans la note.
    # (Ils restent calculés et exposés à part, pour juger les conditions de shooting.)
    w = {"Houle": 0.32, "Période": 0.25, "Direction": 0.23, "Vent": 0.20,
         "Lumière": 0.0, "Ciel": 0.0}
    total = sum(s[k] * w[k] for k in s)
    return round(total, 1), s

# ──────────────────────────────────────────
# ANALYSE
# ──────────────────────────────────────────
def analyze_spot(spot_name, spot_cfg):
    lat, lon = spot_cfg["lat"], spot_cfg["lon"]
    marine  = fetch_marine(lat, lon)
    weather = fetch_weather(lat, lon)

    now = datetime.now(TZ)
    today = now.date()
    sunrise, sunset = get_sun_times(lat, lon, today)
    sr_h = sunrise.hour + sunrise.minute / 60
    ss_h = sunset.hour + sunset.minute / 60

    times   = marine["hourly"]["time"]
    results = []

    for i, ts in enumerate(times):
        dt = datetime.fromisoformat(ts).replace(tzinfo=TZ)
        if dt < now:
            continue
        if (dt - now).total_seconds() > FORECAST_HOURS * 3600:
            break

        wave_h    = marine["hourly"]["wave_height"][i]    or 0
        wave_p    = marine["hourly"]["wave_period"][i]    or 0
        swell_dir = marine["hourly"]["swell_wave_direction"][i] or 0
        wind_spd  = weather["hourly"]["wind_speed_10m"][i]   or 0
        wind_dir  = weather["hourly"]["wind_direction_10m"][i] or 0
        cloud     = weather["hourly"]["cloud_cover"][i]   or 0

        hour_dec = dt.hour + dt.minute / 60
        score, breakdown = compute_score(
            wave_h, wave_p, swell_dir,
            wind_spd, wind_dir,
            hour_dec, sr_h, ss_h, cloud,
            spot_cfg["h_ideal"], spot_cfg["swell_opt"], spot_cfg["swell_tol"],
        )

        results.append({
            "dt": dt, "score": score, "breakdown": breakdown,
            "wave_h": wave_h, "wave_p": wave_p,
            "swell_dir": swell_dir, "swell_dir_label": dir_label(swell_dir),
            "wind_spd": wind_spd, "wind_dir": wind_dir,
            "wind_label": dir_label(wind_dir),
            "offshore": is_offshore(wind_dir),
            "cloud": cloud,
            "sunrise_h": sr_h, "sunset_h": ss_h,
        })

    return results

# ──────────────────────────────────────────
# MESSAGE TELEGRAM
# ──────────────────────────────────────────
def score_bar(s):
    filled = round(s)
    return "█" * filled + "░" * (10 - filled)

def clean_name(name):
    """Retire l'emoji de tête : '🔥 La Nord (Hossegor)' → 'La Nord (Hossegor)'."""
    return re.sub(r"^[^\w(]+", "", name).strip()

def slug(name):
    """Slug identique à generate_pages.py pour lier vers /spots/<slug>/."""
    s = unicodedata.normalize("NFKD", clean_name(name).lower()).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

def find_best_window(results):
    """Trouve la meilleure fenêtre continue ≥ ALERT_THRESHOLD."""
    good = [r for r in results if r["score"] >= ALERT_THRESHOLD]
    if not good:
        return None, []
    best = max(good, key=lambda x: x["score"])
    # Fenêtre de ±2h autour du pic
    window = [r for r in good
              if abs((r["dt"] - best["dt"]).total_seconds()) <= 7200]
    return best, window

def build_alert(spot_name, spot_cfg, results):
    """Retourne (message, is_fire) ou (None, False) si pas assez bon."""
    best, window = find_best_window(results)
    if not best:
        return None, False

    is_fire = best["score"] >= ALERT_FIRE and spot_cfg["priority"] == "fire"

    # Quand
    now = datetime.now(TZ)
    delta = best["dt"] - now
    hours_away = delta.total_seconds() / 3600
    days_away  = int(hours_away // 24)

    if hours_away < 2:
        quand    = "maintenant"
        urgence  = ""
    elif hours_away < 24:
        quand    = f"aujourd'hui à {best['dt'].strftime('%Hh')}"
        urgence  = f"  ⏱ dans {int(hours_away)}h"
    elif days_away == 1:
        quand    = f"demain à {best['dt'].strftime('%Hh')}"
        urgence  = "  ⏱ J-1"
    elif days_away == 2:
        quand    = f"après-demain ({jour_fr(best['dt'])}) à {best['dt'].strftime('%Hh')}"
        urgence  = "  ⏱ J-2"
    else:
        quand    = f"{jour_fr(best['dt'])} {best['dt'].strftime('%d/%m')} à {best['dt'].strftime('%Hh')}"
        urgence  = f"  ⏱ J-{days_away}"

    # Header
    nom = clean_name(spot_name)
    if is_fire:
        header = f"🔥 GROSSE SESSION — {nom}"
    else:
        header = f"🟢 GO — {nom}"

    # Durée de la fenêtre
    if len(window) >= 2:
        t_start = window[0]["dt"].strftime("%Hh")
        t_end   = window[-1]["dt"].strftime("%Hh")
        fenetre = f"{t_start}–{t_end}"
    else:
        fenetre = best["dt"].strftime("%Hh")

    wind_info = (f"{best['wind_spd']:.0f}km/h {best['wind_label']}"
                 f"{' ✅' if best['offshore'] else ' ⚠️ onshore'}")

    msg  = f"{header}\n"
    msg += f"{'─' * 28}\n"
    msg += f"📅 <b>{quand.capitalize()}</b>{urgence}\n"
    msg += f"🕐 Fenêtre : {fenetre}\n"
    msg += f"⭐ Score : <b>{best['score']}/10</b>  {score_bar(best['score'])}\n\n"
    msg += f"🌊 <b>{best['wave_h']:.1f}m</b> · {best['wave_p']:.0f}s · {best['swell_dir_label']} {best['swell_dir']:.0f}°\n"
    msg += f"💨 {wind_info}\n"
    msg += f"👉 <a href=\"{SITE_URL}/spots/{slug(spot_name)}/\">voir la fiche</a>"

    return msg, is_fire

# ──────────────────────────────────────────
# TELEGRAM
# ──────────────────────────────────────────
def send(text, disable_notification=False):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        raise SystemExit("❌ TELEGRAM_TOKEN / CHAT_ID manquants. "
                         "Crée un fichier .env à côté du script (voir .env.example).")
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    r = requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_notification": disable_notification,
    }, timeout=10)
    return r.json()

# ──────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────
def run():
    now = datetime.now(TZ)
    print(f"[{now.strftime('%H:%M')}] SurfAlert démarré...")

    alerts = []   # (score, msg, is_fire, spot_name)

    for spot_name, spot_cfg in SPOTS.items():
        try:
            print(f"  → Analyse {spot_name}...")
            results = analyze_spot(spot_name, spot_cfg)
            msg, is_fire = build_alert(spot_name, spot_cfg, results)
            if msg:
                best_score = max(r["score"] for r in results)
                alerts.append((best_score, msg, is_fire, spot_name))
        except Exception as e:
            print(f"  ❌ Erreur sur {spot_name}: {e}")

    if not alerts:
        # Silence total — pas de message parasite
        print("  → Rien d'intéressant dans les 72h. Aucun message envoyé.")
        return

    # Trie par score décroissant → un seul message digest (le meilleur en détail + les autres en liste)
    alerts.sort(reverse=True)
    top_score, top_msg, top_fire, top_name = alerts[0]
    digest = top_msg
    if len(alerts) > 1:
        digest += "\n\n<b>Aussi go :</b>\n"
        digest += "\n".join(
            f"• {clean_name(name)} — {score}/10  (<a href=\"{SITE_URL}/spots/{slug(name)}/\">fiche</a>)"
            for score, _msg, _fire, name in alerts[1:]
        )
    digest += f"\n\n🌊 <a href=\"{SITE_URL}/\">Tous les spots sur swelleo</a>"
    send(digest, disable_notification=not top_fire)
    print(f"  ✅ Digest envoyé : {len(alerts)} spot(s), top {top_name} ({top_score}/10)")


if __name__ == "__main__":
    run()
