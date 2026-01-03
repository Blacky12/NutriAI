# 🚀 Guide de Configuration - NutriAI

## ⚡ Configuration Rapide (5 minutes)

### 1️⃣ Backend (2 min)

```bash
cd backend

# Créer le fichier .env
echo DEBUG=True > .env
echo DATABASE_URL=postgresql://postgres:VOTRE_MDP@localhost:5432/nutriai_db >> .env
echo OPENROUTER_API_KEY=sk-or-v1-VOTRE_CLE >> .env
echo CLERK_SECRET_KEY=sk_test_VOTRE_CLE_SECRETE >> .env
echo CLERK_PUBLISHABLE_KEY=pk_test_VOTRE_CLE_PUBLIQUE >> .env

# Installer et lancer
pip install -r requirements.txt
uvicorn app.main:app --reload
```

✅ Backend accessible sur `http://localhost:8000`

**Test rapide :** Ouvrez `http://localhost:8000/health` dans votre navigateur

---

### 2️⃣ Base de données PostgreSQL

**Dans pgAdmin4 :**
1. Clic droit sur "Databases" → "Create" → "Database..."
2. Nom : `nutriai_db`
3. Owner : `postgres`
4. Cliquez "Save"

✅ Base créée !

---

### 3️⃣ Android App (3 min)

1. **Ouvrir dans Android Studio**
   - Ouvrir le dossier `android_app/`
   - Attendre la synchronisation Gradle

2. **Configurer l'URL** (si besoin)
   - Émulateur : `http://10.0.2.2:8000/` ✅ (déjà configuré)
   - Device physique : Modifier `RetrofitClient.kt` avec votre IP locale

3. **Lancer l'app**
   - Cliquez sur "Run" ▶️

✅ L'app démarre !

---

## 🧪 Test Complet

1. **Backend tourne** → Voir `✅ Backend OK: healthy` sur l'écran d'accueil
2. **Cliquer "Analyser un repas"**
3. **Taper** : "Poulet grillé avec riz et brocolis"
4. **Cliquer "Analyser"**
5. **Voir les résultats** nutritionnels ! 🎉

---

## ❌ Si ça ne marche pas

### Backend ne démarre pas
- ✅ Vérifier que PostgreSQL tourne
- ✅ Vérifier le fichier `.env` existe
- ✅ Vérifier que la base `nutriai_db` existe

### App ne se connecte pas
- ✅ Vérifier que le backend tourne (`http://localhost:8000/health`)
- ✅ Vérifier l'URL dans `RetrofitClient.kt`
- ✅ Pour device physique : Même WiFi + IP locale correcte

---

## 📝 Fichier .env à créer

Dans `backend/.env` :

```env
DEBUG=True
DATABASE_URL=postgresql://postgres:VOTRE_MOT_DE_PASSE@localhost:5432/nutriai_db
OPENROUTER_API_KEY=sk-or-v1-VOTRE_CLE_API_ICI
CLERK_SECRET_KEY=sk_test_VOTRE_CLE_CLERK_SECRETE
CLERK_PUBLISHABLE_KEY=pk_test_VOTRE_CLE_CLERK_PUBLIQUE
```

**Remplacez :**
- `VOTRE_MOT_DE_PASSE` → Votre mot de passe PostgreSQL
- `VOTRE_CLE_API_ICI` → Votre clé OpenRouter
- `VOTRE_CLE_CLERK_SECRETE` → Votre clé secrète Clerk (voir ci-dessous)
- `VOTRE_CLE_CLERK_PUBLIQUE` → Votre clé publique Clerk

**Note :** Si vous n'avez pas encore configuré Clerk, vous pouvez laisser ces lignes vides. L'application utilisera un utilisateur temporaire pour le développement.

---

## 🔐 Configuration Clerk (Optionnel pour développement local)

### Obtenir les clés Clerk

1. Créer un compte sur [clerk.com](https://clerk.com) (gratuit)
2. Créer une nouvelle application
3. Aller dans "API Keys"
4. Copier :
   - **Secret Key** → `CLERK_SECRET_KEY` (commence par `sk_test_`)
   - **Publishable Key** → `CLERK_PUBLISHABLE_KEY` (commence par `pk_test_`)

### Pour la production (Render)

Ajoutez ces variables dans les variables d'environnement Render :
- `CLERK_SECRET_KEY` : Votre clé secrète Clerk
- `CLERK_PUBLISHABLE_KEY` : Votre clé publique Clerk

---

**C'est tout ! Vous êtes prêt ! 🎉**

