from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from fastapi import Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel

from ....core.database import get_db
from ....core.admin_auth import create_admin_session, verify_admin_session, verify_admin_password
from ....core.config import get_settings
from ....models.meal import Meal
from ....models.user import User

router = APIRouter()
settings = get_settings()


class AdminLoginRequest(BaseModel):
    password: str


@router.post("/login")
async def admin_login(request: AdminLoginRequest, response: Response):
    """Connexion admin"""
    if verify_admin_password(request.password):
        session_token = create_admin_session()
        response.set_cookie(
            key="admin_session",
            value=session_token,
            httponly=True,
            secure=False,  # True en production avec HTTPS
            samesite="lax"
        )
        return {"message": "Connexion réussie", "redirect": "/admin"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Mot de passe incorrect"
        )


@router.get("/logout")
async def admin_logout(request: Request, response: Response):
    """Déconnexion admin"""
    from ....core.admin_auth import admin_sessions
    
    # Récupérer le token de session depuis les cookies
    admin_session = request.cookies.get("admin_session")
    
    # Supprimer la session de la liste
    if admin_session and admin_session in admin_sessions:
        admin_sessions.discard(admin_session)
    
    # Supprimer le cookie avec les mêmes paramètres que lors de la création
    response.delete_cookie(
        key="admin_session",
        httponly=True,
        samesite="lax",
        path="/"
    )
    
    return RedirectResponse(url="/admin", status_code=303)


def require_admin_auth(admin_session: Optional[str] = Cookie(None)) -> bool:
    """Dependency pour vérifier l'authentification admin"""
    if not verify_admin_session(admin_session):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentification admin requise"
        )
    return True


@router.get("/stats")
async def get_admin_stats(
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin_auth)
):
    """Statistiques pour le dashboard admin"""
    try:
        # Total repas analysés
        total_meals = db.query(func.count(Meal.id)).scalar() or 0
        
        # Total utilisateurs
        total_users = db.query(func.count(User.id)).scalar() or 0
        
        # Coût total
        total_cost = db.query(func.sum(Meal.cost_usd)).scalar() or 0.0
        
        # Tokens total
        total_tokens = db.query(func.sum(Meal.tokens_used)).scalar() or 0
        
        # Coût par jour (7 derniers jours)
        seven_days_ago = datetime.now() - timedelta(days=7)
        daily_costs = db.query(
            func.date(Meal.created_at).label('date'),
            func.sum(Meal.cost_usd).label('cost')
        ).filter(
            Meal.created_at >= seven_days_ago
        ).group_by(
            func.date(Meal.created_at)
        ).all()
        
        daily_stats = [
            {
                "date": str(date),
                "cost": float(cost) if cost else 0.0
            }
            for date, cost in daily_costs
        ]
        
        # Repas par jour (7 derniers jours)
        daily_meals = db.query(
            func.date(Meal.created_at).label('date'),
            func.count(Meal.id).label('count')
        ).filter(
            Meal.created_at >= seven_days_ago
        ).group_by(
            func.date(Meal.created_at)
        ).all()
        
        daily_meals_stats = [
            {
                "date": str(date),
                "count": count
            }
            for date, count in daily_meals
        ]
        
        # Top modèles utilisés
        model_usage = db.query(
            Meal.model_used,
            func.count(Meal.id).label('count'),
            func.sum(Meal.cost_usd).label('cost')
        ).group_by(
            Meal.model_used
        ).all()
        
        model_stats = [
            {
                "model": model,
                "count": count,
                "cost": float(cost) if cost else 0.0
            }
            for model, count, cost in model_usage
        ]
        
        return {
            "summary": {
                "total_meals": total_meals,
                "total_users": total_users,
                "total_cost_usd": round(float(total_cost), 6),
                "total_tokens": total_tokens,
                "avg_cost_per_meal": round(float(total_cost) / total_meals, 6) if total_meals > 0 else 0.0
            },
            "daily_costs": daily_stats,
            "daily_meals": daily_meals_stats,
            "model_usage": model_stats
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur récupération stats: {str(e)}"
        )


