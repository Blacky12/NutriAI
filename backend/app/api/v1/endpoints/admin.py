from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, List
from datetime import datetime, timedelta

from ....core.database import get_db
from ....models.meal import Meal
from ....models.user import User

router = APIRouter()


@router.get("/stats")
async def get_admin_stats(db: Session = Depends(get_db)):
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


