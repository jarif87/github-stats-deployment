from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import Response, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os
import threading
import time
import requests
from dotenv import load_dotenv
from github_client import GitHubClient
from trophy_calculator import calculate_trophies
from config import Config
from themes import get_theme, THEMES
from svg_generators import generate_stats_card, generate_languages_chart, generate_trophies_display
from pathlib import Path
from contextlib import asynccontextmanager
import hashlib

load_dotenv()

# ─────────────────────────────────────────────
# In-memory cache  {key: (timestamp, value)}
# ─────────────────────────────────────────────
_cache: dict = {}
CACHE_TTL = 3600  # 1 hour

def cache_get(key: str):
    entry = _cache.get(key)
    if entry and (time.time() - entry[0]) < CACHE_TTL:
        return entry[1]
    return None

def cache_set(key: str, value):
    _cache[key] = (time.time(), value)

def cache_clear(username: str = None):
    if username:
        keys = [k for k in _cache if k.startswith(username)]
        for k in keys:
            del _cache[k]
    else:
        _cache.clear()

# ─────────────────────────────────────────────
# Placeholder SVGs – shown while server warms up
# or when GitHub API fails. Never shows broken image.
# ─────────────────────────────────────────────
def placeholder_trophies_svg(message: str = "Loading trophies…") -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="660" height="120">
  <rect width="660" height="120" rx="12" fill="#1a1b27"/>
  <text x="330" y="52" text-anchor="middle" fill="#70a5fd"
        font-family="Arial,sans-serif" font-size="22">🏆</text>
  <text x="330" y="78" text-anchor="middle" fill="#a9b1d6"
        font-family="Arial,sans-serif" font-size="13">{message}</text>
  <text x="330" y="100" text-anchor="middle" fill="#565f89"
        font-family="Arial,sans-serif" font-size="11">Refresh in a few seconds</text>
</svg>'''

def placeholder_stats_svg(message: str = "Loading stats…") -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="495" height="195">
  <rect width="495" height="195" rx="12" fill="#1a1b27"/>
  <text x="247" y="85" text-anchor="middle" fill="#70a5fd"
        font-family="Arial,sans-serif" font-size="22">📊</text>
  <text x="247" y="112" text-anchor="middle" fill="#a9b1d6"
        font-family="Arial,sans-serif" font-size="13">{message}</text>
  <text x="247" y="135" text-anchor="middle" fill="#565f89"
        font-family="Arial,sans-serif" font-size="11">Refresh in a few seconds</text>
</svg>'''

def placeholder_languages_svg(message: str = "Loading languages…") -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200">
  <rect width="600" height="200" rx="12" fill="#1a1b27"/>
  <text x="300" y="88" text-anchor="middle" fill="#70a5fd"
        font-family="Arial,sans-serif" font-size="22">💻</text>
  <text x="300" y="115" text-anchor="middle" fill="#a9b1d6"
        font-family="Arial,sans-serif" font-size="13">{message}</text>
  <text x="300" y="138" text-anchor="middle" fill="#565f89"
        font-family="Arial,sans-serif" font-size="11">Refresh in a few seconds</text>
