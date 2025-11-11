# 🔑 Configuration OpenRouter - Guide complet

## Qu'est-ce qu'OpenRouter ?

OpenRouter est une **passerelle unifiée** pour accéder à plusieurs modèles d'IA (GPT-4, Claude, Llama, Mistral, etc.) avec **une seule API**. C'est parfait pour notre projet car :

✅ Un seul compte pour tous les modèles  
✅ Facturation transparente au token près  
✅ Dashboard de monitoring intégré  
✅ Prix souvent plus bas que les API directes  
✅ Pas besoin de multiple comptes (OpenAI, Anthropic, etc.)

---

## 🚀 Étapes pour créer votre compte

### 1. Créer un compte OpenRouter

1. Allez sur : **https://openrouter.ai/**
2. Cliquez sur **"Sign Up"** ou **"Get Started"**
3. Créez un compte avec :
   - Email
   - Google OAuth
   - GitHub OAuth (recommandé pour développeurs)

### 2. Ajouter du crédit

1. Une fois connecté, allez dans **"Settings"** → **"Credits"**
2. Cliquez sur **"Add Credits"**
3. Ajoutez **2$** (le budget alloué pour votre projet)
   - Carte bancaire acceptée
   - Minimum généralement 5$ (vous pouvez mettre plus si vous voulez)

💡 **Astuce :** OpenRouter offre parfois des crédits gratuits pour les nouveaux utilisateurs !

### 3. Créer une clé API

1. Allez dans **"Keys"** dans le menu
2. Cliquez sur **"Create Key"**
3. Donnez un nom à votre clé : `NutriAI-Dev`
4. **Copiez la clé immédiatement** (elle ne sera plus visible après)
5. Format : `sk-or-v1-xxxxxxxxxxxxx...`

⚠️ **IMPORTANT :** Ne JAMAIS partager ou commit cette clé dans Git !

---

## 🔐 Stocker la clé de manière sécurisée

### Pour le développement local

Créez un fichier `.env` à la racine du projet (sera ignoré par Git) :

```bash
# .env
OPENROUTER_API_KEY=sk-or-v1-votre-clé-ici
```

Puis ajoutez `.env` à votre `.gitignore` :

```bash
# .gitignore
.env
.env.local
*.env
```

### Pour Firebase Cloud Functions

Les clés API doivent être stockées dans les **variables d'environnement Firebase** :

```bash
# Dans le terminal, à la racine du projet
firebase functions:config:set openrouter.key="sk-or-v1-votre-clé-ici"
```

Puis dans votre Cloud Function :

```javascript
const functions = require('firebase-functions');
const OPENROUTER_API_KEY = functions.config().openrouter.key;
```

### Pour GitHub Actions (CI/CD)

1. Allez dans votre repo GitHub
2. **Settings** → **Secrets and variables** → **Actions**
3. Cliquez sur **"New repository secret"**
4. Nom : `OPENROUTER_API_KEY`
5. Valeur : votre clé API

---

## 📊 Dashboard de monitoring

OpenRouter fournit un dashboard natif pour suivre vos coûts :

### Accéder au dashboard
1. Connectez-vous à https://openrouter.ai/
2. Allez dans **"Activity"** ou **"Usage"**

### Métriques disponibles
- 💰 **Coûts en temps réel** (par requête)
- 🔢 **Tokens utilisés** (input + output)
- 📈 **Graphiques d'évolution** (jour/semaine/mois)
- 🤖 **Répartition par modèle** (quel modèle coûte le plus)
- ⏱️ **Latence moyenne** des requêtes

💡 **Conseil :** Vérifiez ce dashboard quotidiennement pour éviter les surprises !

---

## 🎯 Choisir le bon modèle

Voici un comparatif des modèles disponibles sur OpenRouter (prix indicatifs) :

### Pour l'analyse nutritionnelle (texte)

| Modèle | Prix/1M tokens (input) | Prix/1M tokens (output) | Performance | Recommandation |
|--------|------------------------|-------------------------|-------------|----------------|
| **GPT-4 Turbo** | ~10$ | ~30$ | ⭐⭐⭐⭐⭐ | ✅ Meilleur qualité |
| **GPT-3.5 Turbo** | ~0.50$ | ~1.50$ | ⭐⭐⭐⭐ | ✅ Bon rapport qualité/prix |
| **Claude 3 Haiku** | ~0.25$ | ~1.25$ | ⭐⭐⭐⭐ | ✅ Rapide et économique |
| **Llama 3.1 70B** | ~0.50$ | ~0.75$ | ⭐⭐⭐⭐ | ✅ Excellent choix |
| **Mistral Large** | ~2$ | ~6$ | ⭐⭐⭐⭐ | ⚠️ Moyen, plus cher |

### Estimation de coûts pour 2$ de budget

Avec **Llama 3.1 70B** (recommandé) :
- Prix moyen : ~0.60$ / 1M tokens
- Analyse type : ~500 tokens (input + output)
- **Nombre d'analyses possibles : ~6600** 🎉

