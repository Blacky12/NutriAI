# 📋 Cahier des Charges - Assistant Diététique IA

**Nom du projet :** NutriAI Assistant  
**Date de création :** 9 novembre 2025  
**Date de livraison :** 4 janvier 2026  
**Équipe :** Solo

---

## 1. Concept & Problématique

### 🎯 Problème résolu
Beaucoup de personnes souhaitent manger plus sainement mais :
- Ne connaissent pas la valeur nutritionnelle de leurs repas
- N'ont pas le temps de chercher les informations nutritionnelles
- Ont du mal à équilibrer leur alimentation au quotidien

### 💡 Solution proposée
Une application mobile qui analyse instantanément les repas (par description texte) et fournit :
- Informations nutritionnelles détaillées (calories, macros, micros)
- Suggestions d'amélioration personnalisées
- Historique et suivi des repas
- Conseils nutritionnels adaptés

### 👥 Public cible
- Personnes soucieuses de leur alimentation (18-45 ans)
- Sportifs en phase de rééquilibrage alimentaire
- Étudiants voulant mieux manger sans expertise nutritionnelle
- Familles cherchant à adopter une alimentation plus saine

### ⚠️ Disclaimer médical
**Important :** Cette application ne remplace pas l'avis d'un professionnel de santé. Les suggestions sont à titre informatif uniquement.

---

## 2. Acteurs & Use Cases

### Acteurs principaux

#### 👤 Utilisateur standard (authentifié)
- Peut analyser ses repas par description texte
- Consulte l'historique de ses analyses
- Reçoit des suggestions nutritionnelles personnalisées
- Suit ses statistiques (quotidiennes, hebdomadaires)

#### 👨‍💼 Administrateur
- Accède au dashboard de monitoring
- Surveille les coûts OpenRouter en temps réel
- Visualise les statistiques d'utilisation
- Gère les utilisateurs (si nécessaire)

### Use Cases principaux

```
┌─────────────────────────────────────────┐
│          UTILISATEUR                    │
└─────────────────────────────────────────┘
              │
              ├─→ S'inscrire / Se connecter
              ├─→ Analyser un repas (texte)
              ├─→ Consulter les résultats nutritionnels
              ├─→ Voir l'historique des repas
              ├─→ Consulter ses statistiques
              └─→ Modifier son profil

┌─────────────────────────────────────────┐
│         ADMINISTRATEUR                  │
└─────────────────────────────────────────┘
              │
              ├─→ Accéder au dashboard admin
              ├─→ Monitorer les coûts IA
              ├─→ Voir les métriques d'usage
              └─→ Exporter les données
```

### Scénarios détaillés

#### UC1 : Analyser un repas
1. L'utilisateur se connecte à l'application
2. Il accède à l'écran "Nouvelle analyse"
3. Il décrit son repas (ex: "Pâtes carbonara, salade verte, coca")
4. Il valide l'analyse
5. L'IA traite la demande via OpenRouter
6. Les résultats s'affichent : calories, protéines, glucides, lipides
7. Des suggestions d'amélioration sont proposées
8. L'analyse est sauvegardée dans l'historique

#### UC2 : Consulter l'historique
1. L'utilisateur accède à la section "Historique"
2. Il voit la liste de ses analyses passées
3. Il peut filtrer par date
4. Il peut cliquer sur une analyse pour voir les détails
5. Il peut supprimer une analyse

---

## 3. Architecture Technique

### Stack technologique

**Frontend :**
- Flutter (Dart) - Mobile & Web
- Provider pour la gestion d'état
- Firebase SDK pour Flutter

**Backend :**
- Firebase Authentication (Email/Password)
- Cloud Firestore (base de données NoSQL)
- Firebase Cloud Functions (proxy API sécurisé)
- Firebase Hosting (version web)
- Firebase App Distribution (déploiement mobile)

**Intelligence Artificielle :**
- OpenRouter API
- Modèle IA : *À définir* (comparaison GPT-4, Claude, Llama, Mistral)
- Budget : 2$ maximum

**Déploiement :**
- Firebase Hosting (Web)
- Firebase App Distribution (Android APK)
- GitHub Actions (CI/CD)

### Schéma d'architecture

