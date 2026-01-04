# 🥗 NutriAI - Assistant Nutritionnel Intelligent

Application mobile Android avec backend FastAPI pour analyser les repas grâce à l'IA OpenRouter.

## 🛠️ Stack Technique

| Domaine | Technologie |
|---------|-------------|
| **Frontend** | Kotlin + Jetpack Compose |
| **Backend** | FastAPI (Python) |
| **Auth** | Clerk (intégré) |
| **Base de données** | PostgreSQL |
| **ORM** | SQLAlchemy |
| **IA** | OpenRouter (GPT-3.5 Turbo) |
| **Hébergement** | Render |
| **CI/CD** | GitHub Actions + Render |
| **Distribution** | APK Android |

## 🚀 Démarrage Rapide

### Backend

```bash
cd backend
pip install -r requirements.txt

# Créer un fichier .env avec :
# DATABASE_URL=postgresql://user:password@localhost:5432/nutriai_db
# OPENROUTER_API_KEY=votre_clé_api
# CLERK_SECRET_KEY=votre_clé_clerk (optionnel pour développement)

uvicorn app.main:app --reload
```

L'API sera disponible sur `http://localhost:8000`

### Android

1. Ouvrir `android_app/` dans Android Studio
2. Configurer l'URL de l'API dans `RetrofitClient.kt` :
   - Local : `http://10.0.2.2:8000/`
   - Production : `https://nutriai-backend-htic.onrender.com/`
3. Run ▶️

## 📁 Structure du Projet

```
project2/
├── backend/                    # API FastAPI
│   ├── app/
│   │   ├── api/v1/endpoints/  # Routes API (meals, admin, auth)
│   │   ├── core/              # Config, Database, Auth
│   │   ├── models/            # Modèles SQLAlchemy (User, Meal)
│   │   ├── schemas/           # Schémas Pydantic (validation)
│   │   └── static/             # Pages web (HTML)
│   ├── requirements.txt        # Dépendances Python
│   └── Procfile               # Configuration Render
├── android_app/                # App Android
│   └── app/src/main/java/com/nutriai/app/
│       ├── data/
│       │   ├── api/           # Retrofit (NutriApi, RetrofitClient)
│       │   └── auth/          # AuthManager
│       ├── ui/screens/         # Écrans Compose
│       └── viewmodel/          # ViewModels (MVVM)
├── .github/workflows/          # CI/CD GitHub Actions
├── render.yaml                 # Configuration Render
└── README.md
```

## 🎯 Fonctionnalités

### Application Mobile
- ✅ Authentification utilisateur (Clerk)
- ✅ Analyse de repas par description texte via IA (GPT-3.5 Turbo)
- ✅ Affichage nutritionnel complet (calories, protéines, glucides, lipides, fibres)
- ✅ Suggestions d'amélioration nutritionnelle
- ✅ Historique des repas analysés
- ✅ Gestion des quotas par abonnement (Free, Pro, Premium)

### Backend & Web
- ✅ API REST complète avec documentation automatique
- ✅ Dashboard admin sécurisé avec authentification
- ✅ Monitoring des coûts IA et statistiques d'utilisation
- ✅ Landing page et page pricing
- ✅ Conformité légale (RGPD, AI Act, mentions légales, cookies)

## 📝 API Endpoints

### Authentification
- `POST /api/v1/auth/signup` - Créer un compte
- `POST /api/v1/auth/signin` - Se connecter
- `GET /api/v1/auth/me` - Informations utilisateur (protégé)

### Repas
- `POST /api/v1/meals/analyze` - Analyser un repas (protégé)
- `GET /api/v1/meals/` - Historique des repas (protégé)

### Admin
- `POST /api/v1/admin/login` - Connexion admin
- `GET /api/v1/admin/logout` - Déconnexion admin
- `GET /api/v1/admin/stats` - Statistiques admin (protégé)

### Pages Web
- `/` - Landing page
- `/pricing` - Page tarifs
- `/admin` - Dashboard admin (authentification requise)
- `/legal` - Mentions légales
- `/privacy` - Politique de confidentialité
- `/cookies` - Politique des cookies

**Documentation API interactive :** 
- Local : `http://localhost:8000/docs`
- Production : `https://nutriai-backend-htic.onrender.com/docs`

## 🌐 URLs de Production

