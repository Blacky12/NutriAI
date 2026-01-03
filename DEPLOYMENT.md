# 🚀 Guide de Déploiement - NutriAI

## Déploiement Backend sur Render

### 1. Préparer le projet

1. Créer un fichier `render.yaml` à la racine du projet :

```yaml
services:
  - type: web
    name: nutriai-backend
    env: python
    buildCommand: pip install -r backend/requirements.txt
    startCommand: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        sync: false
      - key: OPENROUTER_API_KEY
        sync: false
      - key: DEBUG
        value: False
```

2. Créer un fichier `Procfile` dans `backend/` :

```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 2. Créer la base de données PostgreSQL sur Render

1. Aller sur [Render Dashboard](https://dashboard.render.com)
2. Cliquer "New +" → "PostgreSQL"
3. Remplir le formulaire :
   - **Name** : `nutriai-db`
   - **Database** : `nutriai_db` (ou laissez par défaut)
   - **Region** : Choisir la région la plus proche (ex: `Frankfurt` pour l'Europe)
   - **PostgreSQL Version** : `16` (ou la plus récente)
   - **Plan** : Free (pour test)
4. Cliquer "Create Database"
5. ⏳ Attendre 2-3 minutes que la base soit créée
6. Une fois créée, cliquer sur votre base de données `nutriai-db`
7. Dans l'onglet **"Connections"**, copier l'**Internal Database URL** (format : `postgresql://user:password@host:5432/dbname`)
   - ⚠️ Utilisez l'**Internal Database URL**, pas l'External !

### 3. Déployer le Backend

1. Aller sur [Render Dashboard](https://dashboard.render.com)
2. Cliquer "New +" → "Web Service"
3. Connecter votre repo GitHub :
   - Cliquer "Connect account" si nécessaire
   - Autoriser Render à accéder à votre GitHub
   - Sélectionner le repo : `Blacky12/NutriAI`
   - Cliquer "Connect"

4. Configuration du service :
   - **Name** : `nutriai-backend`
   - **Region** : Même région que votre base de données (ex: `Frankfurt`)
   - **Branch** : `develop` (ou `main`)
   - **Root Directory** : `backend` ⚠️ **Important !**
   - **Environment** : `Python 3`
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

5. Variables d'environnement (cliquer "Advanced" → "Add Environment Variable") :
   - `DATABASE_URL` : L'**Internal Database URL** de l'étape 2
   - `OPENROUTER_API_KEY` : Votre clé API OpenRouter
   - `DEBUG` : `False`
   - `CORS_ORIGINS` : `*` (permet toutes les origines pour l'app Android)

6. Cliquer "Create Web Service"
7. ⏳ Attendre 5-10 minutes que le déploiement se termine
8. Une fois terminé, copier l'URL générée (ex: `https://nutriai-backend.onrender.com`)

### 4. Mettre à jour l'App Android

Dans `android_app/app/src/main/java/com/nutriai/app/data/api/RetrofitClient.kt` :

```kotlin
// Pour production
private const val BASE_URL = "https://nutriai-backend.onrender.com/"

// Pour développement local
// private const val BASE_URL = "http://10.0.2.2:8000/"
```

### 5. Tester

1. Attendre que le déploiement soit terminé (5-10 min)
2. Tester l'API : `https://votre-app.onrender.com/health`
3. Tester le dashboard : `https://votre-app.onrender.com/admin`
4. Tester la landing : `https://votre-app.onrender.com/`

---

## Déploiement Backend sur Railway

### Alternative à Render

1. Aller sur [Railway](https://railway.app)
2. "New Project" → "Deploy from GitHub repo"
3. Sélectionner votre repo
4. Railway détecte automatiquement Python
5. Ajouter les variables d'environnement :
   - `DATABASE_URL` : Créer une base PostgreSQL dans Railway
   - `OPENROUTER_API_KEY` : Votre clé
   - `DEBUG` : `False`
6. Railway génère automatiquement une URL publique

---

## URLs de Production

Une fois déployé, vous aurez :
- **API** : `https://votre-app.onrender.com/api/v1/meals/analyze`
- **Dashboard Admin** : `https://votre-app.onrender.com/admin`
- **Landing Page** : `https://votre-app.onrender.com/`
- **Pricing** : `https://votre-app.onrender.com/pricing`
- **Mentions Légales** : `https://votre-app.onrender.com/legal`

---

## Notes Importantes

- ⚠️ **Sleep Mode** : Le plan gratuit de Render met le service en veille après 15 minutes d'inactivité
- ⚠️ **Cold Start** : La première requête après le sleep peut prendre 30-60 secondes
- 💡 **Astuce** : Pour la démo, faites une requête toutes les 10 minutes pour garder le service actif
- ✅ Pour la production réelle, considérer un plan payant ($7/mois) pour de meilleures performances
- ✅ Configurer un domaine personnalisé si nécessaire

## Dépannage

### Erreur : "Database connection failed"
- Vérifier que `DATABASE_URL` utilise l'**Internal Database URL** (pas External)
- Vérifier que la base PostgreSQL est active
- Vérifier les credentials

### Erreur : "Module not found"
- Vérifier que `Root Directory` est bien `backend`
- Vérifier que `requirements.txt` contient tous les packages

### Erreur : "CORS blocked"
- Vérifier que `CORS_ORIGINS` contient `*` dans les variables d'environnement
- Redéployer le service après modification

### L'app Android ne se connecte pas
- Vérifier que l'URL dans `RetrofitClient.kt` est correcte (avec `https://`)
- Vérifier que l'appareil/émulateur a accès à Internet
- Consulter les logs Android Studio pour les erreurs réseau

---

## Génération APK Android

```bash
cd android_app
./gradlew assembleRelease
```

L'APK sera dans : `app/build/outputs/apk/release/app-release.apk`

Pour signer l'APK, voir la documentation Android officielle.