```
┌──────────────────────────────────────────────────┐
│              FLUTTER APPLICATION                 │
│  ┌────────────────────────────────────────────┐  │
│  │          Presentation Layer                │  │
│  │  (Screens: Auth, Home, Analysis, History) │  │
│  └────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────┐  │
│  │        Business Logic Layer                │  │
│  │     (Providers: Auth, Meal, User)          │  │
│  └────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────┐  │
│  │           Data Layer                       │  │
│  │  (Services: Auth, Database, AI, Storage)  │  │
│  └────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────┘
                       ↕
┌──────────────────────────────────────────────────┐
│              FIREBASE BACKEND                    │
│                                                  │
│  • Authentication (Email/Password)               │
│  • Cloud Firestore (Users, Meals, Analytics)    │
│  • Cloud Functions (analyzemeal, getStats)      │
│  • Hosting (Web deployment)                      │
│  • App Distribution (Mobile deployment)          │
└──────────────────────────────────────────────────┘
                       ↕
┌──────────────────────────────────────────────────┐
│            OPENROUTER API                        │
│                                                  │
│  • Endpoint: api.openrouter.ai/api/v1/chat      │
│  • Modèle: [À sélectionner]                     │
│  • Prompt engineering pour analyse nutritionnelle│
└──────────────────────────────────────────────────┘
```

---

## 4. Modèle de données (Firestore)

### Collection : `users`
```json
{
  "uid": "firebase_uid",
  "email": "user@example.com",
  "displayName": "John Doe",
  "createdAt": "timestamp",
  "subscription": "free",
  "dailyQuota": 10,
  "quotaUsed": 3
}
```

### Collection : `meals`
```json
{
  "id": "meal_id",
  "userId": "firebase_uid",
  "description": "Pâtes carbonara, salade verte",
  "analysis": {
    "calories": 650,
    "proteins": 25,
    "carbs": 70,
    "fats": 28,
    "suggestions": ["Réduire la portion...", "Ajouter des légumes..."]
  },
  "timestamp": "timestamp",
  "modelUsed": "gpt-4",
  "tokensCost": 1250
}
```

### Collection : `admin_metrics`
```json
{
  "date": "2025-11-09",
  "totalCosts": 0.45,
  "totalRequests": 120,
  "totalTokens": 45000,
  "modelBreakdown": {
    "gpt-4": { "requests": 50, "cost": 0.30 },
    "llama-3": { "requests": 70, "cost": 0.15 }
  }
}
```

---

## 5. Justification du choix du modèle IA

### Comparaison des modèles (OpenRouter)

*À compléter après tests - Semaine 2*

| Modèle | Coût/1M tokens | Performance | Pertinence |
|--------|----------------|-------------|------------|
| GPT-4 | $$$ | ⭐⭐⭐⭐⭐ | TBD |
| Claude 3 | $$$ | ⭐⭐⭐⭐⭐ | TBD |
| Llama 3.1 | $ | ⭐⭐⭐⭐ | TBD |
| Mistral | $ | ⭐⭐⭐ | TBD |

### Critères de sélection
1. **Précision nutritionnelle** : capacité à estimer correctement les valeurs
2. **Coût par requête** : respect du budget 2$
3. **Latence** : temps de réponse acceptable (<5s)
4. **Qualité des suggestions** : pertinence des conseils

---

## 6. Dashboard Monitoring des Coûts

### Fonctionnalités requises
- Coût total consommé (sur 2$)
- Nombre de requêtes par jour/semaine
- Répartition par modèle IA
- Tokens utilisés (input/output)
- Coût moyen par requête
- Graphiques d'évolution

*Screenshots à ajouter en Semaine 3-4*

---

## 7. Stratégie de Pricing

### Paliers tarifaires (basés sur coûts réels)

*À finaliser après observation des coûts réels - Semaine 4-5*

#### 🆓 Plan Gratuit
- 10 analyses par jour
- Historique 7 jours
- Suggestions de base

#### 💎 Plan Pro - 9,99€/mois
- 500 analyses par jour
- Historique illimité
- Suggestions détaillées
- Export PDF
- Support prioritaire

#### 🏢 Plan Premium - 19,99€/mois
- Analyses illimitées
- Analyse photo de repas (future feature)
- Coach IA personnalisé
- API access
- Support 24/7

### Calcul de la marge
*À compléter avec données réelles*

---

## 8. Conformité Légale

### 🔒 RGPD
- [ ] Politique de confidentialité rédigée
- [ ] Collecte minimale de données
- [ ] Droit à l'oubli implémenté (suppression compte)
- [ ] Consentement explicite lors de l'inscription
- [ ] Chiffrement des données sensibles

