# 📱 Guide de Génération APK - NutriAI

## Générer l'APK pour installer sur votre téléphone

### Méthode 1 : Via Android Studio (Recommandé)

1. **Ouvrir Android Studio**
   - Ouvrir le projet `android_app/`

2. **Build → Generate Signed Bundle / APK**
   - Menu : `Build` → `Generate Signed Bundle / APK`
   - Sélectionner **APK** (pas Bundle)
   - Cliquer **Next**

3. **Créer une clé de signature** (si première fois)
   - Cliquer **Create new...**
   - Remplir le formulaire :
     - **Key store path** : Choisir un emplacement (ex: `nutriai.jks`)
     - **Password** : Créer un mot de passe (notez-le !)
     - **Key alias** : `nutriai`
     - **Key password** : Même mot de passe
     - Informations : Votre nom, organisation, etc.
   - Cliquer **OK**

4. **Sélectionner la clé existante** (si déjà créée)
   - Sélectionner votre fichier `.jks`
   - Entrer les mots de passe
   - Cliquer **Next**

5. **Choisir le type de build**
   - Sélectionner **release**
   - Cliquer **Finish**

6. **Récupérer l'APK**
   - Une fois terminé, Android Studio affichera un message
   - Cliquer **locate** pour ouvrir le dossier
   - L'APK sera dans : `android_app/app/release/app-release.apk`

7. **Installer sur votre téléphone**
   - Transférer l'APK sur votre téléphone (USB, email, cloud, etc.)
   - Sur Android, autoriser l'installation depuis "Sources inconnues"
   - Ouvrir l'APK et installer

---

### Méthode 2 : Via ligne de commande (Plus rapide)

```bash
cd android_app

# Générer l'APK release (non signé pour test)
./gradlew assembleRelease

# L'APK sera dans :
# android_app/app/build/outputs/apk/release/app-release.apk
```

**Pour Windows PowerShell :**
```powershell
cd android_app
.\gradlew.bat assembleRelease
```

**Note :** Cet APK ne sera pas signé. Pour l'installer sur votre téléphone, vous devrez autoriser "Sources inconnues" dans les paramètres Android.

---

### Méthode 3 : APK Debug (Pour test rapide)

```bash
cd android_app
./gradlew assembleDebug

# L'APK sera dans :
# android_app/app/build/outputs/apk/debug/app-debug.apk
```

**Avantages :**
- Plus rapide à générer
- Pas besoin de signature
- Parfait pour tester

**Inconvénients :**
- Plus lourd
- Moins optimisé
- Affiche "Debug" dans certaines interfaces

---

## Installation sur téléphone Android

### Étape 1 : Transférer l'APK

**Option A : USB**
1. Connecter votre téléphone en USB
2. Activer le mode "Transfert de fichiers"
3. Copier l'APK dans le dossier Downloads du téléphone

**Option B : Email/Cloud**
1. Envoyer l'APK par email à vous-même
2. Ou uploader sur Google Drive / Dropbox
3. Télécharger sur le téléphone

**Option C : ADB (si développeur)**
```bash
adb install app-release.apk
```

### Étape 2 : Autoriser l'installation

1. Sur votre téléphone, aller dans **Paramètres**
2. **Sécurité** → **Sources inconnues** (ou **Installation d'applications**)
3. Autoriser l'installation depuis cette source

### Étape 3 : Installer

1. Ouvrir le fichier APK téléchargé
2. Cliquer **Installer**
3. Attendre la fin de l'installation
4. Ouvrir l'app depuis le menu d'applications

---

## Pour la présentation

### Recommandations

1. **Générer l'APK signé** (méthode 1) pour un rendu professionnel
2. **Tester sur votre téléphone** avant la présentation
3. **Vérifier que l'app se connecte** à l'API en production
4. **Préparer un backup** : garder l'APK sur votre ordinateur et cloud

### Checklist avant présentation

- [ ] APK généré et testé
- [ ] App installée sur votre téléphone
- [ ] Connexion à l'API testée
- [ ] Analyse de repas fonctionnelle
- [ ] Historique fonctionnel
- [ ] Dashboard admin accessible avec mot de passe

---

## Mot de passe Admin par défaut

Le mot de passe admin par défaut est : `admin123`

**⚠️ Important :** Changez-le en production en modifiant la variable d'environnement `ADMIN_PASSWORD` sur Render.

---

## Dépannage

### Erreur : "APK non signé"
- Utiliser la méthode 1 (signature via Android Studio)
- Ou autoriser "Sources inconnues" sur Android

### Erreur : "App ne se connecte pas"
- Vérifier que l'URL dans `RetrofitClient.kt` est correcte
- Vérifier que votre téléphone a Internet
- Vérifier que le backend Render est actif

### Erreur : "Installation bloquée"
- Aller dans Paramètres → Sécurité
- Autoriser l'installation depuis "Sources inconnues"

---

**C'est tout ! Vous êtes prêt pour la présentation ! 🎉**



