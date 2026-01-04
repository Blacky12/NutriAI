# 🚀 Guide de Déploiement Render - NutriAI

## Problème : Render ne déploie pas automatiquement

### Cause probable

Render surveille généralement la branche `main`, mais vous avez pushé sur `develop`.

### Solutions

## Solution 1 : Merger develop vers main (Recommandé)

```bash
# 1. Passer sur main
git checkout main

# 2. Merger develop dans main
git merge develop

# 3. Pousser sur main
git push origin main
```

Render détectera automatiquement le push sur `main` et redéploiera.

---

## Solution 2 : Configurer Render pour surveiller develop

1. Aller sur [Render Dashboard](https://dashboard.render.com)
2. Cliquer sur votre service `nutriai-backend`
3. Aller dans **Settings** → **Build & Deploy**
4. Dans **Branch**, changer de `main` à `develop`
5. Cliquer **Save Changes**
6. Render redéploiera automatiquement

---

## Solution 3 : Redéploiement manuel (Rapide)

1. Aller sur [Render Dashboard](https://dashboard.render.com)
2. Cliquer sur votre service `nutriai-backend`
3. Cliquer sur le bouton **Manual Deploy** → **Deploy latest commit**
4. Render redéploiera le dernier commit de la branche surveillée

---

## Vérifier la configuration Render

### 1. Vérifier la branche surveillée

Dans Render Dashboard → Votre service → Settings → Build & Deploy :
- **Branch** : Doit être `main` ou `develop` selon votre workflow
- **Auto-Deploy** : Doit être activé (ON)

### 2. Vérifier la connexion GitHub

Dans Render Dashboard → Votre service → Settings → **Connected Repository** :
- ✅ Le repo GitHub doit être connecté
- ✅ Les permissions doivent être accordées

### 3. Vérifier les logs

Dans Render Dashboard → Votre service → **Logs** :
- Vérifier s'il y a des erreurs de build
- Vérifier le dernier déploiement

---

## Workflow recommandé

### Pour le développement :

```bash
# Travailler sur develop
git checkout develop
git add .
git commit -m "Vos modifications"
git push origin develop

# GitHub Actions vérifie le code (CI)
# ✅ Si tout est OK, merger vers main
```

### Pour déployer :

```bash
# Merger develop → main
git checkout main
git merge develop
git push origin main

# Render déploie automatiquement (CD)
```

---

## Vérifier que le déploiement fonctionne

1. **Attendre 2-5 minutes** après le push sur `main`
2. Aller sur Render Dashboard → Votre service
3. Vérifier l'onglet **Events** pour voir le déploiement en cours
4. Une fois terminé, tester : `https://nutriai-backend-htic.onrender.com/admin`

---

## Dépannage

### Render ne détecte pas les changements

1. Vérifier que **Auto-Deploy** est activé
2. Vérifier que la branche surveillée correspond à celle où vous poussez
3. Vérifier les permissions GitHub dans Render

### Le déploiement échoue

1. Consulter les **Logs** dans Render
2. Vérifier que `requirements.txt` est à jour
3. Vérifier que `Procfile` existe dans `backend/`
4. Vérifier que `render.yaml` est valide

### Le déploiement prend trop de temps

- Normal : Le premier déploiement peut prendre 5-10 minutes
- Les déploiements suivants : 2-5 minutes
- Si > 10 minutes : Vérifier les logs pour erreurs

---

## Configuration actuelle

- **Branche surveillée** : `main` (par défaut Render)
- **Auto-Deploy** : Activé (si configuré)
- **Build Command** : `pip install -r backend/requirements.txt`
- **Start Command** : `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

---

**Astuce** : Pour un workflow plus fluide, configurez Render pour surveiller `develop` et utilisez `main` uniquement pour les releases.

