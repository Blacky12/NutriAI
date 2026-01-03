# 🚀 Guide de Configuration - NutriAI

## ⚡ Configuration Rapide (5 minutes)

### 1️⃣ Backend (2 min)

```bash
cd backend

# Créer le fichier .env
echo DEBUG=True > .env
echo DATABASE_URL=postgresql://postgres:VOTRE_MDP@localhost:5432/nutriai_db >> .env
echo OPENROUTER_API_KEY=sk-or-v1-VOTRE_CLE >> .env

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
```

**Remplacez :**
- `VOTRE_MOT_DE_PASSE` → Votre mot de passe PostgreSQL
- `VOTRE_CLE_API_ICI` → Votre clé OpenRouter

---

**C'est tout ! Vous êtes prêt ! 🎉**

