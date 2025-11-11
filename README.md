# 🥗 NutriAI - Assistant Nutritionnel Intelligent

Application mobile diététique avec IA implémentée pour les besoins nutritionnels de l'utilisateur.

---

## 📋 Description

**NutriAI** est une application mobile Flutter qui utilise l'intelligence artificielle pour analyser les repas et fournir des conseils nutritionnels personnalisés. Le projet utilise Firebase pour l'authentification et le stockage de données, et OpenRouter pour l'intégration de modèles d'IA.

### 🎯 Objectifs du projet

- Permettre aux utilisateurs d'analyser leurs repas (description texte)
- Fournir des informations nutritionnelles détaillées (calories, macros)
- Suggérer des améliorations alimentaires personnalisées
- Suivre l'historique des repas
- Dashboard administrateur pour monitoring des coûts IA

---

## 🛠️ Technologies utilisées

### Frontend
- **Flutter** (Dart) - Framework mobile multiplateforme
- **Provider** - Gestion d'état
- **Material Design 3** - Design system

### Backend
- **Firebase Authentication** - Authentification utilisateurs
- **Cloud Firestore** - Base de données NoSQL
- **Firebase Cloud Functions** - API backend sécurisé
- **Firebase Hosting** - Déploiement web
- **Firebase App Distribution** - Distribution mobile

### Intelligence Artificielle
- **OpenRouter API** - Accès aux modèles IA (GPT-4, Claude, Llama, Mistral)
- Budget : 2$ pour le développement

---

## 📦 Installation

### Prérequis
- Flutter SDK (3.9.2+)
- Dart SDK
- Firebase CLI
- Un compte Firebase
- Un compte OpenRouter (optionnel pour le développement)

### Étapes d'installation

1. **Cloner le repository**
```bash
git clone https://github.com/Blacky12/NutriAI.git
cd NutriAI
```

2. **Installer les dépendances**
```bash
flutter pub get
```

3. **Configuration Firebase**
```bash
# Installer FlutterFire CLI si nécessaire
dart pub global activate flutterfire_cli

# Configurer Firebase pour le projet
flutterfire configure
```

4. **Lancer l'application**
```bash
# Sur émulateur/device Android
flutter run

# Sur navigateur web
flutter run -d chrome
```

---

## 📁 Structure du projet

```
lib/
├── app/                    # Configuration de l'application
│   └── theme/             # Thème et couleurs
├── core/                  # Code réutilisable
│   ├── constants/         # Constantes
│   ├── services/          # Services (Auth, Database, AI)
│   └── utils/             # Utilitaires (validators, formatters)
├── models/                # Modèles de données
├── providers/             # State management (Provider)
├── screens/               # Écrans de l'application
│   ├── auth/             # Login, Register
│   ├── home/             # Page d'accueil
│   ├── meal/             # Analyse de repas
│   ├── profile/          # Profil utilisateur
│   └── admin/            # Dashboard admin
└── widgets/               # Widgets réutilisables
    ├── common/           # Widgets génériques
    └── meal/             # Widgets spécifiques aux repas
```

---

## 🚀 Fonctionnalités

### ✅ Implémentées (Semaine 1)
- [x] Authentification (inscription/connexion)
- [x] Gestion des utilisateurs (Firestore)
- [x] Interface de base avec navigation
- [x] Système de quotas quotidiens
- [x] Architecture propre et modulaire

### 🚧 En cours de développement
- [ ] Analyse de repas par texte (Semaine 2)
- [ ] Intégration OpenRouter (Semaine 2)
- [ ] Historique des analyses (Semaine 3)
- [ ] Dashboard administrateur (Semaine 3-4)
- [ ] Landing page + pricing (Semaine 5)
- [ ] CI/CD avec GitHub Actions (Semaine 6)

### 🔮 Fonctionnalités futures
- [ ] Analyse de repas par photo
- [ ] Coach IA personnalisé
- [ ] Export PDF des analyses
- [ ] Application mobile native (iOS)

---

## 📊 Progression du projet

| Semaine | Objectifs | Statut |
|---------|-----------|--------|
| **S1** | Organisation, architecture, auth | ✅ Terminée |
| **S2** | Intégration OpenRouter, analyse IA | 🚧 En cours |
| **S3** | Dashboard monitoring, optimisation | ⏳ À venir |
| **S4** | Gestion erreurs, caching | ⏳ À venir |
| **S5** | Landing page, pricing | ⏳ À venir |
| **S6** | Fonctionnalités optionnelles | ⏳ À venir |
| **S7** | Finitions, rapport final | ⏳ À venir |
| **S8** | Tests finaux, livraison | ⏳ À venir |

**Date de livraison :** 4 janvier 2026

---

## 📖 Documentation

Toute la documentation du projet se trouve dans le dossier `docs/` :

- **[Cahier des charges](docs/cahier_des_charges.md)** - Spécifications complètes
- **[Architecture technique](docs/architecture.md)** - Détails de l'architecture
- **[Suivi hebdomadaire](docs/suivi_semaine_1.md)** - Progression et notes
- **[Guide OpenRouter](docs/setup_openrouter.md)** - Configuration de l'API IA

---

## 🔐 Conformité légale

Le projet respecte :
- **RGPD** - Protection des données personnelles
- **AI Act** - Réglementation européenne sur l'IA
- **Disclaimer médical** - Limitations clairement indiquées

⚠️ **Disclaimer** : Cette application fournit des informations nutritionnelles à titre indicatif uniquement. Elle ne remplace pas l'avis d'un professionnel de santé.

---

## 🧪 Tests

```bash
# Lancer les tests unitaires
flutter test

# Lancer les tests d'intégration
flutter drive --target=test_driver/app.dart
```

---

## 🌐 Déploiement

### Version Web
```bash
flutter build web --release
firebase deploy --only hosting
```

### Version Android (APK)
```bash
flutter build apk --release
# Upload sur Firebase App Distribution
```

---

## 👥 Auteur

**Blacky12** - Projet scolaire - École  
Accompagnement IA : Cursor (Claude Sonnet 4.5)

---

## 📄 Licence

Ce projet est développé dans un cadre scolaire.

---

## 🙏 Remerciements

- **Professeur** - Pour l'encadrement du projet
- **Firebase** - Pour les services backend gratuits
- **OpenRouter** - Pour l'accès aux modèles IA
- **Flutter Community** - Pour les packages et ressources

---

## 📞 Contact

Pour toute question sur le projet, consultez la documentation dans le dossier `docs/` ou créez une issue sur GitHub.

---

**Date de création :** 9 novembre 2025  
**Dernière mise à jour :** 11 novembre 2025  
**Version :** 1.0.0 (Semaine 1)
