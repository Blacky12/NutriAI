package com.nutriai.app.viewmodel

import androidx.compose.runtime.State
import androidx.compose.runtime.mutableStateOf
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.nutriai.app.data.api.RetrofitClient
import kotlinx.coroutines.launch

class HomeViewModel : ViewModel() {
    private val _apiStatus = mutableStateOf("Checking connection...")
    val apiStatus: State<String> = _apiStatus

    init {
        checkHealth()
    }

    private fun checkHealth() {
        viewModelScope.launch {
            try {
                val response = RetrofitClient.api.getHealth()
                _apiStatus.value = "OK - Backend Status: ${response.status}"
            } catch (e: java.net.ConnectException) {
                _apiStatus.value = "ERREUR - Connexion refusee\nVerifiez que le backend tourne sur http://localhost:8000"
            } catch (e: java.net.UnknownHostException) {
                _apiStatus.value = "ERREUR - Host inconnu\nVerifiez l'URL dans RetrofitClient.kt"
            } catch (e: Exception) {
                _apiStatus.value = "ERREUR: ${e.javaClass.simpleName}\n${e.message}"
            }
        }
    }
}