</svg>'''

# ─────────────────────────────────────────────
# Lifespan: NO self-ping (useless on Render free tier).
# Use UptimeRobot (free) to ping /ping every 5 min instead.
# ─────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("✓ Server started. Use UptimeRobot to ping /ping every 5 min to stay warm.")
    print("  https://uptimerobot.com  →  monitor: https://github-stats-deployment.onrender.com/ping")
    yield

app = FastAPI(
    title=Config.API_TITLE,
    description=Config.API_DESCRIPTION,
    version=Config.API_VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if GITHUB_TOKEN:
    GITHUB_TOKEN = GITHUB_TOKEN.strip().strip('"').strip("'")
client = GitHubClient(token=GITHUB_TOKEN)
Config.validate()

BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


# ─────────────────────────────────────────────
# /ping  – Ultra-fast keep-alive endpoint
#          Returns instantly, no DB/API calls.
#          Point UptimeRobot here (every 5 min).
# ─────────────────────────────────────────────
@app.get("/ping")
async def ping():
    return "pong"


# ─────────────────────────────────────────────
# /health – Lightweight status check.
#            Does NOT call GitHub API so it
#            always returns fast (< 5 ms).
# ─────────────────────────────────────────────
@app.get("/health")
async def health():
    return {
        "status": "ok",
        "github_token": bool(GITHUB_TOKEN),
        "cache_entries": len(_cache),
        "uptime": "running"
    }


@app.get("/")
async def root():
    return {
        "name": Config.API_TITLE,
        "description": Config.API_DESCRIPTION,
        "version": Config.API_VERSION,
        "endpoints": {
            "stats":      "/stats?username=USER&theme=midnight",
            "languages":  "/languages?username=USER&theme=midnight&layout=vertical",
            "trophies":   "/trophies?username=USER&theme=midnight&style=modern",
            "dashboard":  "/dashboard?username=USER&theme=midnight"
        },
        "themes": list(THEMES.keys()),
        "keep_alive_tip": "Point UptimeRobot at /ping every 5 min to prevent Render sleep",
    }


# ─────────────────────────────────────────────
# /stats
# ─────────────────────────────────────────────
@app.get("/stats", response_class=Response)
async def github_stats(
    username: str = Query(...),
    theme: str = Query("midnight", enum=list(THEMES.keys())),
    hide: str = Query(""),
    v: str = Query(None),
    t: str = Query(None)
):
    cache_key = f"{username}:stats:{theme}:{hide}"
    cached = cache_get(cache_key)
    if cached:
        return Response(content=cached, media_type="image/svg+xml", headers={
            "Cache-Control": "public, max-age=3600",
            "X-Cache": "HIT"
        })

    try:
        user_stats = client.get_user_stats(username)
        selected_theme = get_theme(theme)
        hidden = [x.strip() for x in hide.split(",") if x.strip()]
        svg = generate_stats_card(username, user_stats, selected_theme, hidden)
        cache_set(cache_key, svg)
        return Response(content=svg, media_type="image/svg+xml", headers={
            "Cache-Control": "public, max-age=3600",
            "X-Cache": "MISS"
        })
    except Exception as e:
        # Return placeholder – never a broken image
        print(f"[stats] Error for {username}: {e}")
        return Response(
            content=placeholder_stats_svg(f"Could not load stats for {username}"),
            media_type="image/svg+xml",
            headers={"Cache-Control": "no-cache"}
        )


# ─────────────────────────────────────────────
# /languages
# ─────────────────────────────────────────────
@app.get("/languages", response_class=Response)
async def languages_chart(
    username: str = Query(...),
    theme: str = Query("midnight", enum=list(THEMES.keys())),
    layout: str = Query("horizontal", enum=["vertical", "horizontal"]),
    top: int = Query(10, ge=3, le=15),
    animated: bool = Query(True),
    v: str = Query(None),
    t: str = Query(None)
):
    cache_key = f"{username}:languages:{theme}:{layout}:{top}:{animated}"
    cached = cache_get(cache_key)
    if cached:
        return Response(content=cached, media_type="image/svg+xml", headers={
            "Cache-Control": "public, max-age=3600",
            "X-Cache": "HIT"
        })

    try:
        all_languages = client.get_top_languages(username, include_all=True)
        selected_theme = get_theme(theme)
        svg = generate_languages_chart(username, all_languages, selected_theme, layout, top, animated)
        cache_set(cache_key, svg)
        return Response(content=svg, media_type="image/svg+xml", headers={
            "Cache-Control": "public, max-age=3600",
            "X-Cache": "MISS"
        })
    except Exception as e:
        print(f"[languages] Error for {username}: {e}")
        return Response(
            content=placeholder_languages_svg(f"Could not load languages for {username}"),
            media_type="image/svg+xml",
            headers={"Cache-Control": "no-cache"}
        )


# ─────────────────────────────────────────────
# /trophies
# ─────────────────────────────────────────────
@app.get("/trophies", response_class=Response)
async def trophies(
    username: str = Query(...),
    theme: str = Query("midnight", enum=list(THEMES.keys())),
    columns: int = Query(6, ge=2, le=8),
    style: str = Query("modern", enum=["modern", "classic", "minimal"]),
    v: str = Query(None),
    t: str = Query(None)
):
    cache_key = f"{username}:trophies:{theme}:{columns}:{style}"
    cached = cache_get(cache_key)
    if cached:
        return Response(content=cached, media_type="image/svg+xml", headers={
            "Cache-Control": "public, max-age=3600",
            "X-Cache": "HIT"
        })

    try:
        stats = client.get_user_stats(username)
        trophies_data = calculate_trophies(stats)
        selected_theme = get_theme(theme)
        svg = generate_trophies_display(username, trophies_data, selected_theme, columns, style)
        cache_set(cache_key, svg)
        return Response(content=svg, media_type="image/svg+xml", headers={
            "Cache-Control": "public, max-age=3600",
            "X-Cache": "MISS"
        })
    except Exception as e:
        # NEVER raise HTTP 500 for SVG endpoints – return placeholder instead
        print(f"[trophies] Error for {username}: {e}")
        return Response(
            content=placeholder_trophies_svg(f"Could not load trophies for {username}"),
            media_type="image/svg+xml",
            headers={"Cache-Control": "no-cache"}
        )


# ─────────────────────────────────────────────
# /dashboard
# ─────────────────────────────────────────────
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    username: str = Query(...),
    theme: str = Query("midnight", enum=list(THEMES.keys()))
):
    selected_theme = get_theme(theme)
    return templates.TemplateResponse("dashboard.html", {
        "request":          request,
        "username":         username,
        "bg":               selected_theme["bg"],
        "bg_card":          selected_theme["bg_card"],
        "primary":          selected_theme["primary"],
        "primary_gradient": selected_theme["primary_gradient"],
        "secondary":        selected_theme["secondary"],
        "text":             selected_theme["text"],
        "text_secondary":   selected_theme["text_secondary"],
        "border":           selected_theme["border"]
    })


@app.get("/api/dashboard-data")
async def dashboard_data(username: str = Query(...)):
    cache_key = f"{username}:dashboard"
    cached = cache_get(cache_key)
    if cached:
        return cached
    try:
        stats     = client.get_user_stats(username)
        languages = client.get_top_languages(username, include_all=True)
        trophies_data = calculate_trophies(stats)
        result = {"stats": stats, "languages": languages, "trophies": trophies_data}
        cache_set(cache_key, result)
        return result
    except Exception as e:
        return {"error": str(e)}


@app.get("/themes")
async def list_themes():
    return {"themes": list(THEMES.keys()), "details": THEMES}


@app.get("/clear-cache")
async def clear_cache_endpoint(username: str = Query(None)):
    cache_clear(username)
    return {"message": f"Cache cleared for {username if username else 'all users'}"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)