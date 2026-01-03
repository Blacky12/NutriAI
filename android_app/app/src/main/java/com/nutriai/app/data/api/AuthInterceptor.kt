package com.nutriai.app.data.api

import com.nutriai.app.data.auth.AuthManager
import okhttp3.Interceptor
import okhttp3.Response

/**
 * Interceptor Retrofit pour ajouter le token Clerk dans les headers
 */
class AuthInterceptor : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val originalRequest = chain.request()
        
        // Récupérer le token depuis AuthManager
        val token = AuthManager.getToken()
        
        // Si un token existe, l'ajouter dans le header Authorization
        val newRequest = if (token != null) {
            originalRequest.newBuilder()
                .header("Authorization", "Bearer $token")
                .build()
        } else {
            originalRequest
        }
        
        return chain.proceed(newRequest)
    }
}

