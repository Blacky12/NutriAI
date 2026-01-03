package com.nutriai.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.collectAsState
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.nutriai.app.data.auth.AuthManager
import com.nutriai.app.ui.screens.MealInputScreen
import com.nutriai.app.ui.screens.MealResultScreen
import com.nutriai.app.ui.screens.MealHistoryScreen
import com.nutriai.app.ui.screens.LoginScreen
import com.nutriai.app.ui.screens.SignUpScreen
import com.nutriai.app.ui.theme.NutriAITheme
import com.nutriai.app.viewmodel.MealViewModel
import com.nutriai.app.viewmodel.HomeViewModel

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // Initialiser AuthManager
        AuthManager.initialize(this)
        
        enableEdgeToEdge()
        setContent {
            NutriAITheme {
                NutriAIApp()
            }
        }
    }
}

@Composable
fun NutriAIApp() {
    val navController = rememberNavController()
    val mealViewModel: MealViewModel = viewModel()
    val isAuthenticated by AuthManager.isAuthenticated.collectAsState()

    NavHost(
        navController = navController,
        startDestination = if (isAuthenticated) "home" else "login"
    ) {
        composable("login") {
            LoginScreen(
                onLoginSuccess = { navController.navigate("home") { popUpTo("login") { inclusive = true } } },
                onSignUpClick = { navController.navigate("signup") }
            )
        }
        composable("signup") {
            SignUpScreen(
                onSignUpSuccess = { navController.navigate("home") { popUpTo("signup") { inclusive = true } } },
                onBackClick = { navController.popBackStack() }
            )
        }
        composable("home") {
            // Réinitialiser l'état si nécessaire
            LaunchedEffect(Unit) {
                mealViewModel.clearError()
            }
            
            HomeScreen(
                onAnalyzeClick = { navController.navigate("input") },
                onHistoryClick = { navController.navigate("history") }
            )
        }
        composable("input") {
            MealInputScreen(
                viewModel = mealViewModel,
                onResult = { navController.navigate("result") }
            )
        }
        composable("result") {
            val state = mealViewModel.state.value
            val result = state.result
            
            LaunchedEffect(Unit) {
                if (result == null) {
                    navController.popBackStack()
                }
            }
            
            if (result != null) {
                MealResultScreen(
                    result = result,
                    onBack = { 
                        mealViewModel.clearResult()
                        navController.navigate("home") {
                            popUpTo("home") { inclusive = false }
                        }
                    }
                )
            }
        }
        composable("history") {
            MealHistoryScreen(
                viewModel = mealViewModel,
                onBack = { navController.popBackStack() }
            )
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    onAnalyzeClick: () -> Unit,
    onHistoryClick: () -> Unit,
    homeViewModel: HomeViewModel = viewModel()
) {
    Scaffold(
        topBar = {
            TopAppBar(title = { Text("NutriAI Assistant") })
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Spacer(modifier = Modifier.weight(1f))
            
            Text(
                text = "🥗 NutriAI",
                style = MaterialTheme.typography.displayMedium
            )
            
            Text(
                text = "Votre assistant nutritionnel intelligent",
                style = MaterialTheme.typography.bodyLarge
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            Card(
                colors = CardDefaults.cardColors(
                    containerColor = if (homeViewModel.apiStatus.value.contains("OK")) {
                        MaterialTheme.colorScheme.primaryContainer
                    } else {
                        MaterialTheme.colorScheme.errorContainer
                    }
                ),
                modifier = Modifier.fillMaxWidth()
            ) {
                Text(
                    text = homeViewModel.apiStatus.value,
                    modifier = Modifier.padding(12.dp),
                    style = MaterialTheme.typography.bodySmall
                )
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            
            Button(
                onClick = onAnalyzeClick,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Analyser un repas")
            }
            
            OutlinedButton(
                onClick = onHistoryClick,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Historique")
            }
            
            TextButton(
                onClick = {
                    AuthManager.signOut()
                    // Navigation sera gérée automatiquement par le NavHost
                }
            ) {
                Text("Déconnexion")
            }
            
            Spacer(modifier = Modifier.weight(1f))
        }
    }
}
