# 📋 Cahier des Charges - NutriAI

**Projet :** Application IA-Driven (MVP)  
**Date :** Janvier 2026  
**Équipe :** Nicolas Ferbeck

---

## 1. Concept

### 1.1 Problème résolu

NutriAI résout le problème de l'analyse nutritionnelle rapide et accessible. Beaucoup de personnes souhaitent connaître les valeurs nutritionnelles de leurs repas mais :
- Les applications existantes nécessitent une saisie manuelle fastidieuse
- Les bases de données nutritionnelles sont incomplètes
- L'analyse prend du temps

**Solution :** Utiliser l'IA pour analyser une simple description textuelle d'un repas et obtenir instantanément les valeurs nutritionnelles complètes avec des suggestions d'amélioration.

### 1.2 Public cible

- **Primaire :** Personnes soucieuses de leur alimentation (18-45 ans)
- **Secondaire :** Sportifs, personnes suivant un régime, étudiants
- **Tertiaire :** Professionnels de la nutrition (outil de démonstration)

---

## 2. Acteurs & Use Cases

### 2.1 Acteurs

1. **Utilisateur Gratuit** : 10 analyses/jour
2. **Utilisateur Pro** : 500 analyses/jour
3. **Utilisateur Premium** : Analyses illimitées
4. **Administrateur** : Monitoring des coûts et statistiques

### 2.2 Use Cases Principaux

#### UC1 : Analyser un repas
- **Acteur :** Utilisateur
- **Précondition :** Compte créé et connecté
- **Scénario :**
  1. Utilisateur ouvre l'application
  2. Clique sur "Analyser un repas"
  3. Saisit la description du repas
  4. Clique sur "Analyser"
  5. Reçoit les valeurs nutritionnelles et suggestions
- **Postcondition :** Repas sauvegardé dans l'historique

#### UC2 : Consulter l'historique
- **Acteur :** Utilisateur
- **Scénario :**
  1. Utilisateur clique sur "Historique"
  2. Voit la liste de ses repas analysés
  3. Peut consulter les détails de chaque repas

#### UC3 : Monitorer les coûts (Admin)
- **Acteur :** Administrateur
- **Scénario :**
  1. Admin accède au dashboard
  2. Consulte les statistiques de coûts
  3. Analyse les graphiques d'utilisation
  4. Exporte les données si nécessaire

---

## 3. Justification du choix du modèle IA

### 3.1 Modèle choisi : GPT-3.5 Turbo via OpenRouter

**Raisons du choix :**

1. **Coût** : 
   - ~$0.0001-0.001 par analyse
   - Très économique pour un MVP
   - Permet une marge confortable sur les plans payants

2. **Performance** :
   - Excellente compréhension du langage naturel
   - Capacité à extraire des informations structurées
   - Génération de suggestions pertinentes

3. **Pertinence technique** :
   - API simple et fiable via OpenRouter
   - Support JSON dans les réponses
   - Latence acceptable (< 3 secondes)
   - Compatible avec notre stack (Python/FastAPI)

### 3.2 Alternatives considérées

- **GPT-4** : Trop cher pour un MVP (~10x plus cher)
- **Claude** : Bonne alternative mais moins de contrôle sur le format
- **Modèles spécialisés nutrition** : Non disponibles via OpenRouter

---

## 4. Architecture

### 4.1 Schéma Architecture

```
┌─────────────────┐
│  Android App   │
│  (Kotlin)       │
└────────┬────────┘
         │ HTTPS/REST
         │
┌────────▼────────┐
│   FastAPI       │
│   Backend       │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼────────┐
│PostgreSQL│ │ OpenRouter│
│ Database │ │   API     │
└─────────┘ └───────────┘
```

### 4.2 Stack Technique

| Composant | Technologie |
|-----------|------------|
| Frontend Mobile | Kotlin + Jetpack Compose |
| Backend API | FastAPI (Python) |
| Base de données | PostgreSQL |
| ORM | SQLAlchemy |
| IA | OpenRouter (GPT-3.5 Turbo) |
| Auth | Clerk (à implémenter) |
| Hébergement | Render / Railway |
| Distribution | APK Android |

### 4.3 Flux de données

1. **Analyse de repas :**
   ```
   Android → FastAPI → OpenRouter → Parsing JSON → PostgreSQL → Android
   ```

2. **Historique :**
   ```
   Android → FastAPI → PostgreSQL → Android
   ```

3. **Dashboard Admin :**
   ```
   Navigateur → FastAPI → PostgreSQL → Calcul stats → Graphiques
   ```

---

## 5. Diagramme UML de Classes

```
┌─────────────────┐
│      User       │
├─────────────────┤
│ - id: String    │
│ - email: String │
│ - quota: int    │
│ - tier: Enum    │
└────────┬────────┘
         │
         │ 1
         │
         │ *
┌────────▼────────┐
│      Meal       │
├─────────────────┤
│ - id: String    │
│ - user_id: FK   │
│ - description   │
│ - calories      │
│ - proteins      │
│ - carbs         │
│ - fats          │
│ - cost_usd      │
│ - tokens_used   │
│ - created_at    │
└─────────────────┘
```

---

## 6. Dashboard Monitoring Coûts

### 6.1 Captures d'écran

[À ajouter : Screenshots du dashboard]

### 6.2 Fonctionnalités

- **Statistiques globales :**
  - Total repas analysés
  - Total utilisateurs
  - Coût total en USD
  - Coût moyen par repas
  - Total tokens utilisés

- **Graphiques :**
  - Coûts par jour (7 derniers jours)
  - Nombre de repas par jour
  - Répartition par modèle IA utilisé

