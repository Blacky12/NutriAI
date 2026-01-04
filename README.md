# 🥗 NutriAI - Assistant Nutritionnel Intelligent

Application mobile Android native développée en **Kotlin + Jetpack Compose** avec un backend **FastAPI** pour analyser les repas grâce à l'IA **OpenRouter**.

## 📱 À propos

NutriAI est une application mobile Android qui permet d'analyser la valeur nutritionnelle d'un repas simplement en le décrivant en texte. L'application utilise l'intelligence artificielle (GPT-3.5 Turbo via OpenRouter) pour extraire les informations nutritionnelles et fournir des suggestions d'amélioration.

## 🛠️ Stack Technique

| Composant | Technologie |
|-----------|-------------|
| **Application Mobile** | Kotlin + Jetpack Compose (MVVM) |
| **Backend API** | FastAPI (Python 3.11+) |
| **Authentification** | Clerk |
| **Base de données** | PostgreSQL |
| **ORM** | SQLAlchemy |
| **IA / LLM** | OpenRouter (GPT-3.5 Turbo) |
| **Client HTTP** | Retrofit (Android) |
| **Hébergement** | Render |
| **CI/CD** | GitHub Actions + Render |
| **Distribution** | APK Android |

## 🚀 Installation et Configuration

### Prérequis

- **Python 3.11+** pour le backend
- **PostgreSQL 14+** pour la base de données
- **Android Studio** (version récente) pour l'application mobile
- **Compte Clerk** pour l'authentification
- **Clé API OpenRouter** pour l'analyse nutritionnelle

### Backend (FastAPI)

1. **Cloner le repository**
```bash
git clone <votre-repo>
cd project2
```

2. **Installer les dépendances Python**
```bash
cd backend
pip install -r requirements.txt
```

3. **Configurer les variables d'environnement**

Créer un fichier `.env` dans le dossier `backend/` :

```env
# Base de données PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/nutriai_db

# OpenRouter API (pour l'IA)
OPENROUTER_API_KEY=votre_clé_api_openrouter

# Clerk Authentication (optionnel pour développement local)
CLERK_SECRET_KEY=votre_clé_secret_clerk
CLERK_PUBLISHABLE_KEY=votre_clé_publishable_clerk

# Configuration admin dashboard
ADMIN_PASSWORD=admin123

# CORS (pour permettre les requêtes depuis l'app Android)
CORS_ORIGINS=*

# Mode debug
DEBUG=False
```

4. **Créer la base de données PostgreSQL**

```bash
# Via psql
createdb nutriai_db

# Ou via pgAdmin4
# Créer une nouvelle base de données nommée "nutriai_db"
```

5. **Lancer le serveur**

```bash
cd backend
uvicorn app.main:app --reload
```

Le serveur sera accessible sur `http://localhost:8000`

**Documentation API interactive :** `http://localhost:8000/docs`

### Application Android

1. **Ouvrir le projet dans Android Studio**
   - Ouvrir Android Studio
   - File → Open → Sélectionner le dossier `android_app/`

2. **Configurer l'URL de l'API**

Modifier le fichier `android_app/app/src/main/java/com/nutriai/app/data/api/RetrofitClient.kt` :

```kotlin
// Pour développement local (émulateur Android)
private const val BASE_URL = "http://10.0.2.2:8000/"

// Pour production
// private const val BASE_URL = "https://nutriai-backend-htic.onrender.com/"
```

**Note :** `10.0.2.2` est l'adresse IP spéciale de l'émulateur Android pour accéder à `localhost` de votre machine.

3. **Lancer l'application**
   - Connecter un appareil Android ou démarrer un émulateur
   - Cliquer sur Run ▶️ dans Android Studio

## 📁 Structure du Projet

