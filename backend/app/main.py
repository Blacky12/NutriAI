from fastapi import FastAPI, Request
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
async def admin_dashboard(request: Request):
    """Dashboard admin - Authentification requise"""
    from .core.admin_auth import verify_admin_session, create_admin_session
    from fastapi import Cookie
    
    admin_session = request.cookies.get("admin_session")
    
    # Vérifier si déjà authentifié
    if not verify_admin_session(admin_session):
        # Afficher page de login
        login_html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Connexion Admin - NutriAI</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        .login-box {
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            max-width: 400px;
            width: 100%;
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 30px;
            text-align: center;
            font-size: 24px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 500;
        }
        input[type="password"] {
            width: 100%;
            padding: 14px;
            margin: 0;
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input[type="password"]:focus {
            outline: none;
            border-color: #3498db;
        }
        button {
            width: 100%;
            padding: 14px;
            background: #3498db;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.3s;
            margin-top: 10px;
        }
        button:hover {
            background: #2980b9;
        }
        button:active {
            transform: scale(0.98);
        }
        .error {
            color: #e74c3c;
            margin-top: 15px;
            text-align: center;
            font-size: 14px;
            min-height: 20px;
        }
        .info {
            color: #7f8c8d;
            font-size: 12px;
            margin-top: 15px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="login-box">
        <h1>🔐 Connexion Admin</h1>
        <form id="loginForm">
            <div class="form-group">
                <label for="password">Mot de passe administrateur</label>
                <input type="password" id="password" name="password" placeholder="Entrez le mot de passe" required autofocus>
            </div>
            <button type="submit">Se connecter</button>
            <div id="error" class="error"></div>
            <div class="info">Mot de passe par défaut : admin123</div>
        </form>
    </div>
    <script>
        document.getElementById('loginForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const passwordInput = document.getElementById('password');
            const errorDiv = document.getElementById('error');
            const password = passwordInput.value.trim();
            
            if (!password) {
                errorDiv.textContent = 'Veuillez entrer un mot de passe';
                return;
            }
            
            errorDiv.textContent = '';
            passwordInput.disabled = true;
            
            try {
                const response = await fetch('/api/v1/admin/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    credentials: 'include',
                    body: JSON.stringify({password: password})
                });
                
                if (response.ok) {
                    window.location.reload();
                } else {
                    const data = await response.json().catch(() => ({}));
                    errorDiv.textContent = data.detail || 'Mot de passe incorrect';
                    passwordInput.disabled = false;
                    passwordInput.focus();
                }
            } catch (error) {
                errorDiv.textContent = 'Erreur de connexion. Veuillez réessayer.';
                passwordInput.disabled = false;
                passwordInput.focus();
            }
        });
        
        // Focus sur le champ password au chargement
        document.getElementById('password').focus();
    </script>
</body>
</html>"""
        return HTMLResponse(content=login_html)
    
    # Afficher le dashboard
    static_file = os.path.join(static_dir, "dashboard.html")
    if os.path.exists(static_file):
        with open(static_file, "r", encoding="utf-8") as f:
            content = f.read()
            # Ajouter bouton déconnexion avec style amélioré
            logout_button = '''<div style="text-align:right; margin-bottom:15px;">
                <a href="/api/v1/admin/logout" 
                   style="display:inline-block; padding:8px 16px; background:#e74c3c; color:white; text-decoration:none; border-radius:4px; font-weight:500; transition:background 0.3s;"
                   onmouseover="this.style.background='#c0392b'" 
                   onmouseout="this.style.background='#e74c3c'">
                    🚪 Déconnexion
                </a>
            </div>'''
            content = content.replace('<header>', f'<header>{logout_button}')
            return HTMLResponse(content=content)
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

