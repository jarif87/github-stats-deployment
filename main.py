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

load_dotenv()

def keep_alive():
    while True:
        try:
            requests.get(
                "https://github-stats-deployment.onrender.com/health",
                timeout=10
            )
            print("Keep-alive ping sent")
        except Exception as e:
            print(f"Keep-alive ping failed: {e}")
        time.sleep(240)

@asynccontextmanager
async def lifespan(app: FastAPI):
    threading.Thread(target=keep_alive, daemon=True).start()
    print("✓ Keep-alive thread started (pinging every 4 minutes)")
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


@app.get("/health")
async def health():
    """Lightweight health check endpoint for keep-alive pings"""
    return {"status": "ok"}


@app.get("/")
async def root():
    return {
        "name": Config.API_TITLE,
        "description": Config.API_DESCRIPTION,
        "version": Config.API_VERSION,
        "endpoints": {
            "stats": "/stats?username=USER&theme=midnight",
            "languages": "/languages?username=USER&theme=midnight&layout=vertical",
            "trophies": "/trophies?username=USER&theme=midnight&style=modern",
            "dashboard": "/dashboard?username=USER&theme=midnight"
        },
        "themes": list(THEMES.keys()),
        "features": [
            "Vertical bar charts for languages",
            "Animated SVG charts",
            "Multiple layout options",
            "Responsive dashboard",
            "Achievement trophies",
            "Contribution streaks",
            "Real-time data",
            "Interactive chart switching"
        ]
    }


@app.get("/stats", response_class=Response)
async def github_stats(
    username: str = Query(...),
    theme: str = Query("midnight", enum=list(THEMES.keys())),
    hide: str = Query(""),
    v: str = Query(None),
    t: str = Query(None)
):
    try:
        user_stats = client.get_user_stats(username)
        selected_theme = get_theme(theme)
        hidden = [x.strip() for x in hide.split(",") if x.strip()]
        svg = generate_stats_card(username, user_stats, selected_theme, hidden)
        return Response(content=svg, media_type="image/svg+xml", headers={
            "Cache-Control": "public, max-age=3600",
            "Content-Type": "image/svg+xml"
        })
    except Exception as e:
        from svg_generators.stats_card import generate_error_svg
        return Response(content=generate_error_svg(str(e)), media_type="image/svg+xml")


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
    try:
        all_languages = client.get_top_languages(username, include_all=True)
        selected_theme = get_theme(theme)
        svg = generate_languages_chart(username, all_languages, selected_theme, layout, top, animated)
        return Response(content=svg, media_type="image/svg+xml", headers={
            "Cache-Control": "public, max-age=3600"
        })
    except Exception as e:
        error_svg = f'''<svg width="600" height="200">
            <rect width="600" height="200" fill="#1a1a2e" rx="16"/>
            <text x="300" y="100" fill="#ef4444" text-anchor="middle" font-family="'Inter', sans-serif" font-size="14">Error: {str(e)[:50]}</text>
        </svg>'''
        return Response(content=error_svg, media_type="image/svg+xml")


@app.get("/trophies", response_class=Response)
async def trophies(
    username: str = Query(...),
    theme: str = Query("midnight", enum=list(THEMES.keys())),
    columns: int = Query(6, ge=2, le=8),
    style: str = Query("modern", enum=["modern", "classic", "minimal"]),
    v: str = Query(None),
    t: str = Query(None)
):
    try:
        stats = client.get_user_stats(username)
        trophies_data = calculate_trophies(stats)
        selected_theme = get_theme(theme)
        svg = generate_trophies_display(username, trophies_data, selected_theme, columns, style)
        return Response(content=svg, media_type="image/svg+xml", headers={
            "Cache-Control": "public, max-age=3600"
        })
    except Exception as e:
        raise HTTPException(500, detail=str(e))


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    username: str = Query(...),
    theme: str = Query("midnight", enum=list(THEMES.keys()))
):
    selected_theme = get_theme(theme)
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "username": username,
        "bg": selected_theme["bg"],
        "bg_card": selected_theme["bg_card"],
        "primary": selected_theme["primary"],
        "primary_gradient": selected_theme["primary_gradient"],
        "secondary": selected_theme["secondary"],
        "text": selected_theme["text"],
        "text_secondary": selected_theme["text_secondary"],
        "border": selected_theme["border"]
    })


@app.get("/api/dashboard-data")
async def dashboard_data(username: str = Query(...)):
    try:
        stats = client.get_user_stats(username)
        languages = client.get_top_languages(username, include_all=True)
        trophies_data = calculate_trophies(stats)
        return {"stats": stats, "languages": languages, "trophies": trophies_data}
    except Exception as e:
        return {"error": str(e)}


@app.get("/themes")
async def list_themes():
    return {"themes": list(THEMES.keys()), "details": THEMES}


@app.get("/clear-cache")
async def clear_cache(username: str = Query(None)):
    client.clear_cache(username)
    return {"message": f"Cache cleared for {username if username else 'all users'}"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)