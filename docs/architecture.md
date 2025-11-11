# 🏗️ Architecture Technique - NutriAI Assistant

## Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT (Flutter)                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  UI Layer (Screens & Widgets)                         │  │
│  │  • AuthScreen, HomeScreen, AnalysisScreen...          │  │
│  └───────────────────────────────────────────────────────┘  │
│                           ↕                                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  State Management (Provider)                          │  │
│  │  • AuthProvider, MealProvider, AdminProvider          │  │
│  └───────────────────────────────────────────────────────┘  │
│                           ↕                                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Services Layer                                       │  │
│  │  • AuthService, DatabaseService, AIService            │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           ↕ HTTPS
┌─────────────────────────────────────────────────────────────┐
│                  FIREBASE BACKEND                           │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │  Firebase    │  │  Cloud       │  │  Cloud          │   │
│  │  Auth        │  │  Firestore   │  │  Functions      │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
│                                              ↕               │
└──────────────────────────────────────────────┼───────────────┘
                                               ↕ HTTPS/API Key
┌─────────────────────────────────────────────────────────────┐
│                    OPENROUTER API                           │
│  • Endpoint: api.openrouter.ai/api/v1/chat/completions     │
│  • Models: GPT-4, Claude 3, Llama 3.1, Mistral...          │
└─────────────────────────────────────────────────────────────┘
```

---

## Structure Flutter (Clean Architecture)

```
lib/
├── main.dart                    # Entry point
│
├── app/                         # App-level configuration
│   ├── app.dart                # MaterialApp config
│   ├── routes/                 # Navigation
│   │   └── app_router.dart
│   └── theme/                  # UI Theme
│       ├── app_colors.dart
│       └── app_theme.dart
│
├── core/                        # Core utilities
│   ├── constants/
│   │   ├── api_constants.dart
│   │   └── app_constants.dart
│   ├── utils/
│   │   ├── validators.dart
│   │   └── formatters.dart
│   └── services/               # Business services
│       ├── auth_service.dart
│       ├── database_service.dart
│       ├── ai_service.dart
│       └── storage_service.dart
│
├── models/                      # Data models
│   ├── user_model.dart
│   ├── meal_model.dart
│   ├── nutrition_model.dart
│   └── analysis_result_model.dart
│
├── providers/                   # State management
│   ├── auth_provider.dart
│   ├── meal_provider.dart
│   ├── user_provider.dart
│   └── admin_provider.dart
│
├── screens/                     # UI Screens
│   ├── auth/
│   │   ├── login_screen.dart
│   │   ├── register_screen.dart
│   │   └── forgot_password_screen.dart
│   ├── home/
│   │   └── home_screen.dart
│   ├── meal/
│   │   ├── meal_input_screen.dart
│   │   ├── meal_result_screen.dart
│   │   └── meal_history_screen.dart
│   ├── profile/
│   │   └── profile_screen.dart
│   └── admin/
│       └── dashboard_screen.dart
│
└── widgets/                     # Reusable widgets
    ├── common/
    │   ├── custom_button.dart
    │   ├── custom_text_field.dart
    │   └── loading_indicator.dart
    └── meal/
        ├── nutrition_card.dart
        └── suggestion_card.dart
```

---

## Base de données Firestore

### Collections

#### 1. **users**
```
users/
└── {userId}
    ├── email: string
    ├── displayName: string
    ├── createdAt: timestamp
    ├── lastLoginAt: timestamp
    ├── subscription: "free" | "pro" | "premium"
    ├── dailyQuota: number
    ├── quotaUsed: number
    └── quotaResetDate: timestamp
```

#### 2. **meals**
```
meals/
└── {mealId}
    ├── userId: string (indexed)
    ├── description: string
    ├── timestamp: timestamp (indexed)
    ├── analysis: {
    │   ├── calories: number
    │   ├── proteins: number
    │   ├── carbs: number
    │   ├── fats: number
    │   ├── fiber: number
    │   ├── suggestions: string[]
    │   └── detailedAnalysis: string
    │ }
    ├── metadata: {
    │   ├── modelUsed: string
    │   ├── tokensUsed: number
    │   ├── costUSD: number
    │   └── responseTime: number
    │ }
    └── deleted: boolean (soft delete)
