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
        print("❌ Clerk non configuré")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Clerk non configuré"
        )
    
    try:
        print(f"📝 Tentative création compte pour: {request.email}")
        
        # Appeler l'API Clerk pour créer un utilisateur
        async with httpx.AsyncClient(timeout=30.0) as client:
            clerk_url = "https://api.clerk.com/v1/users"
            headers = {
                "Authorization": f"Bearer {settings.CLERK_SECRET_KEY}",
                "Content-Type": "application/json"
            }
            
            # Format correct pour l'API Clerk
            payload = {
                "email_address": [request.email],
                "password": request.password,
                "skip_password_checks": True,  # Pour MVP : désactiver vérification pwned passwords
                "skip_password_requirement": False,
            }
            
            if request.first_name:
                payload["first_name"] = request.first_name
            if request.last_name:
                payload["last_name"] = request.last_name
            
            print(f"📤 Envoi requête à Clerk: {clerk_url}")
            response = await client.post(clerk_url, json=payload, headers=headers)
            
            print(f"📥 Réponse Clerk: status={response.status_code}, body={response.text[:200]}")
            
            if response.status_code not in [200, 201]:
                error_detail = response.text
                print(f"❌ Erreur Clerk: {error_detail}")
                
                # Parser l'erreur pour donner un message plus clair
                try:
                    error_json = response.json()
                    if "errors" in error_json and len(error_json["errors"]) > 0:
                        error_message = error_json["errors"][0].get("message", "Erreur inconnue")
                        # Message plus user-friendly
                        if "pwned" in error_message.lower() or "data breach" in error_message.lower():
                            error_message = "Ce mot de passe a été compromis dans une fuite de données. Veuillez utiliser un mot de passe plus sécurisé."
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=error_message
                        )
                except:
                    pass
                
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Erreur création compte: {error_detail[:200]}"
                )
            
            clerk_data = response.json()
            clerk_user_id = clerk_data.get("id")
            
            print(f"✅ Utilisateur Clerk créé: {clerk_user_id}")
            
            if not clerk_user_id:
                print("❌ ID utilisateur Clerk non reçu")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="ID utilisateur Clerk non reçu"
                )
            
            # Créer l'utilisateur dans notre DB
            try:
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
                    print(f"✅ Utilisateur créé dans DB: {clerk_user_id}")
                else:
                    print(f"ℹ️ Utilisateur existe déjà dans DB: {clerk_user_id}")
            except Exception as db_error:
                print(f"❌ Erreur DB: {str(db_error)}")
                db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Erreur sauvegarde utilisateur: {str(db_error)}"
                )
            
            # Générer un token simplifié pour MVP
            token = f"clerk_{clerk_user_id}"
            
            return AuthResponse(
                token=token,
                user_id=clerk_user_id,
                email=request.email,
                message="Compte créé avec succès"
            )
            
    except HTTPException:
        raise
    except httpx.HTTPError as e:
        print(f"❌ Erreur HTTP Clerk: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur communication avec Clerk: {str(e)}"
        )
    except Exception as e:
        print(f"❌ Erreur inattendue: {str(e)}")
        import traceback
        traceback.print_exc()
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