- **API** : https://nutriai-backend-htic.onrender.com
- **Landing Page** : https://nutriai-backend-htic.onrender.com/
- **Dashboard Admin** : https://nutriai-backend-htic.onrender.com/admin
  - Mot de passe par défaut : `admin123` (à changer en production)
- **Pricing** : https://nutriai-backend-htic.onrender.com/pricing
- **Documentation API** : https://nutriai-backend-htic.onrender.com/docs

## 🔐 Authentification

### Utilisateurs (App Mobile)
- Authentification via **Clerk**
- Tokens JWT ou simplifiés pour MVP
- Gestion automatique des sessions

### Admin (Dashboard Web)
- Authentification par mot de passe
- Session basée sur cookies
- Mot de passe configurable via variable d'environnement `ADMIN_PASSWORD`

## 🚀 Déploiement

### Backend sur Render

1. **Créer la base PostgreSQL** sur Render Dashboard
2. **Créer un Web Service** connecté au repo GitHub
3. **Configurer les variables d'environnement** :
   - `DATABASE_URL` (Internal Database URL)
   - `OPENROUTER_API_KEY`
   - `CLERK_SECRET_KEY`
   - `CLERK_PUBLISHABLE_KEY`
   - `ADMIN_PASSWORD` (optionnel, défaut: `admin123`)
   - `CORS_ORIGINS` (défaut: `*`)
4. Render déploie automatiquement à chaque push sur `main`

Voir **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)** pour le guide complet.

### Génération APK Android

```bash
cd android_app
./gradlew assembleRelease
```

L'APK sera dans : `app/build/outputs/apk/release/app-release.apk`

Voir **[docs/GENERER_APK.md](docs/GENERER_APK.md)** pour le guide détaillé.

## 🔄 CI/CD

Le projet utilise **GitHub Actions** pour le CI/CD :

- ✅ **CI (Continuous Integration)** : Tests, linting, validation du code
- ✅ **CD (Continuous Deployment)** : Déploiement automatique sur Render

**Workflow :**
1. Push sur `main` ou `develop` → GitHub Actions vérifie le code
2. Si tout est OK → Render déploie automatiquement (sur `main` uniquement)

**Fichiers de configuration :**
- `.github/workflows/ci.yml` - Pipeline CI
- `.github/workflows/deploy.yml` - Validation déploiement
- `render.yaml` - Configuration Render

## 📚 Documentation

- **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Guide de déploiement sur Render
- **[docs/GENERER_APK.md](docs/GENERER_APK.md)** - Guide pour générer l'APK Android
- **[docs/cahier_des_charges.md](docs/cahier_des_charges.md)** - Cahier des charges complet

## 🛠️ Développement

### Prérequis

- Python 3.11+
- PostgreSQL 14+
- Android Studio (pour l'app mobile)
- Compte Clerk (pour l'authentification)
- Clé API OpenRouter (pour l'IA)

### Variables d'environnement

Créer un fichier `.env` dans `backend/` :

```env
DATABASE_URL=postgresql://user:password@localhost:5432/nutriai_db
OPENROUTER_API_KEY=votre_clé_api
CLERK_SECRET_KEY=votre_clé_clerk
CLERK_PUBLISHABLE_KEY=votre_clé_publishable
ADMIN_PASSWORD=admin123
CORS_ORIGINS=*
DEBUG=False
```

### Tests locaux

```bash
# Backend
cd backend
uvicorn app.main:app --reload

# Tester l'API
curl http://localhost:8000/health
```

## 📊 Architecture

- **Backend** : FastAPI avec architecture modulaire (endpoints, models, schemas)
- **Frontend** : MVVM avec Jetpack Compose
- **Base de données** : PostgreSQL avec SQLAlchemy ORM
- **Authentification** : Clerk pour les utilisateurs, session cookies pour admin
- **IA** : OpenRouter API pour l'analyse nutritionnelle

## 🐛 Dépannage

### L'app Android ne se connecte pas
- Vérifier l'URL dans `RetrofitClient.kt`
- Vérifier que le backend est actif
- Vérifier les logs Android Studio

### Erreur de déploiement Render
- Vérifier les variables d'environnement
- Vérifier les logs dans Render Dashboard
- Vérifier que `requirements.txt` est à jour

### Erreur d'authentification
- Vérifier que `CLERK_SECRET_KEY` est configuré
- Vérifier les tokens dans les logs
- Vérifier que l'utilisateur existe dans Clerk

## 📄 Licence

Projet scolaire - École

---

**Version :** 1.0  
**Dernière mise à jour :** Janvier 2026
