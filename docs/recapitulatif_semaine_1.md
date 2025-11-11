# 📊 Récapitulatif Détaillé - Semaine 1

**Date :** 9 novembre - 11 novembre 2025  
**Objectif :** Organisation du projet, choix de la stack technique, architecture, authentification basique

---

## 🎯 Ce qui a été accompli

### 1. **Prise de décision stratégique**

#### Choix du concept
- **Projet retenu :** Assistant Diététique IA (NutriAI)
- **Problème résolu :** Aider les utilisateurs à mieux manger grâce à l'analyse nutritionnelle automatisée par IA
- **Public cible :** Personnes soucieuses de leur alimentation (18-45 ans), sportifs, étudiants

#### Stack technologique choisie
| Composant | Technologie | Justification |
|-----------|-------------|---------------|
| **Frontend** | Flutter (Dart) | Multiplateforme (mobile + web), performant, moderne |
| **State Management** | Provider | Simple, recommandé par Flutter, adapté au projet |
| **Backend** | Firebase | Gratuit, bien intégré avec Flutter, services complets |
| **Authentification** | Firebase Auth | Email/Password, sécurisé, facile à implémenter |
| **Base de données** | Cloud Firestore | NoSQL, temps réel, évolutif |
| **Intelligence Artificielle** | OpenRouter API | Accès à plusieurs modèles IA (GPT, Claude, Llama) |
| **Hébergement** | Firebase Hosting + App Distribution | Gratuit, URL publique, facile à déployer |

---

### 2. **Configuration de l'environnement**

#### Firebase
- ✅ Projet Firebase créé : `nutriai-edd68`
- ✅ Firebase Authentication activée (Email/Password)
- ✅ Cloud Firestore créé (région : europe-west1)
- ✅ Application Flutter connectée à Firebase (Android, iOS, Web, Windows, macOS)
- ✅ Configuration automatique via FlutterFire CLI

#### Git & GitHub
- ✅ Repository GitHub créé : `https://github.com/Blacky12/NutriAI.git`
- ✅ Stratégie Git Flow mise en place :
  - `main` → Production (versions stables)
  - `develop` → Développement (intégration continue)
  - `feature/*` → Nouvelles fonctionnalités
- ✅ 11 commits organisés par fonctionnalité
- ✅ `.gitignore` configuré pour protéger les fichiers sensibles

#### Dépendances Flutter ajoutées
```yaml
dependencies:
  firebase_core: ^3.6.0          # Firebase SDK de base
  firebase_auth: ^5.3.1          # Authentification
  cloud_firestore: ^5.4.4        # Base de données
  cloud_functions: ^5.1.3        # Cloud Functions
  provider: ^6.1.2               # State management
  http: ^1.2.2                   # Appels API
  intl: ^0.19.0                  # Formatage dates/nombres
```

---

### 3. **Architecture du projet**

#### Structure des dossiers
```
lib/
├── app/
│   ├── routes/          # Navigation (à implémenter)
│   └── theme/           # ✅ Thème personnalisé (couleurs, styles)
├── core/
│   ├── constants/       # ✅ Constantes (API, app)
│   ├── services/        # ✅ Services (Auth, Database)
│   └── utils/           # ✅ Utilitaires (validators)
├── models/              # ✅ Modèles de données (User, Meal)
├── providers/           # ✅ State management (AuthProvider)
├── screens/             # ✅ Écrans de l'application
│   ├── auth/           # ✅ Login, Register
│   ├── home/           # ✅ Écran d'accueil
│   ├── meal/           # À implémenter (S2)
│   ├── profile/        # À implémenter (S3)
│   └── admin/          # À implémenter (S3-4)
└── widgets/             # ✅ Composants réutilisables
    ├── common/         # ✅ CustomButton, CustomTextField, LoadingIndicator
    └── meal/           # À implémenter (S2)
```

