import 'package:cloud_firestore/cloud_firestore.dart';

/// Modèle représentant un utilisateur
class UserModel {
  final String uid;
  final String email;
  final String displayName;
  final DateTime createdAt;
  final DateTime? lastLoginAt;
  final String subscription; // 'free', 'pro', 'premium'
  final int dailyQuota;
  final int quotaUsed;
  final DateTime quotaResetDate;

  UserModel({
    required this.uid,
    required this.email,
    required this.displayName,
    required this.createdAt,
    this.lastLoginAt,
    this.subscription = 'free',
    this.dailyQuota = 10,
    this.quotaUsed = 0,
    required this.quotaResetDate,
  });

  /// Créer un UserModel depuis un document Firestore
  factory UserModel.fromFirestore(DocumentSnapshot doc) {
    final data = doc.data() as Map<String, dynamic>;
    return UserModel(
      uid: doc.id,
      email: data['email'] ?? '',
      displayName: data['displayName'] ?? '',
      createdAt: (data['createdAt'] as Timestamp).toDate(),
      lastLoginAt: data['lastLoginAt'] != null
          ? (data['lastLoginAt'] as Timestamp).toDate()
          : null,
      subscription: data['subscription'] ?? 'free',
      dailyQuota: data['dailyQuota'] ?? 10,
      quotaUsed: data['quotaUsed'] ?? 0,
      quotaResetDate: (data['quotaResetDate'] as Timestamp).toDate(),
    );
  }

  /// Créer un UserModel depuis un Map
  factory UserModel.fromMap(Map<String, dynamic> map) {
    return UserModel(
      uid: map['uid'] ?? '',
      email: map['email'] ?? '',
      displayName: map['displayName'] ?? '',
      createdAt: (map['createdAt'] as Timestamp).toDate(),
      lastLoginAt: map['lastLoginAt'] != null
          ? (map['lastLoginAt'] as Timestamp).toDate()
          : null,
      subscription: map['subscription'] ?? 'free',
      dailyQuota: map['dailyQuota'] ?? 10,
      quotaUsed: map['quotaUsed'] ?? 0,
      quotaResetDate: (map['quotaResetDate'] as Timestamp).toDate(),
    );
  }

  /// Convertir en Map pour Firestore
  Map<String, dynamic> toMap() {
    return {
      'uid': uid,
      'email': email,
      'displayName': displayName,
      'createdAt': Timestamp.fromDate(createdAt),
      'lastLoginAt':
          lastLoginAt != null ? Timestamp.fromDate(lastLoginAt!) : null,
      'subscription': subscription,
      'dailyQuota': dailyQuota,
      'quotaUsed': quotaUsed,
      'quotaResetDate': Timestamp.fromDate(quotaResetDate),
    };
  }

  /// Vérifier si l'utilisateur a atteint son quota
  bool hasReachedQuota() {
    return quotaUsed >= dailyQuota && dailyQuota != -1; // -1 = illimité
  }

  /// Copier avec modifications
  UserModel copyWith({
    String? uid,
    String? email,
    String? displayName,
    DateTime? createdAt,
    DateTime? lastLoginAt,
    String? subscription,
    int? dailyQuota,
    int? quotaUsed,
    DateTime? quotaResetDate,
  }) {
    return UserModel(
      uid: uid ?? this.uid,
      email: email ?? this.email,
      displayName: displayName ?? this.displayName,
      createdAt: createdAt ?? this.createdAt,
      lastLoginAt: lastLoginAt ?? this.lastLoginAt,
      subscription: subscription ?? this.subscription,
      dailyQuota: dailyQuota ?? this.dailyQuota,
      quotaUsed: quotaUsed ?? this.quotaUsed,
      quotaResetDate: quotaResetDate ?? this.quotaResetDate,
    );
  }
}

