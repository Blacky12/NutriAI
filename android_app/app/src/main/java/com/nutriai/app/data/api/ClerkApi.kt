package com.nutriai.app.data.api

import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.Header
import retrofit2.http.POST

/**
 * Interface Retrofit pour l'API Clerk
 * Utilise l'API REST publique de Clerk
 */
interface ClerkApi {
    
    data class SignUpRequest(
        val email_address: String,
        val password: String,
        val first_name: String? = null,
        val last_name: String? = null
    )
    
    data class SignInRequest(
        val identifier: String, // email ou username
        val password: String
    )
    
    data class ClerkResponse(
        val id: String? = null,
        val email_addresses: List<EmailAddress>? = null,
        val first_name: String? = null,
        val last_name: String? = null,
        val response: SessionResponse? = null
    )
    
    data class EmailAddress(
        val email_address: String,
        val id: String
    )
    
    data class SessionResponse(
        val id: String,
        val user_id: String,
        val last_active_at: Long? = null
    )
    
    /**
     * Créer un compte utilisateur
     * POST https://api.clerk.com/v1/sign_ups
     */
    @POST("v1/sign_ups")
    suspend fun signUp(
        @Header("Authorization") apiKey: String,
        @Body request: SignUpRequest
    ): Response<ClerkResponse>
    
    /**
     * Se connecter
     * POST https://api.clerk.com/v1/sign_ins
     */
    @POST("v1/sign_ins")
    suspend fun signIn(
        @Header("Authorization") apiKey: String,
        @Body request: SignInRequest
    ): Response<ClerkResponse>
}