- **Actualisation :** Automatique toutes les 30 secondes

### 6.3 Accès

- URL : `https://votre-app.onrender.com/admin`
- Authentification : À implémenter (actuellement publique pour MVP)

---

## 7. Stratégie de Pricing

### 7.1 Plans proposés

| Plan | Prix | Quota | Caractéristiques |
|------|------|-------|------------------|
| **Gratuit** | 0€/mois | 10/jour | Fonctionnalités de base |
| **Pro** | 9.99€/mois | 500/jour | Priorité + Export |
| **Premium** | 19.99€/mois | Illimité | API + Support 24/7 |

### 7.2 Calcul de la marge

**Coût moyen par analyse :** ~$0.0005 (0.0005 USD)

**Calcul pour plan Gratuit :**
- 10 analyses/jour × 30 jours = 300 analyses/mois
- Coût : 300 × $0.0005 = $0.15/mois
- Marge : 0€ (service gratuit)

**Calcul pour plan Pro :**
- 500 analyses/jour × 30 jours = 15,000 analyses/mois
- Coût : 15,000 × $0.0005 = $7.50/mois
- Prix : 9.99€/mois (~$11)
- **Marge :** $3.50/mois (32% de marge)

**Calcul pour plan Premium :**
- Analyses illimitées (estimation : 50,000/mois)
- Coût : 50,000 × $0.0005 = $25/mois
- Prix : 19.99€/mois (~$22)
- **Marge :** -$3/mois (nécessite ajustement ou limite)

### 7.3 Recommandations

- Ajuster le plan Premium à 29.99€/mois pour une marge positive
- Ou limiter à 30,000 analyses/mois pour Premium
- Surveiller les coûts réels et ajuster si nécessaire

---

## 8. Conformité Légale

### 8.1 RGPD

✅ **Conformité réalisée :**
- Politique de confidentialité complète
- Gestion des droits utilisateurs (accès, rectification, suppression)
- Base légale du traitement (consentement, exécution contrat)
- Durée de conservation des données (3 ans)
- Mesures de sécurité (HTTPS, chiffrement)

### 8.2 AI Act

✅ **Conformité réalisée :**
- Information transparente sur l'utilisation de l'IA
- Modèle utilisé clairement indiqué (GPT-3.5 Turbo)
- Disclaimers médicaux présents
- Résultats présentés comme suggestions, pas avis médicaux

### 8.3 Mentions Légales

✅ **Pages créées :**
- Mentions légales complètes
- Politique de confidentialité
- Politique des cookies
- Informations sur l'éditeur et l'hébergement

### 8.4 Gestion des Cookies

✅ **Implémenté :**
- Information sur les cookies utilisés
- Tableau détaillé des cookies
- Instructions pour gérer les cookies
- Cookies strictement nécessaires identifiés

---

## 9. Présentation Finale

### 9.1 Captures d'écran

[À ajouter : Screenshots de l'application complète]

### 9.2 Parcours Utilisateur Type

**Scénario :** Utilisateur analyse son petit-déjeuner

1. **Ouverture de l'app** → Écran d'accueil avec statut de connexion
2. **Clic "Analyser un repas"** → Écran de saisie
3. **Saisie :** "2 œufs brouillés, 2 tranches de pain complet, beurre"
4. **Clic "Analyser"** → Chargement (2-3 secondes)
5. **Résultats affichés :**
   - Calories : 450 kcal
   - Protéines : 25g
   - Glucides : 35g
   - Lipides : 20g
   - Suggestions : "Ajouter des légumes pour plus de fibres"
6. **Retour au menu** → Historique mis à jour

### 9.3 Points Forts

- ✅ Interface intuitive et moderne
- ✅ Résultats instantanés (< 3 secondes)
- ✅ Analyse précise grâce à l'IA
- ✅ Suggestions pertinentes
- ✅ Historique complet
- ✅ Dashboard admin pour monitoring

---

## 10. CI/CD & Déploiement

### 10.1 Pipeline de Déploiement

**Actuellement :** Déploiement manuel sur Render/Railway

**Processus :**
1. Push sur GitHub (branche main)
2. Render détecte les changements
3. Build automatique (pip install)
4. Déploiement automatique
5. Tests de santé (health check)

### 10.2 Choix Techniques

**Pourquoi Render/Railway :**
- ✅ Déploiement simple et rapide
- ✅ Intégration GitHub native
- ✅ PostgreSQL inclus
- ✅ Plan gratuit pour MVP
- ✅ HTTPS automatique

**Alternatives considérées :**
- AWS/GCP : Trop complexe pour MVP
- Heroku : Plus cher, moins flexible
- VPS : Nécessite plus de configuration

### 10.3 Améliorations Futures

- [ ] Pipeline CI/CD complet (GitHub Actions)
- [ ] Tests automatisés
- [ ] Déploiement staging/production
- [ ] Monitoring avec Sentry
- [ ] Backup automatique de la DB

---

## 11. Conclusion

NutriAI est un MVP fonctionnel qui démontre l'intégration réussie de l'IA dans une application mobile. Le projet respecte les contraintes du cahier des charges avec :

- ✅ Intégration IA fonctionnelle
- ✅ Application mobile complète
- ✅ Dashboard admin opérationnel
- ✅ Conformité légale de base
- ✅ Documentation complète

**Prochaines étapes :**
- Déploiement en production
- Tests utilisateurs
- Amélioration de l'authentification
- Optimisation des coûts IA

---

**Date de rédaction :** 2 janvier 2026  
**Version :** 1.0


