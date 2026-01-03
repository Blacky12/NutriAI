package com.nutriai.app.viewmodel

import androidx.compose.runtime.State
import androidx.compose.runtime.mutableStateOf
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.nutriai.app.data.api.MealAnalysisResponse
import com.nutriai.app.data.api.MealRead
import com.nutriai.app.data.api.RetrofitClient
import kotlinx.coroutines.launch
import retrofit2.HttpException

data class MealUiState(
    val isLoading: Boolean = false,
    val error: String? = null,
    val result: MealAnalysisResponse? = null,
    val meals: List<MealRead> = emptyList()
)

class MealViewModel : ViewModel() {
    private val _state = mutableStateOf(MealUiState())
    val state: State<MealUiState> = _state

    fun analyzeMeal(description: String) {
        if (description.isBlank()) {
            _state.value = _state.value.copy(error = "Veuillez décrire votre repas")
            return
        }

        _state.value = _state.value.copy(isLoading = true, error = null)

        viewModelScope.launch {
            try {
                val response = RetrofitClient.api.analyzeMeal(
                    com.nutriai.app.data.api.MealAnalysisRequest(description)
                )
                _state.value = _state.value.copy(
                    isLoading = false,
                    result = response,
                    error = null
                )
            } catch (e: java.net.ConnectException) {
                _state.value = _state.value.copy(
                    isLoading = false,
                    error = "Connexion refusée. Vérifiez que le backend tourne sur http://localhost:8000"
                )
            } catch (e: java.net.UnknownHostException) {
                _state.value = _state.value.copy(
                    isLoading = false,
                    error = "Host inconnu. Vérifiez l'URL dans RetrofitClient.kt"
                )
            } catch (e: HttpException) {
                _state.value = _state.value.copy(
                    isLoading = false,
                    error = "Erreur HTTP ${e.code()}: ${e.message}"
                )
            } catch (e: Exception) {
                _state.value = _state.value.copy(
                    isLoading = false,
                    error = "Erreur: ${e.javaClass.simpleName} - ${e.message}"
                )
            }
        }
    }

    fun loadMeals() {
        _state.value = _state.value.copy(isLoading = true, error = null)

        viewModelScope.launch {
            try {
                val meals = RetrofitClient.api.getMeals()
                _state.value = _state.value.copy(
                    isLoading = false,
                    meals = meals,
                    error = null
                )
            } catch (e: java.net.ConnectException) {
                _state.value = _state.value.copy(
                    isLoading = false,
                    error = "Connexion refusee. Verifiez que le backend tourne."
                )
            } catch (e: java.net.UnknownHostException) {
                _state.value = _state.value.copy(
                    isLoading = false,
                    error = "Host inconnu. Verifiez l'URL dans RetrofitClient.kt"
                )
            } catch (e: HttpException) {
                _state.value = _state.value.copy(
                    isLoading = false,
                    error = "Erreur HTTP ${e.code()}: ${e.message}"
                )
            } catch (e: Exception) {
                _state.value = _state.value.copy(
                    isLoading = false,
                    error = "Erreur: ${e.javaClass.simpleName} - ${e.message}"
                )
            }
        }
    }

    fun clearError() {
        _state.value = _state.value.copy(error = null)
    }

    fun clearResult() {
        _state.value = _state.value.copy(result = null)
    }
}
