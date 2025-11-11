import 'package:cloud_firestore/cloud_firestore.dart';

/// Modèle représentant une analyse de repas
class MealModel {
  final String id;
  final String userId;
  final String description;
  final NutritionAnalysis analysis;
  final DateTime timestamp;
  final MealMetadata metadata;

  MealModel({
    required this.id,
    required this.userId,
    required this.description,
    required this.analysis,
    required this.timestamp,
    required this.metadata,
  });

  /// Créer un MealModel depuis un document Firestore
  factory MealModel.fromFirestore(DocumentSnapshot doc) {
    final data = doc.data() as Map<String, dynamic>;
    return MealModel(
      id: doc.id,
      userId: data['userId'] ?? '',
      description: data['description'] ?? '',
      analysis: NutritionAnalysis.fromMap(data['analysis'] ?? {}),
      timestamp: (data['timestamp'] as Timestamp).toDate(),
      metadata: MealMetadata.fromMap(data['metadata'] ?? {}),
    );
  }

  /// Convertir en Map pour Firestore
  Map<String, dynamic> toMap() {
    return {
      'userId': userId,
      'description': description,
      'analysis': analysis.toMap(),
      'timestamp': Timestamp.fromDate(timestamp),
      'metadata': metadata.toMap(),
    };
  }
}

/// Analyse nutritionnelle d'un repas
class NutritionAnalysis {
  final double calories;
  final double proteins;
  final double carbs;
  final double fats;
  final double fiber;
  final List<String> suggestions;
  final String detailedAnalysis;

  NutritionAnalysis({
    required this.calories,
    required this.proteins,
    required this.carbs,
    required this.fats,
    this.fiber = 0,
    required this.suggestions,
    this.detailedAnalysis = '',
  });

  factory NutritionAnalysis.fromMap(Map<String, dynamic> map) {
    return NutritionAnalysis(
      calories: (map['calories'] ?? 0).toDouble(),
      proteins: (map['proteins'] ?? 0).toDouble(),
      carbs: (map['carbs'] ?? 0).toDouble(),
      fats: (map['fats'] ?? 0).toDouble(),
      fiber: (map['fiber'] ?? 0).toDouble(),
      suggestions: List<String>.from(map['suggestions'] ?? []),
      detailedAnalysis: map['detailedAnalysis'] ?? '',
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'calories': calories,
      'proteins': proteins,
      'carbs': carbs,
      'fats': fats,
      'fiber': fiber,
      'suggestions': suggestions,
      'detailedAnalysis': detailedAnalysis,
    };
  }
}

/// Métadonnées d'un appel API
class MealMetadata {
  final String modelUsed;
  final int tokensUsed;
  final double costUSD;
  final int responseTimeMs;

  MealMetadata({
    required this.modelUsed,
    required this.tokensUsed,
    required this.costUSD,
    required this.responseTimeMs,
  });

  factory MealMetadata.fromMap(Map<String, dynamic> map) {
    return MealMetadata(
      modelUsed: map['modelUsed'] ?? '',
      tokensUsed: map['tokensUsed'] ?? 0,
      costUSD: (map['costUSD'] ?? 0).toDouble(),
      responseTimeMs: map['responseTimeMs'] ?? 0,
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'modelUsed': modelUsed,
      'tokensUsed': tokensUsed,
      'costUSD': costUSD,
      'responseTimeMs': responseTimeMs,
    };
  }
}

