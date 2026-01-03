package com.nutriai.app.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SignUpScreen(
    onSignUpSuccess: () -> Unit,
    onBackClick: () -> Unit
) {
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var confirmPassword by remember { mutableStateOf("") }
    var isLoading by remember { mutableStateOf(false) }
    var errorMessage by remember { mutableStateOf<String?>(null) }
    val coroutineScope = rememberCoroutineScope()
    
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Inscription - NutriAI") },
                navigationIcon = {
                    IconButton(onClick = onBackClick) {
                        Text("←")
                    }
                }
            )
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
                text = "Créer un compte",
                style = MaterialTheme.typography.headlineMedium
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            OutlinedTextField(
                value = email,
                onValueChange = { email = it },
                label = { Text("Email") },
                modifier = Modifier.fillMaxWidth(),
                placeholder = { Text("votre@email.com") },
                singleLine = true
            )
            
            OutlinedTextField(
                value = password,
                onValueChange = { password = it },
                label = { Text("Mot de passe") },
                modifier = Modifier.fillMaxWidth(),
                visualTransformation = PasswordVisualTransformation(),
                singleLine = true
            )
            
            OutlinedTextField(
                value = confirmPassword,
                onValueChange = { confirmPassword = it },
                label = { Text("Confirmer le mot de passe") },
                modifier = Modifier.fillMaxWidth(),
                visualTransformation = PasswordVisualTransformation(),
                singleLine = true
            )
            
            errorMessage?.let { error ->
                Text(
                    text = error,
                    color = MaterialTheme.colorScheme.error,
                    style = MaterialTheme.typography.bodySmall
                )
            }
            
            Button(
                onClick = {
                    if (password != confirmPassword) {
                        errorMessage = "Les mots de passe ne correspondent pas"
                        return@Button
                    }
                    if (password.length < 8) {
                        errorMessage = "Le mot de passe doit contenir au moins 8 caractères"
                        return@Button
                    }
                    
                    isLoading = true
                    errorMessage = null
                    
                    // Appeler AuthManager pour créer le compte
                    coroutineScope.launch {
                        val result = com.nutriai.app.data.auth.AuthManager.signUp(email, password)
                        isLoading = false
                        
                        result.onSuccess { message ->
                            if (com.nutriai.app.data.auth.AuthManager.isAuthenticated.value) {
                                onSignUpSuccess()
                            } else {
                                errorMessage = message
                            }
                        }.onFailure { e ->
                            errorMessage = e.message ?: "Erreur lors de l'inscription"
                        }
                    }
                },
                modifier = Modifier.fillMaxWidth(),
                enabled = !isLoading && email.isNotBlank() && password.isNotBlank() && confirmPassword.isNotBlank()
            ) {
                if (isLoading) {
                    CircularProgressIndicator(
                        modifier = Modifier.size(20.dp),
                        color = MaterialTheme.colorScheme.onPrimary
                    )
                } else {
                    Text("S'inscrire")
                }
            }
            
            TextButton(onClick = onBackClick) {
                Text("Déjà un compte ? Se connecter")
            }
            
            Spacer(modifier = Modifier.weight(1f))
        }
    }
}