### 🤖 AI Act (Réglementation européenne)
- [ ] Transparence sur l'utilisation de l'IA
- [ ] Disclaimer visible : "Analyse générée par IA"
- [ ] Limitations clairement indiquées
- [ ] Classification du risque : **Risque limité** (information nutritionnelle)

### ⚖️ Mentions Légales
- [ ] Identité de l'éditeur
- [ ] Coordonnées de contact
- [ ] Hébergeur (Firebase/Google)
- [ ] Responsable de publication

### 🍪 Cookies & Tracking
- [ ] Bannière de consentement (si analytics utilisés)
- [ ] Liste des cookies utilisés
- [ ] Possibilité de refuser

### ⚠️ Disclaimer Médical
**Visible sur toutes les pages d'analyse :**
> "Cette application fournit des informations nutritionnelles à titre indicatif uniquement. Elle ne remplace pas l'avis d'un médecin, nutritionniste ou diététicien. Consultez un professionnel de santé pour tout conseil médical personnalisé."

---

## 9. MVP - Fonctionnalités Minimales (Obligatoires)

### ✅ Semaine 1-2
- [x] Authentification (email/password)
- [ ] Gestion utilisateurs (Firestore)
- [ ] Interface de base (navigation)

### ✅ Semaine 3
- [ ] Analyse de repas par texte
- [ ] Intégration OpenRouter fonctionnelle
- [ ] Affichage des résultats

### ✅ Semaine 4
- [ ] Historique des analyses
- [ ] Dashboard admin (monitoring coûts)
- [ ] Optimisation des prompts

### ✅ Semaine 5
- [ ] Landing page
- [ ] Page pricing
- [ ] Conformité légale de base

### ✅ Semaine 6-7
- [ ] CI/CD avec GitHub Actions
- [ ] Déploiement production (Web + Mobile)
- [ ] Tests et debugging

### ✅ Semaine 8
- [ ] Polish UX
- [ ] Documentation finale
- [ ] Rapport PDF complet

---

## 10. Planning Détaillé

| Semaine | Dates | Objectifs | Livrables |
|---------|-------|-----------|-----------|
| **S1** | 9-15 nov | Organisation, choix stack, auth basique | CDC v0, Suivi S1 |
| **S2** | 16-22 nov | Intégration OpenRouter, premiers appels API | Analyse fonctionnelle |
| **S3** | 23-29 nov | CI/CD, fonctionnalité IA core MVP, dashboard monitoring | Dashboard admin |
| **S4** | 30 nov-6 déc | Optimisation prompts, gestion erreurs robuste, caching | Suivi coûts optimisé |
| **S5** | 7-13 déc | Landing page + pricing | Pages publiques |
| **S6** | 14-20 déc | Fonctionnalités optionnelles, polish UX | App finalisée |
| **S7** | 21-27 déc | Finitions, rapport PDF final, démo fluide | Rapport final |
| **S8** | 28 déc-3 jan | Buffer, tests finaux | Livraison |

**Deadline :** 4 janvier 2026, 23h59

---

## 11. Risques & Mitigation

| Risque | Impact | Probabilité | Mitigation |
|--------|--------|-------------|------------|
| Dépassement budget OpenRouter | ⚠️ Haut | Moyenne | Dashboard monitoring temps réel, caching, quotas |
| Modèle IA imprécis | ⚠️ Moyen | Faible | Tests comparatifs, prompts optimisés |
| Problèmes Firebase | ⚠️ Moyen | Faible | Documentation officielle, backup plan |
| Retard planning | ⚠️ Moyen | Moyenne | Focus MVP, fonctionnalités optionnelles en S6 |
| Complexité CI/CD | ⚠️ Faible | Faible | GitHub Actions templates existants |

---

## 12. Technologies & Dépendances

### Packages Flutter principaux
```yaml
dependencies:
  firebase_core: ^latest
  firebase_auth: ^latest
  cloud_firestore: ^latest
  cloud_functions: ^latest
  provider: ^latest
  http: ^latest
  intl: ^latest
  cached_network_image: ^latest
```

### Services externes
- **Firebase** (gratuit avec limitations)
- **OpenRouter** (2$ de crédit)
- **GitHub** (repo + Actions)

---

**Dernière mise à jour :** 9 novembre 2025  
**Version :** 0.1 (Draft initial)

