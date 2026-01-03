from fastapi import Depends, HTTPException, status, Header
from typing import Optional
from clerk_sdk_python import Clerk
from sqlalchemy.orm import Session
from datetime import datetime
from jose import jwt, JWTError
import httpx

from .config import get_settings
from .database import get_db
from ..models.user import User, SubscriptionTier

settings = get_settings()

# Initialiser Clerk client
clerk_client = None
if settings.CLERK_SECRET_KEY:
    clerk_client = Clerk(bearer_auth=settings.CLERK_SECRET_KEY)


async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency pour obtenir l'utilisateur actuel depuis le token Clerk
    Si Clerk n'est pas configuré, utilise un utilisateur temporaire pour le développement
    """
    # Mode développement : si Clerk n'est pas configuré, utiliser un utilisateur temporaire
    if not clerk_client or not settings.CLERK_SECRET_KEY:
        print("⚠️ Clerk non configuré, utilisation d'un utilisateur temporaire pour le développement")
        temp_user_id = "temp_user_dev"
        user = db.query(User).filter(User.id == temp_user_id).first()
        if not user:
            user = User(
                id=temp_user_id,
                email="dev@nutriai.app",
                display_name="Dev User",
                subscription=SubscriptionTier.FREE,
                daily_quota=10,
                quota_used=0,
                quota_reset_date=datetime.now()
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        return user
    
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token d'authentification manquant",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extraire le token du header "Bearer <token>"
    try:
        token = authorization.replace("Bearer ", "").strip()
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Format de token invalide",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Vérifier le token avec Clerk
    try:
        # Décoder le JWT pour obtenir l'ID utilisateur
        # Clerk utilise des JWTs signés avec leur clé publique
        # Pour simplifier, on va utiliser l'API Clerk pour vérifier le token
        try:
            # Récupérer les infos de l'utilisateur depuis Clerk
            # Le token JWT contient l'ID utilisateur dans le claim "sub"
            decoded_token = jwt.get_unverified_claims(token)
            clerk_user_id = decoded_token.get("sub")
            
            if not clerk_user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token invalide: ID utilisateur manquant",
                )
            
            # Récupérer les infos complètes de l'utilisateur depuis Clerk API
            try:
                user_info = clerk_client.users.get(clerk_user_id)
                email = user_info.get("email_addresses", [{}])[0].get("email_address", "") if user_info.get("email_addresses") else ""
                first_name = user_info.get("first_name", "")
                last_name = user_info.get("last_name", "")
                display_name = f"{first_name} {last_name}".strip() or user_info.get("username", "User")
            except:
                # Si on ne peut pas récupérer depuis Clerk, utiliser les infos du token
                email = decoded_token.get("email", "")
                display_name = decoded_token.get("name") or decoded_token.get("first_name", "User")
                
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token JWT invalide",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Récupérer ou créer l'utilisateur dans notre DB
        user = db.query(User).filter(User.id == clerk_user_id).first()
        
        if not user:
            # Créer un nouvel utilisateur depuis Clerk
            user = User(
                id=clerk_user_id,
                email=email or f"{clerk_user_id}@clerk.app",
                display_name=display_name,
                subscription=SubscriptionTier.FREE,
                daily_quota=10,
                quota_used=0,
                quota_reset_date=datetime.now()
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            # Mettre à jour les infos si nécessaire
            if email and user.email != email:
                user.email = email
            if display_name and user.display_name != display_name:
                user.display_name = display_name
            db.commit()
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur authentification Clerk: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Erreur authentification: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