Avec **GPT-3.5 Turbo** :
- Prix moyen : ~1$ / 1M tokens
- Analyse type : ~500 tokens
- **Nombre d'analyses possibles : ~4000** 👍

Avec **GPT-4 Turbo** :
- Prix moyen : ~20$ / 1M tokens
- Analyse type : ~500 tokens
- **Nombre d'analyses possibles : ~200** ⚠️

### 🏆 Recommandation pour le MVP

**Commencez avec GPT-3.5 Turbo** :
- Excellent compromis qualité/prix
- Largement testé et fiable
- Budget suffisant pour développer et tester
- Possibilité de passer à Llama 3.1 ensuite pour économiser

---

## 🧪 Tester l'API OpenRouter

### Option 1 : Avec cURL (terminal)

```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-or-v1-votre-clé" \
  -d '{
    "model": "openai/gpt-3.5-turbo",
    "messages": [
      {
        "role": "user",
        "content": "Analyse nutritionnelle de : poulet grillé avec riz blanc"
      }
    ]
  }'
```

### Option 2 : Avec Postman

1. Ouvrez Postman
2. **POST** : `https://openrouter.ai/api/v1/chat/completions`
3. **Headers** :
   - `Content-Type: application/json`
   - `Authorization: Bearer sk-or-v1-votre-clé`
4. **Body (JSON)** :
```json
{
  "model": "openai/gpt-3.5-turbo",
  "messages": [
    {
      "role": "user",
      "content": "Analyse ce repas et donne calories, protéines, glucides, lipides en JSON : Pâtes carbonara"
    }
  ]
}
```

### Option 3 : Playground OpenRouter

OpenRouter a un **playground intégré** :
1. Allez sur https://openrouter.ai/playground
2. Sélectionnez un modèle
3. Testez vos prompts en direct
4. Voyez les coûts en temps réel

---

## 📝 Exemple de prompt optimisé

Pour économiser des tokens, utilisez des prompts **courts et structurés** :

```
Analyse ce repas en JSON strict :
Repas : "{description}"

Format attendu :
{
  "calories": number,
  "proteins": number,
  "carbs": number,
  "fats": number,
  "suggestions": [string, string]
}
```

### Tokens approximatifs
- Prompt ci-dessus : ~80 tokens (input)
- Réponse JSON : ~120 tokens (output)
- **Total par analyse : ~200 tokens**

Avec GPT-3.5 Turbo ($1/1M tokens), ça coûte : **0.0002$** par analyse ! 🎉

---

## 🛡️ Bonnes pratiques de sécurité

### ❌ À NE JAMAIS FAIRE
```javascript
// MAUVAIS : Clé API exposée côté client (Flutter)
const API_KEY = "sk-or-v1-xxxxx"; // ⚠️ DANGEREUX !

http.post(
  'https://openrouter.ai/api/v1/chat/completions',
  headers: {'Authorization': 'Bearer $API_KEY'} // ❌ Exposé !
);
```

### ✅ BONNE PRATIQUE
```javascript
// BON : Appel via Cloud Function (backend sécurisé)
// Côté Flutter (client)
final result = await FirebaseFunctions.instance
    .httpsCallable('analyzeMeal')
    .call({'description': mealDescription});

// Côté Cloud Function (backend)
// La clé API reste sur le serveur, jamais exposée
const OPENROUTER_KEY = functions.config().openrouter.key;
```

---

## 🚨 Alertes et limites

### Configurer des alertes de budget

1. Dans OpenRouter, allez dans **"Settings"** → **"Limits"**
2. Définissez une **limite de dépense** : `2.00$`
3. Activez **email alert** à `1.50$` (75% du budget)

### Gérer les dépassements

Si vous atteignez la limite :
- L'API retournera une erreur `429 Too Many Requests`
- Votre app doit gérer cette erreur gracieusement
- Afficher : "Quota journalier atteint, réessayez demain"

---

## 📚 Ressources officielles

- **Documentation OpenRouter** : https://openrouter.ai/docs
- **Liste des modèles** : https://openrouter.ai/models
- **Pricing** : https://openrouter.ai/models (prix par modèle)
- **Playground** : https://openrouter.ai/playground
- **Discord communauté** : https://discord.gg/openrouter

---

## ✅ Checklist de configuration

- [ ] Compte OpenRouter créé
- [ ] 2$ de crédit ajouté
- [ ] Clé API générée et copiée
- [ ] Clé stockée dans `.env` (local)
- [ ] `.env` ajouté au `.gitignore`
- [ ] Test de l'API avec cURL ou Postman
- [ ] Modèle IA choisi (recommandation : GPT-3.5 Turbo)
- [ ] Limite de budget configurée (2$)
- [ ] Alerte email activée (1.50$)

---

**Prochaine étape :** Intégrer OpenRouter dans vos Firebase Cloud Functions ! 🚀

**Dernière mise à jour :** 9 novembre 2025

