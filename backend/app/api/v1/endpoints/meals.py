from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import httpx
import json
import re
import uuid
from datetime import datetime

from ....core.database import get_db
from ....core.config import get_settings
from ....core.auth import get_current_user
from ....models.meal import Meal
from ....models.user import User, SubscriptionTier
from ....schemas.meal import MealAnalysisRequest, MealAnalysisResponse, NutritionData, MealMetadata, MealRead

router = APIRouter()
settings = get_settings()


@router.post("/analyze", response_model=MealAnalysisResponse)
async def analyze_meal(
    request: MealAnalysisRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Analyse un repas via OpenRouter"""
    
    # L'utilisateur est déjà récupéré depuis Clerk via get_current_user
    
    # Vérifier quota
    if user.has_reached_quota():
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Quota atteint"
        )
    
    # Prompt optimisé
    system_prompt = """Tu es un assistant nutritionnel. Retourne UNIQUEMENT un JSON valide :
{
  "calories": nombre,
  "proteins": nombre,
  "carbs": nombre,
  "fats": nombre,
  "fiber": nombre,
  "suggestions": ["suggestion 1", "suggestion 2"]
}"""
    
    # Appel OpenRouter
    if not settings.OPENROUTER_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OPENROUTER_API_KEY non configurée"
        )
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                },
                json={
                    "model": settings.OPENROUTER_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Repas : {request.description.strip()}"}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 500,
                }
            )
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPStatusError as e:
        print(f"❌ Erreur OpenRouter HTTP: {e.response.status_code} - {e.response.text}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Erreur API OpenRouter: {e.response.status_code}"
        )
    except Exception as e:
        print(f"❌ Erreur OpenRouter: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Erreur API: {str(e)}"
        )
    
    # Parser réponse
    try:
        ai_message = data["choices"][0]["message"]["content"]
        usage = data.get("usage", {})
    except (KeyError, IndexError) as e:
        print(f"❌ Erreur format réponse OpenRouter: {data}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Format de réponse invalide: {str(e)}"
        )
    
    try:
        json_match = re.search(r'\{[\s\S]*\}', ai_message)
        if not json_match:
            print(f"❌ Pas de JSON trouvé dans: {ai_message}")
            raise ValueError("JSON invalide dans la réponse")
        nutrition_json = json.loads(json_match.group(0))
    except json.JSONDecodeError as e:
        print(f"❌ Erreur parsing JSON: {ai_message}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur parsing JSON: {str(e)}"
        )
    except Exception as e:
        print(f"❌ Erreur parsing: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur parsing: {str(e)}"
        )
    
    # Calcul coût
    prompt_tokens = usage.get("prompt_tokens", 0)
    completion_tokens = usage.get("completion_tokens", 0)
    total_tokens = usage.get("total_tokens", prompt_tokens + completion_tokens)
    
    input_cost = (prompt_tokens / 1_000_000) * 0.5
    output_cost = (completion_tokens / 1_000_000) * 1.5
    total_cost = input_cost + output_cost
    
    # Sauvegarder
    try:
        meal_id = str(uuid.uuid4())
        meal = Meal(
            id=meal_id,
            user_id=user.id,
            description=request.description.strip(),
            calories=float(nutrition_json.get("calories", 0)),
            proteins=float(nutrition_json.get("proteins", 0)),
            carbs=float(nutrition_json.get("carbs", 0)),
            fats=float(nutrition_json.get("fats", 0)),
            fiber=float(nutrition_json.get("fiber", 0.0)),
            suggestions=nutrition_json.get("suggestions", []),
            model_used=settings.OPENROUTER_MODEL,
            tokens_used=total_tokens,
            cost_usd=round(total_cost, 6)
        )
        
        db.add(meal)
        user.quota_used += 1
        db.commit()
        db.refresh(meal)
    except Exception as e:
        print(f"❌ Erreur sauvegarde DB: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur sauvegarde: {str(e)}"
        )
    
    return MealAnalysisResponse(
        meal_id=meal_id,
        description=meal.description,
        nutrition=NutritionData(
            calories=meal.calories,
            proteins=meal.proteins,
            carbs=meal.carbs,
            fats=meal.fats,
            fiber=meal.fiber,
            suggestions=meal.suggestions
        ),
        metadata=MealMetadata(
            model_used=meal.model_used,
            tokens_used=meal.tokens_used,
            cost_usd=meal.cost_usd
        ),
        quota_remaining=user.daily_quota - user.quota_used if user.daily_quota != -1 else -1
    )


@router.get("/", response_model=List[MealRead])
async def get_meals(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 20
):
    """Récupère l'historique de l'utilisateur connecté"""
    try:
        meals = db.query(Meal)\
            .filter(Meal.user_id == user.id)\
            .order_by(Meal.created_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
        print(f"✅ Récupération historique: {len(meals)} repas trouvés pour user {user.id}")
        
        # Convertir les meals en MealRead avec created_at en string
        result = []
        for meal in meals:
            result.append(MealRead(
                id=meal.id,
                user_id=meal.user_id,
                description=meal.description,
                calories=meal.calories,
                proteins=meal.proteins,
                carbs=meal.carbs,
                fats=meal.fats,
                fiber=meal.fiber,
                suggestions=meal.suggestions,
                created_at=meal.created_at.isoformat() if meal.created_at else ""
            ))
        
        return result
    except Exception as e:
        print(f"❌ Erreur récupération historique: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur récupération historique: {str(e)}"
        )

