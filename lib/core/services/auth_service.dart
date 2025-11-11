import 'package:firebase_auth/firebase_auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import '../../models/user_model.dart';

/// Service gérant l'authentification Firebase
class AuthService {
  final FirebaseAuth _auth = FirebaseAuth.instance;
  final FirebaseFirestore _firestore = FirebaseFirestore.instance;

  /// Stream de l'utilisateur connecté
  Stream<User?> get authStateChanges => _auth.authStateChanges();

  /// Utilisateur actuellement connecté
  User? get currentUser => _auth.currentUser;

  /// Inscription avec email et mot de passe
  Future<UserModel?> signUpWithEmail({
    required String email,
    required String password,
    required String displayName,
  }) async {
    try {
      // Créer le compte Firebase Auth
      final UserCredential userCredential =
          await _auth.createUserWithEmailAndPassword(
        email: email,
        password: password,
      );

      final User? user = userCredential.user;
      if (user == null) return null;

      // Mettre à jour le displayName
      await user.updateProfile(displayName: displayName);

      // Créer le document utilisateur dans Firestore
      final DateTime now = DateTime.now();
      final DateTime quotaResetDate =
          DateTime(now.year, now.month, now.day + 1); // Reset demain

      final UserModel userModel = UserModel(
        uid: user.uid,
        email: email,
        displayName: displayName,
        createdAt: now,
        lastLoginAt: now,
        subscription: 'free',
        dailyQuota: 10,
        quotaUsed: 0,
        quotaResetDate: quotaResetDate,
      );

      await _firestore
          .collection('users')
          .doc(user.uid)
          .set(userModel.toMap());

      return userModel;
    } on FirebaseAuthException catch (e) {
      throw _handleAuthException(e);
    } catch (e) {
      throw 'Erreur lors de l\'inscription: $e';
    }
  }

  /// Connexion avec email et mot de passe
  Future<UserModel?> signInWithEmail({
    required String email,
    required String password,
  }) async {
    try {
      final UserCredential userCredential =
          await _auth.signInWithEmailAndPassword(
        email: email,
        password: password,
      );

      final User? user = userCredential.user;
      if (user == null) return null;

      // Mettre à jour la dernière connexion
      await _firestore.collection('users').doc(user.uid).update({
        'lastLoginAt': Timestamp.fromDate(DateTime.now()),
      });

      // Récupérer les données utilisateur depuis Firestore
      final DocumentSnapshot doc =
          await _firestore.collection('users').doc(user.uid).get();

      if (!doc.exists) return null;

      return UserModel.fromFirestore(doc);
    } on FirebaseAuthException catch (e) {
      throw _handleAuthException(e);
    } catch (e) {
      throw 'Erreur lors de la connexion: $e';
    }
  }

  /// Déconnexion
  Future<void> signOut() async {
    try {
      await _auth.signOut();
    } catch (e) {
      throw 'Erreur lors de la déconnexion: $e';
    }
  }

  /// Réinitialisation du mot de passe
  Future<void> resetPassword(String email) async {
    try {
      await _auth.sendPasswordResetEmail(email: email);
    } on FirebaseAuthException catch (e) {
      throw _handleAuthException(e);
    } catch (e) {
      throw 'Erreur lors de la réinitialisation: $e';
    }
  }

  /// Récupérer les données utilisateur depuis Firestore
  Future<UserModel?> getUserData(String uid) async {
    try {
      final DocumentSnapshot doc =
          await _firestore.collection('users').doc(uid).get();

      if (!doc.exists) return null;

      return UserModel.fromFirestore(doc);
    } catch (e) {
      throw 'Erreur lors de la récupération des données: $e';
    }
  }

  /// Gérer les erreurs Firebase Auth
  String _handleAuthException(FirebaseAuthException e) {
    switch (e.code) {
      case 'weak-password':
        return 'Le mot de passe est trop faible.';
      case 'email-already-in-use':
        return 'Cet email est déjà utilisé.';
      case 'user-not-found':
        return 'Aucun utilisateur trouvé avec cet email.';
      case 'wrong-password':
        return 'Mot de passe incorrect.';
      case 'invalid-email':
        return 'Email invalide.';
      case 'user-disabled':
        return 'Ce compte a été désactivé.';
      case 'too-many-requests':
        return 'Trop de tentatives. Réessayez plus tard.';
      default:
        return 'Erreur d\'authentification: ${e.message}';
    }
  }
}

