package com.nutriai.app.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.nutriai.app.viewmodel.MealViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MealInputScreen(
    onResult: () -> Unit,
    viewModel: MealViewModel
) {
    var description by remember { mutableStateOf("") }
    val state = viewModel.state.value

    // Navigation automatique quand le résultat arrive
    LaunchedEffect(state.result) {
        state.result?.let {
            onResult()
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(title = { Text("Analyser un repas") })
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
            Text(
                text = "Décrivez votre repas",
                style = MaterialTheme.typography.headlineMedium
            )

            OutlinedTextField(
                value = description,
                onValueChange = { description = it },
                modifier = Modifier.fillMaxWidth(),
                label = { Text("Ex: Poulet grillé avec riz et brocolis") },
                placeholder = { Text("Entrez la description...") },
                minLines = 3,
                maxLines = 5,
                enabled = !state.isLoading
            )

            if (state.error != null) {
                Card(
                    colors = CardDefaults.cardColors(
                        containerColor = MaterialTheme.colorScheme.errorContainer
                    ),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text(
                            text = "ERREUR",
                            style = MaterialTheme.typography.titleMedium,
                            color = MaterialTheme.colorScheme.onErrorContainer
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            text = state.error ?: "",
                            color = MaterialTheme.colorScheme.onErrorContainer
                        )
                    }
                }
            }

            Button(
                onClick = { viewModel.analyzeMeal(description) },
                enabled = !state.isLoading && description.isNotBlank(),
                modifier = Modifier.fillMaxWidth()
            ) {
                if (state.isLoading) {
                    CircularProgressIndicator(
                        modifier = Modifier.size(20.dp),
                        color = MaterialTheme.colorScheme.onPrimary
                    )
                } else {
                    Text("Analyser")
                }
            }

            Spacer(modifier = Modifier.weight(1f))
        }
    }
}
