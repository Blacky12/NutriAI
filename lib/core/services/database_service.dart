import 'package:cloud_firestore/cloud_firestore.dart';
import '../../models/user_model.dart';
import '../../models/meal_model.dart';

/// Service gérant les interactions avec Firestore
class DatabaseService {
  final FirebaseFirestore _firestore = FirebaseFirestore.instance;

  // ========== USERS ==========

  /// Récupérer un utilisateur
  Future<UserModel?> getUser(String uid) async {
    try {
      final doc = await _firestore.collection('users').doc(uid).get();
      if (!doc.exists) return null;
      return UserModel.fromFirestore(doc);
    } catch (e) {
      throw 'Erreur lors de la récupération de l\'utilisateur: $e';
    }
  }

  /// Mettre à jour un utilisateur
  Future<void> updateUser(String uid, Map<String, dynamic> data) async {
    try {
      await _firestore.collection('users').doc(uid).update(data);
    } catch (e) {
      throw 'Erreur lors de la mise à jour de l\'utilisateur: $e';
    }
  }

  /// Incrémenter le quota utilisé
  Future<void> incrementQuotaUsed(String uid) async {
    try {
      await _firestore.collection('users').doc(uid).update({
        'quotaUsed': FieldValue.increment(1),
      });
    } catch (e) {
      throw 'Erreur lors de l\'incrémentation du quota: $e';
    }
  }

  /// Réinitialiser le quota quotidien
  Future<void> resetDailyQuota(String uid) async {
    try {
      final now = DateTime.now();
      final tomorrow = DateTime(now.year, now.month, now.day + 1);

      await _firestore.collection('users').doc(uid).update({
        'quotaUsed': 0,
        'quotaResetDate': Timestamp.fromDate(tomorrow),
      });
    } catch (e) {
      throw 'Erreur lors de la réinitialisation du quota: $e';
    }
  }

  // ========== MEALS ==========

  /// Créer une nouvelle analyse de repas
  Future<String> createMeal(MealModel meal) async {
    try {
      final docRef = await _firestore.collection('meals').add(meal.toMap());
      return docRef.id;
    } catch (e) {
      throw 'Erreur lors de la sauvegarde du repas: $e';
    }
  }

  /// Récupérer l'historique des repas d'un utilisateur
  Stream<List<MealModel>> getUserMeals(String userId) {
    return _firestore
        .collection('meals')
        .where('userId', isEqualTo: userId)
        .orderBy('timestamp', descending: true)
        .snapshots()
        .map((snapshot) => snapshot.docs
            .map((doc) => MealModel.fromFirestore(doc))
            .toList());
  }

  /// Récupérer un repas spécifique
  Future<MealModel?> getMeal(String mealId) async {
    try {
      final doc = await _firestore.collection('meals').doc(mealId).get();
      if (!doc.exists) return null;
      return MealModel.fromFirestore(doc);
    } catch (e) {
      throw 'Erreur lors de la récupération du repas: $e';
    }
  }

  /// Supprimer un repas
  Future<void> deleteMeal(String mealId) async {
    try {
      await _firestore.collection('meals').doc(mealId).delete();
    } catch (e) {
      throw 'Erreur lors de la suppression du repas: $e';
    }
  }

  /// Obtenir les statistiques d'un utilisateur
  Future<Map<String, dynamic>> getUserStats(String userId) async {
    try {
      final QuerySnapshot snapshot = await _firestore
          .collection('meals')
          .where('userId', isEqualTo: userId)
          .get();

      if (snapshot.docs.isEmpty) {
        return {
          'totalMeals': 0,
          'averageCalories': 0.0,
          'totalCalories': 0.0,
        };
      }

      double totalCalories = 0;
      for (var doc in snapshot.docs) {
        final data = doc.data() as Map<String, dynamic>;
        final analysis = data['analysis'] as Map<String, dynamic>?;
        totalCalories += (analysis?['calories'] ?? 0).toDouble();
      }

      return {
        'totalMeals': snapshot.docs.length,
        'averageCalories': totalCalories / snapshot.docs.length,
        'totalCalories': totalCalories,
      };
    } catch (e) {
      throw 'Erreur lors de la récupération des statistiques: $e';
    }
  }

  // ========== ADMIN ==========

  /// Récupérer les métriques admin (pour le dashboard)
  Stream<QuerySnapshot> getAdminMetrics() {
    return _firestore
        .collection('admin_metrics')
        .orderBy('date', descending: true)
        .limit(30) // 30 derniers jours
        .snapshots();
  }

  /// Récupérer tous les utilisateurs (admin only)
  Stream<List<UserModel>> getAllUsers() {
    return _firestore
        .collection('users')
        .orderBy('createdAt', descending: true)
        .snapshots()
        .map((snapshot) =>
            snapshot.docs.map((doc) => UserModel.fromFirestore(doc)).toList());
  }
}

