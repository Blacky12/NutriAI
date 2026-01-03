from pydantic import BaseModel, Field


class MealAnalysisRequest(BaseModel):
    description: str = Field(..., min_length=5, max_length=500)


class NutritionData(BaseModel):
    calories: float = Field(..., ge=0)
    proteins: float = Field(..., ge=0)
    carbs: float = Field(..., ge=0)
    fats: float = Field(..., ge=0)
    fiber: float = Field(default=0.0, ge=0)
    suggestions: list[str] = Field(default_factory=list)


class MealMetadata(BaseModel):
    model_used: str
    tokens_used: int
    cost_usd: float


class MealAnalysisResponse(BaseModel):
    meal_id: str
    description: str
    nutrition: NutritionData
    metadata: MealMetadata
    quota_remaining: int


class MealRead(BaseModel):
    id: str
    user_id: str
    description: str
    calories: float
    proteins: float
    carbs: float
    fats: float
    fiber: float
    suggestions: list[str]
    created_at: str

    class Config:
        from_attributes = True

