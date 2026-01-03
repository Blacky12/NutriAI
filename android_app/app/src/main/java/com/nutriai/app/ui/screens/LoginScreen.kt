package com.nutriai.app.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import com.nutriai.app.data.auth.AuthManager
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LoginScreen(
    onLoginSuccess: () -> Unit,
    onSignUpClick: () -> Unit
) {
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var isLoading by remember { mutableStateOf(false) }
    var errorMessage by remember { mutableStateOf<String?>(null) }
    val coroutineScope = rememberCoroutineScope()
    
    // Pour MVP : Mode simplifié avec token manuel
    var tokenInput by remember { mutableStateOf("") }
    var useTokenMode by remember { mutableStateOf(false) }
    
    Scaffold(
        topBar = {
            TopAppBar(title = { Text("Connexion - NutriAI") })
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
                text = "Connectez-vous pour continuer",
                style = MaterialTheme.typography.bodyLarge
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            // Toggle entre mode email/password et mode token
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.Center
            ) {
                TextButton(onClick = { useTokenMode = false }) {
                    Text(if (useTokenMode) "Mode Email" else "✓ Mode Email")
                }
                TextButton(onClick = { useTokenMode = true }) {
                    Text(if (!useTokenMode) "Mode Token" else "✓ Mode Token")
                }
            }
            
            if (useTokenMode) {
                // Mode Token (pour MVP/test)
                OutlinedTextField(
                    value = tokenInput,
                    onValueChange = { tokenInput = it },
                    label = { Text("Token Clerk") },
                    modifier = Modifier.fillMaxWidth(),
                    placeholder = { Text("Collez votre token Clerk ici") },
                    singleLine = true
                )
                
                Text(
                    text = "Pour obtenir un token : Connectez-vous sur clerk.com et copiez votre token de session",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            } else {
                // Mode Email/Password (pour production)
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
            }
            
            errorMessage?.let { error ->
                Text(
                    text = error,
                    color = MaterialTheme.colorScheme.error,
                    style = MaterialTheme.typography.bodySmall
                )
            }
            
            Button(
                onClick = {
                    isLoading = true
                    errorMessage = null
                    
                    if (useTokenMode) {
                        // Mode Token : utiliser directement le token
                        if (tokenInput.isNotBlank()) {
                            AuthManager.setToken(tokenInput)
                            onLoginSuccess()
                        } else {
                            errorMessage = "Veuillez entrer un token"
                            isLoading = false
                        }
                    } else {
                        // Mode Email/Password : Utiliser l'API backend
                        coroutineScope.launch {
                            val result = AuthManager.signIn(email, password)
                            isLoading = false
                            
                            result.onSuccess {
                                onLoginSuccess()
                            }.onFailure { e ->
                                errorMessage = e.message ?: "Erreur lors de la connexion"
                            }
                        }
                    }
                },
                modifier = Modifier.fillMaxWidth(),
                enabled = !isLoading && (
                    (useTokenMode && tokenInput.isNotBlank()) ||
                    (!useTokenMode && email.isNotBlank() && password.isNotBlank())
                )
            ) {
                if (isLoading) {
                    CircularProgressIndicator(
                        modifier = Modifier.size(20.dp),
                        color = MaterialTheme.colorScheme.onPrimary
                    )
                } else {
                    Text("Se connecter")
                }
            }
            
            TextButton(onClick = onSignUpClick) {
                Text("Pas encore de compte ? S'inscrire")
            }
            
            Spacer(modifier = Modifier.weight(1f))
        }
    }
}

