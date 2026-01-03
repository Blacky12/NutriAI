package com.nutriai.app.data.api

import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object RetrofitClient {
    // Production (Render)
    private const val BASE_URL = "https://nutriai-backend-htic.onrender.com/"
    
    // Développement local (décommenter pour tester en local)
    // private const val BASE_URL = "http://10.0.2.2:8000/"

    val api: NutriApi by lazy {
        // Créer un interceptor pour le logging (optionnel, pour debug)
        val loggingInterceptor = HttpLoggingInterceptor().apply {
            level = HttpLoggingInterceptor.Level.BODY
        }
        
        // Créer le client OkHttp avec l'interceptor d'authentification
        val client = OkHttpClient.Builder()
            .addInterceptor(AuthInterceptor())
            .addInterceptor(loggingInterceptor)
            .build()
        
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(client)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(NutriApi::class.java)
    }
}
