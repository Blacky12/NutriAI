package com.nutriai.app.data.api

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object ClerkClient {
    // URL de l'API Clerk
    private const val CLERK_API_BASE_URL = "https://api.clerk.com/"
    
    val api: ClerkApi by lazy {
        Retrofit.Builder()
            .baseUrl(CLERK_API_BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ClerkApi::class.java)
    }
}