#### Architecture Clean
- **Séparation des responsabilités** : UI / Business Logic / Data
- **Services** : Encapsulation de la logique Firebase
- **Providers** : Gestion d'état centralisée et réactive
- **Models** : Représentation typée des données
- **Widgets réutilisables** : DRY (Don't Repeat Yourself)

---

### 4. **Modèles de données créés**

#### UserModel
Représente un utilisateur de l'application :
```dart
class UserModel {
  final String uid;              // ID unique Firebase
  final String email;            // Email
  final String displayName;      // Nom d'affichage
  final DateTime createdAt;      // Date de création
  final DateTime? lastLoginAt;   // Dernière connexion
  final String subscription;     // 'free', 'pro', 'premium'
  final int dailyQuota;          // Quota quotidien d'analyses
  final int quotaUsed;           // Quota utilisé aujourd'hui
  final DateTime quotaResetDate; // Date de reset du quota
}
```

**Fonctionnalités :**
- Conversion vers/depuis Firestore
- Vérification du quota (`hasReachedQuota()`)
- Méthode `copyWith()` pour les modifications

#### MealModel
Représente une analyse de repas :
```dart
class MealModel {
  final String id;                    // ID unique
  final String userId;                // ID de l'utilisateur
  final String description;           // Description du repas
  final NutritionAnalysis analysis;   // Résultats nutritionnels
  final DateTime timestamp;           // Date de l'analyse
  final MealMetadata metadata;        // Métadonnées (coût, tokens, modèle)
}
```

**Sous-modèles :**
- `NutritionAnalysis` : calories, protéines, glucides, lipides, fibres, suggestions
- `MealMetadata` : modèle IA utilisé, tokens consommés, coût en USD, temps de réponse

---

### 5. **Services implémentés**

#### AuthService
Gère toute l'authentification Firebase :
- ✅ `signUpWithEmail()` - Création de compte + document Firestore
- ✅ `signInWithEmail()` - Connexion + mise à jour lastLoginAt
- ✅ `signOut()` - Déconnexion
- ✅ `resetPassword()` - Réinitialisation mot de passe
- ✅ `getUserData()` - Récupération des données utilisateur
- ✅ Gestion des erreurs Firebase (messages en français)

#### DatabaseService
Gère les interactions avec Firestore :
- ✅ CRUD utilisateurs (getUser, updateUser)
- ✅ Gestion des quotas (incrementQuotaUsed, resetDailyQuota)
- ✅ CRUD repas (createMeal, getMeal, deleteMeal)
- ✅ Historique des repas en temps réel (Stream)
- ✅ Statistiques utilisateur (nombre de repas, calories moyennes)
- ✅ Métriques admin (pour le dashboard)

---

### 6. **State Management avec Provider**

#### AuthProvider
Provider principal pour gérer l'état d'authentification :

**État géré :**
- `currentUser` : Utilisateur connecté (UserModel)
- `isLoading` : Indicateur de chargement
- `errorMessage` : Message d'erreur
- `isAuthenticated` : Booléen de connexion
- `authStateChanges` : Stream Firebase Auth

**Méthodes :**
- `initialize()` : Charge les données utilisateur au démarrage
- `signUp()` : Inscription
- `signIn()` : Connexion
- `signOut()` : Déconnexion
- `resetPassword()` : Reset mot de passe
- `refreshUserData()` : Rafraîchir les données
- `incrementQuota()` : Incrémenter le quota utilisé
- `hasReachedQuota()` : Vérifier si quota atteint

**Avantages :**
- ✅ UI réactive automatiquement aux changements
- ✅ État centralisé accessible partout
- ✅ Gestion propre du loading et des erreurs

---

### 7. **Design System**

#### Couleurs personnalisées (AppColors)
```dart
// Couleurs principales
primary: #4CAF50 (Vert nutritif)
secondary: #FF9800 (Orange énergique)

// Couleurs nutritionnelles (pour les macros)
calories: #FF5722 (Rouge-orange)
proteins: #2196F3 (Bleu)
carbs: #FF9800 (Orange)
fats: #9C27B0 (Violet)
fiber: #4CAF50 (Vert)
```

#### Thème Material 3
- AppBar verte avec texte blanc
- Boutons arrondis (12px border radius)
- Cards avec élévation subtile
- Champs de texte avec bordures douces
- Typographie hiérarchisée (6 tailles différentes)

---

### 8. **Fonctionnalités implémentées**

#### ✅ Système d'authentification complet

**Écran de connexion (LoginScreen) :**
- Logo et branding
- Champ email avec validation
- Champ mot de passe avec affichage/masquage
- Bouton de connexion avec indicateur de chargement
- Lien vers l'inscription
- Gestion des erreurs (messages en français)

**Écran d'inscription (RegisterScreen) :**
- Champ nom complet
- Champ email avec validation
- Champ mot de passe avec validation (min 6 caractères)
- Champ confirmation mot de passe
- Bouton d'inscription avec loading
- Retour vers la connexion
- Création automatique du document Firestore

**Validation des champs :**
- Email : format valide requis
- Mot de passe : minimum 6 caractères
- Nom : minimum 2 caractères
- Confirmation : doit correspondre au mot de passe

#### ✅ Écran d'accueil (HomeScreen)

**Carte de profil :**
- Avatar circulaire
- Nom de l'utilisateur
- Email affiché
- Bouton de déconnexion

**Carte de quota journalier :**
- Badge du plan (FREE/PRO/PREMIUM)
- Barre de progression visuelle
- Compteur d'analyses utilisées (ex: 0/10)
- Couleur adaptative selon le plan

**Disclaimer médical :**
- Icône d'avertissement
- Texte légal complet
- Fond coloré pour la visibilité
- ⚠️ "Cette application ne remplace pas l'avis d'un professionnel de santé"

**Boutons d'actions futures :**
- "Analyser un repas" (prêt pour S2)
- "Historique" (prêt pour S3)
- Messages temporaires : "Disponible en Semaine X"

#### ✅ Navigation automatique (AuthWrapper)
- Détection automatique de l'état d'authentification
- Redirection vers Login si non connecté
- Redirection vers Home si connecté
- Écran de chargement pendant la vérification

---

### 9. **Widgets réutilisables créés**

#### CustomTextField
Champ de texte personnalisé avec :
- Label
- Placeholder
- Icônes préfixe/suffixe
- Validation intégrée
- Mode obscure pour mot de passe
- Support multilignes
- État activé/désactivé

#### CustomButton
Bouton personnalisé avec :
- Variantes : elevated / outlined
- Indicateur de chargement intégré
- Support icônes
- Couleurs personnalisables
- Style cohérent avec le thème

#### LoadingIndicator
Indicateur de chargement avec :
- CircularProgressIndicator
- Message optionnel
- Centrage automatique
- Style personnalisé (couleur verte)

---

### 10. **Documentation créée**

#### 📄 Cahier des charges (398 lignes)
- Concept et problématique
- Acteurs et use cases
- Architecture technique détaillée
- Modèle de données Firestore
- Justification du choix du modèle IA
- Stratégie de pricing
- Conformité légale (RGPD, AI Act)
- Planning détaillé (8 semaines)
- Risques et mitigation

#### 🏗️ Architecture technique (476 lignes)
- Schémas d'architecture
- Structure Flutter détaillée
- Collections Firestore
- Cloud Functions à créer
- Flux de données
- Règles de sécurité Firestore
- Stratégie de déploiement
- Optimisations (caching, prompts)

#### 📊 Document de suivi S1 (95 lignes)
- Réalisations de la semaine
- Planification S2
- Screenshots des avancées
- Notes et apprentissages
- Métriques (commits, LOC, coûts)

#### 🔑 Guide OpenRouter (303 lignes)
- Qu'est-ce qu'OpenRouter
- Étapes de création de compte
- Stockage sécurisé des clés API
- Dashboard de monitoring
- Comparatif des modèles IA
- Estimation des coûts
- Tests de l'API
- Bonnes pratiques de sécurité

#### 📖 README.md complet (231 lignes)
- Description du projet
- Technologies utilisées
- Instructions d'installation
- Structure du projet
- Fonctionnalités implémentées/à venir
- Progression par semaine
- Documentation légale
- Contact et remerciements

---

### 11. **Stratégie Git & Commits**

#### Workflow Git Flow professionnel
```
main (production)
  └── develop (intégration)
        └── feature/* (nouvelles fonctionnalités)
```

#### Commits effectués (11 au total)
1. `chore: configuration initiale du projet (gitignore, README)`
2. `docs: ajout documentation complète (CDC, architecture, suivi S1, guide OpenRouter)`
3. `config: configuration Firebase et dépendances (Auth, Firestore, Functions)`
4. `feat: ajout modèles de données (User, Meal, constantes, validators)`
5. `feat: ajout services Firebase (AuthService, DatabaseService)`
6. `feat: ajout state management (AuthProvider) et design system (thème, couleurs)`
7. `feat: ajout widgets réutilisables (CustomButton, CustomTextField, LoadingIndicator)`
8. `feat: ajout système d'authentification (login, register, validation)`
9. `feat: ajout écran d'accueil et navigation (HomeScreen, AuthWrapper)`
10. `config: ajout configuration multi-plateforme (web, linux, macos, windows)`
11. `fix: amélioration affichage disclaimer médical et correction CardTheme`

**Convention utilisée :** Conventional Commits
- `feat:` Nouvelle fonctionnalité
- `fix:` Correction de bug
- `docs:` Documentation
- `config:` Configuration
- `chore:` Tâches diverses

---

### 12. **Sécurité mise en place**

#### Protection des données sensibles
- ✅ `.gitignore` configuré pour exclure :
  - Variables d'environnement (`.env`)
  - Clés API
  - Fichiers de build
  - Fichiers Firebase sensibles

#### Règles Firestore (à implémenter complètement)
- Authentification requise pour toutes les opérations
- Utilisateurs ne peuvent lire/modifier que leurs propres données
- Admin metrics en lecture seule (sauf Cloud Functions)

#### Validation des données
- Validation côté client (email, mot de passe, nom)
- Validation côté serveur via Firebase (à renforcer)
- Gestion des erreurs Firebase Auth

---

### 13. **Métriques du projet**

| Métrique | Valeur |
|----------|--------|
| **Commits** | 11 |
| **Lignes de code** | ~3500 |
| **Fichiers créés** | ~40 |
| **Documentation** | ~1500 lignes |
| **Dépendances** | 7 packages |
| **Temps estimé** | ~8-10 heures |
| **Coûts OpenRouter** | 0$ (pas encore utilisé) |
| **Tests effectués** | Fonctionnels manuels ✅ |

---

### 14. **Tests effectués**

#### Tests manuels réussis ✅
1. **Inscription :**
   - Création de compte avec email/password
   - Validation des champs
   - Création du document Firestore
   - Redirection automatique vers Home

2. **Connexion :**
   - Login avec identifiants corrects
   - Gestion des erreurs (mauvais password)
   - Chargement des données utilisateur
   - Affichage du profil

3. **Déconnexion :**
   - Bouton de déconnexion fonctionnel
   - Retour à l'écran de connexion
   - État nettoyé correctement

4. **Affichage Home :**
   - Profil utilisateur affiché
   - Quota visible (0/10)
   - Disclaimer médical visible
   - Boutons d'actions présents

5. **Navigation :**
   - AuthWrapper redirige correctement
   - Pas d'accès à Home sans authentification
   - Persistance de la session

---

### 15. **Problèmes rencontrés et solutions**

#### Problème 1 : CardTheme Material 3
**Erreur :** `The argument type 'CardTheme' can't be assigned to the parameter type 'CardThemeData'`

**Cause :** Incompatibilité avec Material 3 dans Flutter

**Solution :** Suppression du `cardTheme` personnalisé, utilisation du style par défaut Material 3

**Impact :** Minime, les Cards s'affichent correctement avec le style par défaut

#### Problème 2 : Méthode updateDisplayProfile inexistante
**Erreur :** `The method 'updateDisplayProfile' isn't defined for the type 'User'`

**Cause :** Nom de méthode incorrect dans Firebase Auth

**Solution :** Utilisation de `updateProfile(displayName: ...)` à la place

**Impact :** Corrigé immédiatement, fonctionnel

#### Problème 3 : Conflits .gitignore et README
**Erreur :** Fichiers en conflit lors du `git pull`

**Cause :** GitHub a créé des fichiers que le projet local avait aussi

**Solution :** Renommage temporaire, pull, puis restauration du fichier local

**Impact :** Résolu, aucune perte de données

---

### 16. **Apprentissages clés**

#### Techniques
- ✅ Configuration complète d'un projet Flutter + Firebase
- ✅ Architecture Clean (séparation des responsabilités)
- ✅ State management avec Provider
- ✅ Firestore : modélisation de données NoSQL
- ✅ Git Flow professionnel (branches, commits structurés)
- ✅ Material Design 3 avec Flutter
- ✅ Gestion de l'authentification Firebase

#### Bonnes pratiques
- ✅ Commits atomiques par fonctionnalité
- ✅ Documentation dès le début du projet
- ✅ Validation des données côté client
- ✅ Séparation UI / Logic / Data
- ✅ Widgets réutilisables (DRY)
- ✅ Gestion propre des erreurs
- ✅ Sécurité des données sensibles (.gitignore)

#### Soft skills
- ✅ Planification structurée (CDC, architecture)
- ✅ Prise de décision technique justifiée
- ✅ Résolution de problèmes (debugging)
- ✅ Documentation claire et complète
- ✅ Organisation Git professionnelle

---

### 17. **Prochaines étapes - Semaine 2**

#### Objectifs S2 (16-22 novembre)
1. **Intégration OpenRouter :**
   - Configuration de l'API
   - Création d'une Cloud Function `analyzeMeal`
   - Tests avec différents modèles IA
   - Choix du modèle optimal (coût/performance)

2. **Écran d'analyse de repas :**
   - `MealInputScreen` : saisie texte du repas
   - `MealResultScreen` : affichage des résultats
   - Validation de la description
   - Gestion du quota

3. **Prompt engineering :**
   - Création du prompt système
   - Optimisation pour réduire les tokens
   - Format de réponse JSON structuré
   - Tests et ajustements

4. **Sauvegarde des analyses :**
   - Enregistrement dans Firestore
   - Incrémentation du quota
   - Métadonnées (coût, tokens, temps)

5. **Premiers tests réels :**
   - Analyse de repas de test
   - Vérification de la précision
   - Monitoring des coûts
   - Ajustements si nécessaire

#### Livrables S2
- ✅ Fonctionnalité d'analyse opérationnelle
- ✅ Cloud Function déployée
- ✅ Monitoring des coûts en place
- ✅ Document de suivi S2
- ✅ Tests avec budget 2$ respecté

---

### 18. **Ressources utilisées**

#### Documentation officielle
- [Flutter Documentation](https://flutter.dev/docs)
- [Firebase pour Flutter](https://firebase.flutter.dev/)
- [Provider Package](https://pub.dev/packages/provider)
- [OpenRouter API Docs](https://openrouter.ai/docs)
- [Material Design 3](https://m3.material.io/)

#### Outils
- **Cursor** (AI Assistant) - Claude Sonnet 4.5
- **VS Code / Cursor IDE**
- **Git & GitHub**
- **Firebase Console**
- **FlutterFire CLI**
- **Android Emulator**

#### Packages Flutter
- firebase_core, firebase_auth, cloud_firestore
- cloud_functions, provider, http, intl

---

### 19. **Répartition du travail**

**Travail solo** - Toutes les tâches réalisées avec accompagnement IA pour l'apprentissage :

| Tâche | Temps estimé | Statut |
|-------|--------------|--------|
| Prise de décision (concept, stack) | 1h | ✅ |
| Configuration Firebase | 0.5h | ✅ |
| Structure du projet | 1h | ✅ |
| Modèles de données | 1h | ✅ |
| Services Firebase | 2h | ✅ |
| State management | 1h | ✅ |
| Design system | 0.5h | ✅ |
| Écrans d'authentification | 2h | ✅ |
| Écran d'accueil | 1h | ✅ |
| Documentation | 2h | ✅ |
| Git & commits | 0.5h | ✅ |
| Tests & debugging | 1h | ✅ |
| **TOTAL** | **~13.5h** | ✅ |

---

### 20. **Conclusion Semaine 1**

#### 🎉 Succès
- ✅ Tous les objectifs de la semaine atteints
- ✅ Application fonctionnelle avec authentification complète
- ✅ Architecture solide et évolutive
- ✅ Documentation exhaustive
- ✅ Code propre et organisé
- ✅ Git Flow professionnel
- ✅ Base solide pour les semaines suivantes

#### 💪 Points forts
- Architecture bien pensée dès le départ
- Séparation claire des responsabilités
- Documentation complète et structurée
- Commits organisés et lisibles
- Tests fonctionnels réussis

#### 📈 Axes d'amélioration (S2+)
- Ajouter des tests unitaires
- Implémenter la gestion d'erreurs robuste
- Créer un système de caching
- Optimiser les performances
- Ajouter des animations UI

#### 🚀 Prêt pour la suite !
La Semaine 1 a posé des **fondations solides**. Le projet est bien structuré, documenté et prêt pour l'intégration de l'IA en Semaine 2.

**Prochaine grande étape :** Faire parler l'IA ! 🤖

---

**Date de rédaction :** 11 novembre 2025  
**Auteur :** Nicolas Ferbeck  
**Accompagnement :** Cursor AI (Claude Sonnet 4.5)

