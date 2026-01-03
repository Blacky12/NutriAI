from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from .core.config import get_settings
from .core.database import create_tables, engine
from .models import User, Meal
from .api.v1.endpoints import meals, admin, auth

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting NutriAI API...")
    create_tables()
    print("✅ Database ready!")
    yield
    print("👋 Shutting down...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# CORS_ORIGINS est déjà parsé par le validateur (gère "*" et listes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(meals.router, prefix="/api/v1/meals", tags=["meals"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])

# Servir les fichiers statiques
static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Landing page par défaut"""
    static_file = os.path.join(static_dir, "index.html")
    if os.path.exists(static_file):
        with open(static_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content=f"<h1>NutriAI API</h1><p>Version {settings.VERSION}</p>")


@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard():
    """Dashboard admin"""
    static_file = os.path.join(static_dir, "dashboard.html")
    if os.path.exists(static_file):
        with open(static_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Dashboard non disponible</h1>", status_code=404)


@app.get("/pricing", response_class=HTMLResponse)
async def pricing_page():
    """Page pricing"""
    static_file = os.path.join(static_dir, "pricing.html")
    if os.path.exists(static_file):
        with open(static_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Page non disponible</h1>", status_code=404)


@app.get("/landing", response_class=HTMLResponse)
@app.get("/index", response_class=HTMLResponse)
async def landing_page():
    """Landing page"""
    static_file = os.path.join(static_dir, "index.html")
    if os.path.exists(static_file):
        with open(static_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Page non disponible</h1>", status_code=404)


@app.get("/legal", response_class=HTMLResponse)
async def legal_page():
    """Mentions légales"""
    static_file = os.path.join(static_dir, "legal.html")
    if os.path.exists(static_file):
        with open(static_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Page non disponible</h1>", status_code=404)


@app.get("/privacy", response_class=HTMLResponse)
async def privacy_page():
    """Politique de confidentialité"""
    static_file = os.path.join(static_dir, "privacy.html")
    if os.path.exists(static_file):
        with open(static_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Page non disponible</h1>", status_code=404)


@app.get("/cookies", response_class=HTMLResponse)
async def cookies_page():
    """Politique des cookies"""
    static_file = os.path.join(static_dir, "cookies.html")
    if os.path.exists(static_file):
        with open(static_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Page non disponible</h1>", status_code=404)


@app.get("/health")
async def health():
    return {"status": "healthy"}