```

#### 3. **admin_metrics** (pour le dashboard)
```
admin_metrics/
└── {date}  # Format: YYYY-MM-DD
    ├── date: timestamp
    ├── totalCosts: number
    ├── totalRequests: number
    ├── totalTokens: number
    ├── uniqueUsers: number
    ├── modelBreakdown: {
    │   └── {modelName}: {
    │       ├── requests: number
    │       ├── tokens: number
    │       └── cost: number
    │   }
    │ }
    └── averageResponseTime: number
```

#### 4. **api_calls** (logs détaillés)
```
api_calls/
└── {callId}
    ├── timestamp: timestamp
    ├── userId: string
    ├── modelUsed: string
    ├── promptTokens: number
    ├── completionTokens: number
    ├── totalTokens: number
    ├── costUSD: number
    ├── responseTime: number
    ├── success: boolean
    └── errorMessage: string (if failed)
```

---

## Firebase Cloud Functions

### Functions à créer

```javascript
// functions/index.js

/**
 * Fonction 1: Analyser un repas via OpenRouter
 * Endpoint: analyzemeal
 * Méthode: POST
 * Auth: Required
 */
exports.analyzeMeal = functions.https.onCall(async (data, context) => {
  // 1. Vérifier l'authentification
  // 2. Vérifier le quota utilisateur
  // 3. Appeler OpenRouter API
  // 4. Sauvegarder résultat dans Firestore
  // 5. Mettre à jour les métriques admin
  // 6. Retourner le résultat
});

/**
 * Fonction 2: Obtenir les statistiques admin
 * Endpoint: getAdminStats
 * Méthode: GET
 * Auth: Admin only
 */
exports.getAdminStats = functions.https.onCall(async (data, context) => {
  // 1. Vérifier droits admin
  // 2. Récupérer métriques depuis Firestore
  // 3. Calculer agrégations
  // 4. Retourner dashboard data
});

/**
 * Fonction 3: Reset quotas quotidiens (scheduled)
 * Trigger: Chaque jour à minuit UTC
 */
exports.resetDailyQuotas = functions.pubsub
  .schedule('0 0 * * *')
  .onRun(async (context) => {
    // Reset quotaUsed pour tous les users
  });

/**
 * Fonction 4: Agrégation métriques quotidiennes (scheduled)
 * Trigger: Chaque jour à 23:55 UTC
 */
exports.aggregateDailyMetrics = functions.pubsub
  .schedule('55 23 * * *')
  .onRun(async (context) => {
    // Calculer et sauvegarder métriques du jour
  });
