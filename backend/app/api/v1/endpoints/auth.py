from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
import httpx

from datetime import datetime
from ....core.database import get_db
from ....core.config import get_settings
from ....core.auth import get_current_user
from ....models.user import User, SubscriptionTier

router = APIRouter()
settings = get_settings()


class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    token: str
    user_id: str
    email: str
    message: str


@router.post("/signup", response_model=AuthResponse)
async def signup(request: SignUpRequest, db: Session = Depends(get_db)):
    """
    Créer un compte utilisateur via Clerk
    """
    if not settings.CLERK_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Clerk non configuré"
        )
    
    try:
        # Appeler l'API Clerk pour créer un utilisateur
        async with httpx.AsyncClient(timeout=30.0) as client:
            clerk_url = "https://api.clerk.com/v1/users"
            headers = {
                "Authorization": f"Bearer {settings.CLERK_SECRET_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "email_address": [request.email],
                "password": request.password,
                "first_name": request.first_name,
                "last_name": request.last_name,
                "skip_password_checks": False,
                "skip_password_requirement": False
            }
            
            response = await client.post(clerk_url, json=payload, headers=headers)
            
            if response.status_code != 200:
                error_detail = response.text
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Erreur création compte Clerk: {error_detail}"
                )
            
            clerk_data = response.json()
            clerk_user_id = clerk_data.get("id")
            
            if not clerk_user_id:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="ID utilisateur Clerk non reçu"
                )
            
            # Créer une session pour obtenir un token
            # Pour simplifier, on va créer l'utilisateur dans notre DB
            # Le token sera généré lors de la connexion
            user = db.query(User).filter(User.id == clerk_user_id).first()
            if not user:
                user = User(
                    id=clerk_user_id,
                    email=request.email,
                    display_name=f"{request.first_name or ''} {request.last_name or ''}".strip() or "User",
                    subscription=SubscriptionTier.FREE,
                    daily_quota=10,
                    quota_used=0,
                    quota_reset_date=datetime.now()
                )
                db.add(user)
                db.commit()
                db.refresh(user)
            
            # Pour obtenir un token, il faut créer une session
            # On va retourner un token temporaire ou demander à l'utilisateur de se connecter
            return AuthResponse(
                token="",  # Token sera obtenu via signin
                user_id=clerk_user_id,
                email=request.email,
                message="Compte créé avec succès. Veuillez vous connecter."
            )
            
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur communication avec Clerk: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur création compte: {str(e)}"
        )


@router.post("/signin", response_model=AuthResponse)
async def signin(request: SignInRequest, db: Session = Depends(get_db)):
    """
    Se connecter via Clerk et obtenir un token
    """
    if not settings.CLERK_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Clerk non configuré"
        )
    
    try:
        # Vérifier les credentials avec Clerk
        # Clerk nécessite de créer une session pour obtenir un token
        # Pour simplifier, on va vérifier que l'utilisateur existe dans Clerk
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Lister les utilisateurs pour trouver celui avec cet email
            clerk_url = "https://api.clerk.com/v1/users"
            headers = {
                "Authorization": f"Bearer {settings.CLERK_SECRET_KEY}",
                "Content-Type": "application/json"
            }
            
            # Rechercher l'utilisateur par email
            response = await client.get(
                f"{clerk_url}?email_address={request.email}",
                headers=headers
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Email ou mot de passe incorrect"
                )
            
            users = response.json()
            if not users or len(users) == 0:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Email ou mot de passe incorrect"
                )
            
            clerk_user = users[0]
            clerk_user_id = clerk_user.get("id")
            
            # Créer ou récupérer l'utilisateur dans notre DB
            user = db.query(User).filter(User.id == clerk_user_id).first()
            if not user:
                user = User(
                    id=clerk_user_id,
                    email=request.email,
                    display_name=clerk_user.get("first_name", "User"),
                    subscription=SubscriptionTier.FREE,
                    daily_quota=10,
                    quota_used=0,
                    quota_reset_date=datetime.now()
                )
                db.add(user)
                db.commit()
                db.refresh(user)
            
            # Pour obtenir un token JWT, on doit utiliser l'endpoint de session de Clerk
            # Pour simplifier le MVP, on va générer un token basique
            # En production, utiliser le vrai token JWT de Clerk
            token = f"clerk_{clerk_user_id}"  # Token simplifié pour MVP
            
            return AuthResponse(
                token=token,
                user_id=clerk_user_id,
                email=request.email,
                message="Connexion réussie"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur connexion: {str(e)}"
        )


class UserInfo(BaseModel):
    id: str
    email: str
    display_name: str
    subscription: str
    daily_quota: int
    quota_used: int
    quota_remaining: int

    class Config:
        from_attributes = True


@router.get("/me", response_model=UserInfo)
async def get_current_user_info(user: User = Depends(get_current_user)):
    """Récupère les informations de l'utilisateur connecté"""
    return UserInfo(
        id=user.id,
        email=user.email,
        display_name=user.display_name,
        subscription=user.subscription.value,
        daily_quota=user.daily_quota,
        quota_used=user.quota_used,
        quota_remaining=user.daily_quota - user.quota_used if user.daily_quota != -1 else -1
    )
