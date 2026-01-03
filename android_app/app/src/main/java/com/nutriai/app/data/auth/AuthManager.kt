package com.nutriai.app.data.auth

import android.content.Context
import android.content.SharedPreferences
import com.nutriai.app.data.api.NutriApi
import com.nutriai.app.data.api.RetrofitClient
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

/**
 * Gestionnaire d'authentification pour Clerk
 * Utilise l'API backend pour gérer l'inscription et la connexion
 */
object AuthManager {
    private val api: NutriApi = RetrofitClient.api
    private const val PREFS_NAME = "nutriai_auth"
    private const val KEY_TOKEN = "clerk_token"
    private const val KEY_USER_ID = "user_id"
    private const val KEY_EMAIL = "email"
    
    private val _isAuthenticated = MutableStateFlow<Boolean>(false)
    val isAuthenticated: StateFlow<Boolean> = _isAuthenticated.asStateFlow()
    
    private val _currentToken = MutableStateFlow<String?>(null)
    val currentToken: StateFlow<String?> = _currentToken.asStateFlow()
    
    private lateinit var prefs: SharedPreferences
    
    fun initialize(context: Context) {
        prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        
        // Vérifier si un token existe
        val savedToken = prefs.getString(KEY_TOKEN, null)
        if (savedToken != null) {
            _currentToken.value = savedToken
            _isAuthenticated.value = true
        } else {
            _isAuthenticated.value = false
        }
    }
    
    fun setToken(token: String, userId: String? = null, email: String? = null) {
        _currentToken.value = token
        _isAuthenticated.value = true
        prefs.edit().apply {
            putString(KEY_TOKEN, token)
            if (userId != null) putString(KEY_USER_ID, userId)
            if (email != null) putString(KEY_EMAIL, email)
            apply()
        }
    }
    
    fun signOut() {
        _currentToken.value = null
        _isAuthenticated.value = false
        prefs.edit().clear().apply()
    }
    
    fun getToken(): String? {
        return _currentToken.value ?: prefs.getString(KEY_TOKEN, null)
    }
    
    fun getUserId(): String? {
        return prefs.getString(KEY_USER_ID, null)
    }
    
    fun getEmail(): String? {
        return prefs.getString(KEY_EMAIL, null)
    }
    
    suspend fun signUp(email: String, password: String, firstName: String? = null, lastName: String? = null): Result<String> {
        return try {
            val response = api.signUp(
                com.nutriai.app.data.api.SignUpRequest(
                    email = email,
                    password = password,
                    first_name = firstName,
                    last_name = lastName
                )
            )
            
            if (response.token.isNotEmpty()) {
                setToken(response.token, response.user_id, response.email)
                Result.success(response.message)
            } else {
                // Compte créé mais pas de token, demander connexion
                Result.success(response.message)
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun signIn(email: String, password: String): Result<String> {
        return try {
            val response = api.signIn(
                com.nutriai.app.data.api.SignInRequest(
                    email = email,
                    password = password
                )
            )
            
            setToken(response.token, response.user_id, response.email)
            Result.success(response.message)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