```
project2/
├── backend/                          # Backend FastAPI
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── endpoints/       # Routes API (meals.py, admin.py, auth.py)
│   │   ├── core/                     # Configuration et utilitaires
│   │   │   ├── config.py            # Paramètres (Pydantic Settings)
│   │   │   ├── database.py          # Connexion PostgreSQL (SQLAlchemy)
│   │   │   ├── auth.py              # Authentification Clerk
│   │   │   └── admin_auth.py        # Authentification admin dashboard
│   │   ├── models/                  # Modèles SQLAlchemy
│   │   │   ├── user.py              # Modèle User
│   │   │   └── meal.py              # Modèle Meal
│   │   ├── schemas/                 # Schémas Pydantic (validation)
│   │   │   └── meal.py              # Schémas de validation
│   │   ├── static/                  # Pages web statiques (HTML)
│   │   │   ├── index.html           # Landing page
│   │   │   ├── pricing.html         # Page tarifs
│   │   │   ├── dashboard.html       # Dashboard admin
│   │   │   ├── legal.html           # Mentions légales
│   │   │   ├── privacy.html         # Politique de confidentialité
│   │   │   └── cookies.html         # Politique des cookies
│   │   └── main.py                  # Point d'entrée FastAPI
│   ├── requirements.txt             # Dépendances Python
│   └── Procfile                     # Configuration Render
│
├── android_app/                      # Application Android
│   └── app/
│       └── src/
│           └── main/
│               ├── java/com/nutriai/app/
│               │   ├── MainActivity.kt          # Point d'entrée app
│               │   ├── data/
│               │   │   ├── api/                  # Client API Retrofit
│               │   │   │   ├── NutriApi.kt       # Interface API
│               │   │   │   ├── RetrofitClient.kt # Configuration Retrofit
│               │   │   │   └── AuthInterceptor.kt # Intercepteur auth
│               │   │   └── auth/
│               │   │       └── AuthManager.kt     # Gestion authentification
│               │   ├── ui/
│               │   │   ├── screens/              # Écrans Compose
│               │   │   │   ├── LoginScreen.kt
│               │   │   │   ├── SignUpScreen.kt
│               │   │   │   ├── MealInputScreen.kt
│               │   │   │   ├── MealResultScreen.kt
│               │   │   │   └── MealHistoryScreen.kt
│               │   │   └── theme/               # Thème Material Design
│               │   └── viewmodel/                # ViewModels (MVVM)
│               │       ├── MealViewModel.kt
│               │       └── HomeViewModel.kt
│               └── res/                          # Ressources (images, layouts)
│
├── .github/
│   └── workflows/                   # CI/CD GitHub Actions
│       ├── ci.yml                   # Pipeline CI (tests, linting)
│       └── deploy.yml               # Validation déploiement
│
├── docs/                            # Documentation
│   ├── DEPLOYMENT.md                # Guide déploiement Render
│   ├── GENERER_APK.md               # Guide génération APK
│   └── cahier_des_charges.md        # Cahier des charges
│
├── render.yaml                      # Configuration Render (déploiement)
└── README.md                        # Ce fichier
```

## 🎯 Fonctionnalités

### Application Mobile Android

- ✅ **Authentification utilisateur** via Clerk
  - Inscription avec email et mot de passe
  - Connexion sécurisée
  - Gestion automatique des tokens

- ✅ **Analyse nutritionnelle par IA**
  - Description textuelle du repas
  - Analyse via GPT-3.5 Turbo (OpenRouter)
  - Extraction automatique des valeurs nutritionnelles

- ✅ **Affichage des résultats**
  - Calories totales
  - Protéines, glucides, lipides
  - Fibres alimentaires
  - Suggestions d'amélioration nutritionnelle

- ✅ **Historique des repas**
  - Liste de tous les repas analysés
  - Affichage par date
  - Détails nutritionnels pour chaque repas

- ✅ **Gestion des quotas**
  - Système d'abonnement (Free, Pro, Premium)
  - Limite quotidienne d'analyses selon l'abonnement
  - Suivi de l'utilisation

### Backend & Dashboard Web

- ✅ **API REST complète**
  - Documentation automatique (Swagger/OpenAPI)
  - Endpoints pour authentification, repas, admin
  - Validation des données avec Pydantic

- ✅ **Dashboard admin sécurisé**
  - Authentification par mot de passe
  - Statistiques en temps réel
  - Monitoring des coûts IA
  - Graphiques d'utilisation (Chart.js)

- ✅ **Pages web**
  - Landing page professionnelle
  - Page de tarification
  - Pages de conformité légale (RGPD, AI Act)

## 📝 API Endpoints

### Authentification (`/api/v1/auth`)

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `POST` | `/signup` | Créer un nouveau compte utilisateur |
| `POST` | `/signin` | Se connecter avec email/password |
| `GET` | `/me` | Obtenir les informations de l'utilisateur connecté |

### Repas (`/api/v1/meals`)

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `POST` | `/analyze` | Analyser un repas (protégé) |
| `GET` | `/` | Récupérer l'historique des repas (protégé) |

### Admin (`/api/v1/admin`)

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `POST` | `/login` | Connexion admin dashboard |
| `GET` | `/logout` | Déconnexion admin |
| `GET` | `/stats` | Statistiques admin (protégé) |

### Pages Web

| Route | Description |
|-------|-------------|
| `/` | Landing page |
| `/pricing` | Page tarifs |
| `/admin` | Dashboard admin (authentification requise) |
| `/legal` | Mentions légales |
| `/privacy` | Politique de confidentialité |
| `/cookies` | Politique des cookies |
| `/docs` | Documentation API interactive (Swagger) |

## 🌐 URLs de Production


- **Landing Page** : https://nutriai-backend-htic.onrender.com/
- **Dashboard Admin** : https://nutriai-backend-htic.onrender.com/admin
  - Mot de passe par défaut : `admin123`
- **Page Pricing** : https://nutriai-backend-htic.onrender.com/pricing


## 🔐 Authentification

### Utilisateurs (Application Mobile)