```

---

## Flux de données - Analyse de repas

```
┌─────────────────────────────────────────────────────────┐
│  1. User entre description du repas                     │
│     "Poulet grillé avec riz et brocolis"                │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  2. MealProvider.analyzeMeal()                          │
│     • Validation input                                  │
│     • Affichage loading                                 │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  3. AIService.analyzeMeal()                             │
│     • Appelle Cloud Function "analyzeM eal"             │
│     • Passe description + userId                        │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  4. Cloud Function (analyzeM eal)                       │
│     • Vérifie quota user                                │
│     • Construit prompt optimisé                         │
│     • Appelle OpenRouter API                            │
│     • Parse réponse JSON                                │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  5. OpenRouter API                                      │
│     • Traite avec modèle IA sélectionné                 │
│     • Retourne analyse nutritionnelle                   │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  6. Cloud Function (suite)                              │
│     • Sauvegarde dans Firestore (meals)                 │
│     • Met à jour métriques (admin_metrics)              │
│     • Log appel API (api_calls)                         │
│     • Incrémente quota user                             │
│     • Retourne résultat au client                       │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  7. Flutter App                                         │
│     • MealProvider met à jour le state                  │
│     • Navigation vers ResultScreen                      │
│     • Affichage analyse + suggestions                   │
└─────────────────────────────────────────────────────────┘
```

---

## Sécurité

### Règles Firestore (firestore.rules)

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    // Helper functions
    function isAuthenticated() {
      return request.auth != null;
    }
    
    function isOwner(userId) {
      return isAuthenticated() && request.auth.uid == userId;
    }
    
    function isAdmin() {
      return isAuthenticated() && 
             get(/databases/$(database)/documents/users/$(request.auth.uid))
             .data.role == 'admin';
    }
    
    // Users collection
    match /users/{userId} {
      allow read: if isOwner(userId);
      allow create: if isAuthenticated();
      allow update: if isOwner(userId);
      allow delete: if isOwner(userId);
    }
    
    // Meals collection
    match /meals/{mealId} {
      allow read: if isAuthenticated() && 
                     resource.data.userId == request.auth.uid;
      allow create: if isAuthenticated();
      allow update: if isAuthenticated() && 
                       resource.data.userId == request.auth.uid;
      allow delete: if isAuthenticated() && 
                       resource.data.userId == request.auth.uid;
    }
    
    // Admin metrics (read-only for admin)
    match /admin_metrics/{document=**} {
      allow read: if isAdmin();
      allow write: if false; // Only Cloud Functions can write
    }
    
    // API calls logs (read-only for admin)
    match /api_calls/{document=**} {
      allow read: if isAdmin();
      allow write: if false; // Only Cloud Functions can write
    }
  }
}
```

### Variables d'environnement (à ne JAMAIS commit)

```bash
# .env (local development)
OPENROUTER_API_KEY=your_openrouter_key_here
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_API_KEY=your_firebase_api_key

# GitHub Secrets (pour CI/CD)
OPENROUTER_API_KEY
FIREBASE_TOKEN
```

---

## Déploiement

### 1. Flutter Web → Firebase Hosting

```yaml
# .github/workflows/deploy-web.yml
name: Deploy Web
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: subosito/flutter-action@v2
      - run: flutter pub get
      - run: flutter build web --release
      - uses: FirebaseExtended/action-hosting-deploy@v0
        with:
          repoToken: '${{ secrets.GITHUB_TOKEN }}'
          firebaseServiceAccount: '${{ secrets.FIREBASE_TOKEN }}'
          projectId: your-project-id
```

### 2. Flutter Android → Firebase App Distribution

```yaml
# .github/workflows/deploy-android.yml
name: Deploy Android
on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: subosito/flutter-action@v2
      - run: flutter pub get
      - run: flutter build apk --release
      - uses: wzieba/Firebase-Distribution-Github-Action@v1
        with:
          appId: ${{ secrets.FIREBASE_APP_ID }}
          token: ${{ secrets.FIREBASE_TOKEN }}
          groups: testers
          file: build/app/outputs/flutter-apk/app-release.apk
```

---

## Performance & Optimisations

### Caching Strategy

```dart
// Cache les analyses fréquentes
class CacheService {
  static final Map<String, AnalysisResult> _cache = {};
  
  static AnalysisResult? get(String description) {
    // Normaliser la description (lowercase, trim)
    String key = description.toLowerCase().trim();
    return _cache[key];
  }
  
  static void set(String description, AnalysisResult result) {
    String key = description.toLowerCase().trim();
    _cache[key] = result;
    
    // Limiter taille du cache
    if (_cache.length > 100) {
      _cache.remove(_cache.keys.first);
    }
  }
}
```

### Optimisation des prompts

```dart
// Prompt court et structuré pour économiser tokens
const String ANALYSIS_PROMPT = '''
Analyze meal: "{meal_description}"
Return JSON only:
{
  "calories": number,
  "proteins": number,
  "carbs": number,
  "fats": number,
  "fiber": number,
  "suggestions": [string]
}
''';
```

---

**Version :** 1.0  
**Dernière mise à jour :** 9 novembre 2025

