import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../core/services/auth_service.dart';
import '../core/services/database_service.dart';
import '../models/user_model.dart';

/// Provider gérant l'état d'authentification
class AuthProvider with ChangeNotifier {
  final AuthService _authService = AuthService();
  final DatabaseService _databaseService = DatabaseService();

  UserModel? _currentUser;
  bool _isLoading = false;
  String? _errorMessage;

  // Getters
  UserModel? get currentUser => _currentUser;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;
  bool get isAuthenticated => _currentUser != null;

  /// Stream de l'état d'authentification
  Stream<User?> get authStateChanges => _authService.authStateChanges;

  /// Initialiser le provider avec l'utilisateur connecté
  Future<void> initialize() async {
    final User? firebaseUser = _authService.currentUser;
    if (firebaseUser != null) {
      await loadUserData(firebaseUser.uid);
    }
  }

  /// Charger les données utilisateur depuis Firestore
  Future<void> loadUserData(String uid) async {
    try {
      _isLoading = true;
      notifyListeners();

      _currentUser = await _databaseService.getUser(uid);
      _errorMessage = null;
    } catch (e) {
      _errorMessage = e.toString();
      _currentUser = null;
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  /// Inscription
  Future<bool> signUp({
    required String email,
    required String password,
    required String displayName,
  }) async {
    try {
      _isLoading = true;
      _errorMessage = null;
      notifyListeners();

      _currentUser = await _authService.signUpWithEmail(
        email: email,
        password: password,
        displayName: displayName,
      );

      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _errorMessage = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  /// Connexion
  Future<bool> signIn({
    required String email,
    required String password,
  }) async {
    try {
      _isLoading = true;
      _errorMessage = null;
      notifyListeners();

      _currentUser = await _authService.signInWithEmail(
        email: email,
        password: password,
      );

      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _errorMessage = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  /// Déconnexion
  Future<void> signOut() async {
    try {
      await _authService.signOut();
      _currentUser = null;
      _errorMessage = null;
      notifyListeners();
    } catch (e) {
      _errorMessage = e.toString();
      notifyListeners();
    }
  }

  /// Réinitialiser le mot de passe
  Future<bool> resetPassword(String email) async {
    try {
      _isLoading = true;
      _errorMessage = null;
      notifyListeners();

      await _authService.resetPassword(email);

      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _errorMessage = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  /// Rafraîchir les données utilisateur
  Future<void> refreshUserData() async {
    if (_currentUser != null) {
      await loadUserData(_currentUser!.uid);
    }
  }

  /// Incrémenter le quota utilisé
  Future<void> incrementQuota() async {
    if (_currentUser != null) {
      await _databaseService.incrementQuotaUsed(_currentUser!.uid);
      await refreshUserData();
    }
  }

  /// Vérifier si le quota est dépassé
  bool hasReachedQuota() {
    return _currentUser?.hasReachedQuota() ?? true;
  }

  /// Effacer le message d'erreur
  void clearError() {
    _errorMessage = null;
    notifyListeners();
  }
}

