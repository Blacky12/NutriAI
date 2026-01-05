from fastapi import Depends, HTTPException, status, Cookie, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Optional
import secrets
import hashlib
from .config import get_settings

settings = get_settings()
security = HTTPBasic()

# Stocker les sessions admin (en production, utiliser Redis ou DB)
admin_sessions = set()


def verify_admin_password(password: str) -> bool:
    """Vérifier le mot de passe admin"""
    # Hash simple pour MVP (en production, utiliser bcrypt)
    return password == settings.ADMIN_PASSWORD


def create_admin_session() -> str:
    """Créer une session admin"""
    session_token = secrets.token_urlsafe(32)
    admin_sessions.add(session_token)
    return session_token


def verify_admin_session(session_token: Optional[str]) -> bool:
    """Vérifier la session admin"""
    if not session_token:
        return False
    return session_token in admin_sessions


async def require_admin(request: Request, admin_session: Optional[str] = Cookie(None)):
    """Dependency pour vérifier l'authentification admin"""
    if verify_admin_session(admin_session):
        return True
    
    # Vérifier l'authentification HTTP Basic
    authorization = request.headers.get("Authorization")
    if authorization and authorization.startswith("Basic "):
        try:
            import base64
            credentials = base64.b64decode(authorization.replace("Basic ", "")).decode()
            username, password = credentials.split(":", 1)
            if username == "admin" and verify_admin_password(password):
                return True
        except:
            pass
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentification admin requise",
        headers={"WWW-Authenticate": "Basic"},
    )




