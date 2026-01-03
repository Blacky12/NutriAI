# 🥗 NutriAI - Assistant Nutritionnel Intelligent

Application mobile Android avec backend FastAPI pour analyser les repas grâce à l'IA OpenRouter.

## 🛠️ Stack Technique

| Domaine | Technologie |
|---------|-------------|
| **Frontend** | Kotlin + Jetpack Compose |
| **Backend** | FastAPI (Python) |
| **Auth** | Clerk (à implémenter) |
| **Base de données** | PostgreSQL |
| **ORM** | SQLAlchemy |
| **IA** | OpenRouter (GPT-3.5 Turbo) |
| **Hébergement** | Render / Railway |
| **Distribution** | APK Android |

## 🚀 Démarrage Rapide

Voir **[SETUP.md](SETUP.md)** pour le guide complet de configuration.

### Backend
```bash
cd backend
pip install -r requirements.txt
# Créer .env avec DATABASE_URL et OPENROUTER_API_KEY
uvicorn app.main:app --reload
```

### Android
1. Ouvrir `android_app/` dans Android Studio
2. Run ▶️

## 📁 Structure

```
project2/
├── backend/              # API FastAPI
│   ├── app/
│   │   ├── api/v1/      # Endpoints
│   │   ├── core/        # Config, Database
│   │   ├── models/     # SQLAlchemy models
│   │   └── schemas/     # Pydantic schemas
│   └── requirements.txt
├── android_app/          # App Android
│   └── app/src/main/java/com/nutriai/app/
│       ├── data/api/    # Retrofit
│       ├── ui/screens/  # Compose screens
│       └── viewmodel/   # ViewModels
└── README.md
```

## 🎯 Fonctionnalités

- ✅ Analyse de repas par description texte via IA (GPT-3.5 Turbo)
- ✅ Affichage nutritionnel complet (calories, protéines, glucides, lipides)
- ✅ Suggestions d'amélioration nutritionnelle
- ✅ Historique des repas analysés
- ✅ Gestion des quotas utilisateurs
- ✅ Dashboard admin pour monitoring des coûts IA
- ✅ Landing page et page pricing
- ✅ Conformité légale (RGPD, AI Act, mentions légales)

## 📝 API Endpoints

- `POST /api/v1/meals/analyze` - Analyser un repas
- `GET /api/v1/meals/` - Historique des repas
- `GET /api/v1/admin/stats` - Statistiques admin

**Pages Web :**
- `/` - Landing page
- `/pricing` - Page tarifs
- `/admin` - Dashboard admin
- `/legal` - Mentions légales
- `/privacy` - Politique de confidentialité
- `/cookies` - Politique des cookies

Documentation API : `http://localhost:8000/docs`

## 📚 Documentation

- **[SETUP.md](SETUP.md)** - Guide de configuration
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Guide de déploiement
- **[docs/suivi_hebdomadaire.md](docs/suivi_hebdomadaire.md)** - Document de suivi
- **[docs/cahier_des_charges.md](docs/cahier_des_charges.md)** - Cahier des charges complet

## 📄 Licence

Projet scolaire - École
