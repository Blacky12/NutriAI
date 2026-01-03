from fastapi import Depends, HTTPException, status, Header
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime
from jose import jwt, JWTError
import httpx

from .config import get_settings
from .database import get_db
from ..models.user import User, SubscriptionTier

settings = get_settings()


async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency pour obtenir l'utilisateur actuel depuis le token Clerk
    Si Clerk n'est pas configuré, utilise un utilisateur temporaire pour le développement
    """
    # Mode développement : si Clerk n'est pas configuré, utiliser un utilisateur temporaire
    if not settings.CLERK_SECRET_KEY:
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
        clerk_user_id = None
        email = ""
        display_name = "User"
        
        # Pour MVP : accepter les tokens simplifiés (clerk_{user_id})
        if token.startswith("clerk_"):
            # Token simplifié pour MVP - extraire l'ID utilisateur directement
            clerk_user_id = token.replace("clerk_", "")
            print(f"✅ Token simplifié détecté, user_id: {clerk_user_id}")
            
            # Pour les tokens simplifiés, récupérer les infos depuis la DB
            # (l'utilisateur a déjà été créé lors de l'inscription)
            existing_user = db.query(User).filter(User.id == clerk_user_id).first()
            if existing_user:
                email = existing_user.email
                display_name = existing_user.display_name
        else:
            # Token JWT réel de Clerk
            try:
                decoded_token = jwt.get_unverified_claims(token)
                clerk_user_id = decoded_token.get("sub")
                
                if not clerk_user_id:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Token invalide: ID utilisateur manquant",
                    )
                
                # Récupérer les infos complètes de l'utilisateur depuis Clerk API REST
                try:
                    async with httpx.AsyncClient(timeout=10.0) as client:
                        headers = {"Authorization": f"Bearer {settings.CLERK_SECRET_KEY}"}
                        response = await client.get(
                            f"https://api.clerk.com/v1/users/{clerk_user_id}",
                            headers=headers
                        )
                        if response.status_code == 200:
                            user_info = response.json()
                            email = user_info.get("email_addresses", [{}])[0].get("email_address", "") if user_info.get("email_addresses") else ""
                            first_name = user_info.get("first_name", "")
                            last_name = user_info.get("last_name", "")
                            display_name = f"{first_name} {last_name}".strip() or user_info.get("username", "User")
                        else:
                            # Si on ne peut pas récupérer depuis Clerk, utiliser les infos du token
                            email = decoded_token.get("email", "")
                            display_name = decoded_token.get("name") or decoded_token.get("first_name", "User")
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
        
        if not clerk_user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalide: impossible d'extraire l'ID utilisateur",
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