L'authentification est gérée par **Clerk**, un service d'authentification moderne :

- Inscription avec email et mot de passe
- Tokens JWT pour sécuriser les requêtes API
- Gestion automatique des sessions
- Synchronisation avec la base de données locale

### Admin (Dashboard Web)

Le dashboard admin utilise une authentification par mot de passe simple :

- Mot de passe configurable via variable d'environnement `ADMIN_PASSWORD`
- Sessions basées sur cookies HTTP-only
- Déconnexion sécurisée

## 🚀 Déploiement

### Backend sur Render

Le backend est déployé automatiquement sur **Render** à chaque push sur la branche `main`.

**Configuration :**
1. Créer une base PostgreSQL sur Render Dashboard
2. Créer un Web Service connecté au repository GitHub
3. Configurer les variables d'environnement (voir section Configuration)
4. Render déploie automatiquement

Voir **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)** pour le guide détaillé.

### Génération APK Android

Pour générer un APK signé pour installer sur un appareil Android :

```bash
cd android_app
./gradlew assembleRelease
```

L'APK sera généré dans : `app/build/outputs/apk/release/app-release.apk`

Voir **[docs/GENERER_APK.md](docs/GENERER_APK.md)** pour le guide complet avec Android Studio.

## 🔄 CI/CD

Le projet utilise **GitHub Actions** pour l'intégration et le déploiement continus :

### Pipeline CI (Continuous Integration)

- ✅ Validation du code Python (linting avec flake8)
- ✅ Vérification du formatage (black)
- ✅ Tests d'import et de build
- ✅ Validation des fichiers de configuration

### Pipeline CD (Continuous Deployment)

- ✅ Déploiement automatique sur Render lors d'un push sur `main`
- ✅ Health checks automatiques
- ✅ Rollback en cas d'erreur

**Fichiers de configuration :**
- `.github/workflows/ci.yml` - Pipeline CI
- `.github/workflows/deploy.yml` - Validation déploiement
- `render.yaml` - Configuration Render

## 📊 Architecture

### Backend (FastAPI)

- **Architecture modulaire** : séparation endpoints, models, schemas
- **Dependency Injection** : FastAPI `Depends()` pour les sessions DB et auth
- **ORM SQLAlchemy** : abstraction de la base de données
- **Validation Pydantic** : validation automatique des données

### Frontend Android

- **Architecture MVVM** : séparation logique métier (ViewModel) et UI (Compose)
- **Jetpack Compose** : UI déclarative moderne
- **StateFlow** : gestion d'état réactive
- **Retrofit** : client HTTP type-safe
- **Navigation Compose** : gestion de la navigation entre écrans

### Base de données

- **PostgreSQL** : base de données relationnelle
- **SQLAlchemy ORM** : mapping objet-relationnel
- **Modèles** : User (utilisateurs), Meal (repas analysés)

## 🛠️ Développement

### Tests locaux

**Backend :**
```bash
cd backend
uvicorn app.main:app --reload

# Tester l'API
curl http://localhost:8000/health
```

**Android :**
- Lancer l'émulateur ou connecter un appareil
- Configurer `BASE_URL` sur `http://10.0.2.2:8000/`
- Run dans Android Studio

### Variables d'environnement

Toutes les variables d'environnement sont définies dans `backend/app/core/config.py` et peuvent être surchargées via un fichier `.env` ou les variables d'environnement système.

## 🐛 Dépannage

### L'application Android ne se connecte pas au backend

1. Vérifier que le backend est lancé (`uvicorn app.main:app --reload`)
2. Vérifier l'URL dans `RetrofitClient.kt` :
   - Émulateur : `http://10.0.2.2:8000/`
   - Appareil physique : `http://<IP_LOCALE>:8000/`
3. Vérifier les logs Android Studio (Logcat)
4. Vérifier que CORS est configuré (`CORS_ORIGINS=*`)

### Erreur de déploiement Render

1. Vérifier les variables d'environnement dans Render Dashboard
2. Vérifier les logs de build dans Render
3. Vérifier que `requirements.txt` contient toutes les dépendances
4. Vérifier que `Procfile` existe et est correct

### Erreur d'authentification

1. Vérifier que `CLERK_SECRET_KEY` est configuré
2. Vérifier les tokens dans les logs backend
3. Vérifier que l'utilisateur existe dans Clerk Dashboard
4. Vérifier les headers `Authorization` dans les requêtes

## 📚 Documentation

- **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Guide complet de déploiement sur Render
- **[docs/GENERER_APK.md](docs/GENERER_APK.md)** - Guide pour générer et installer l'APK Android
- **[docs/cahier_des_charges.md](docs/cahier_des_charges.md)** - Cahier des charges complet du projet

## 📄 Licence

Projet scolaire - École

---

**Version :** 1.0  
**Dernière mise à jour :** Janvier 2026  
**Stack :** Kotlin + Jetpack Compose + FastAPI + PostgreSQL
