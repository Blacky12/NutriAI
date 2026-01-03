package com.nutriai.app.data.api

import retrofit2.http.*

interface NutriApi {
    @GET("/")
    suspend fun getRoot(): RootResponse

    @GET("/health")
    suspend fun getHealth(): HealthResponse

    @POST("/api/v1/meals/analyze")
    suspend fun analyzeMeal(@Body request: MealAnalysisRequest): MealAnalysisResponse

    @GET("/api/v1/meals/")
    suspend fun getMeals(@Query("skip") skip: Int = 0, @Query("limit") limit: Int = 20): List<MealRead>

    @GET("/api/v1/meals/{mealId}")
    suspend fun getMeal(@Path("mealId") mealId: String): MealRead
}

data class RootResponse(val message: String)
data class HealthResponse(val status: String)

data class MealAnalysisRequest(val description: String)

data class MealAnalysisResponse(
    val meal_id: String,
    val description: String,
    val nutrition: NutritionData,
    val metadata: MealMetadata,
    val quota_remaining: Int
)

data class NutritionData(
    val calories: Double,
    val proteins: Double,
    val carbs: Double,
    val fats: Double,
    val fiber: Double,
    val suggestions: List<String>
)

data class MealMetadata(
    val model_used: String,
    val tokens_used: Int,
    val cost_usd: Double
)

data class MealRead(
    val id: String,
    val user_id: String,
    val description: String,
    val calories: Double,
    val proteins: Double,
    val carbs: Double,
    val fats: Double,
    val fiber: Double,
    val suggestions: List<String>,
    val created_at: String
)
