/// Constantes de l'application NutriAI
class AppConstants {
  // Nom de l'application
  static const String appName = 'NutriAI';
  static const String appVersion = '1.0.0';

  // Quotas utilisateurs
  static const int freeUserDailyQuota = 10;
  static const int proUserDailyQuota = 500;
  static const int premiumUserDailyQuota = -1; // Illimité

  // Messages d'erreur
  static const String networkError =
      'Erreur de connexion. Vérifiez votre connexion internet.';
  static const String unknownError =
      'Une erreur est survenue. Veuillez réessayer.';
  static const String quotaExceeded =
      'Quota journalier atteint. Revenez demain ou passez à un plan supérieur.';

  // Messages de succès
  static const String loginSuccess = 'Connexion réussie !';
  static const String registerSuccess = 'Compte créé avec succès !';
  static const String analysisSuccess = 'Analyse terminée !';

  // Disclaimer médical
  static const String medicalDisclaimer =
      'Cette application fournit des informations nutritionnelles à titre indicatif uniquement. '
      'Elle ne remplace pas l\'avis d\'un médecin, nutritionniste ou diététicien. '
      'Consultez un professionnel de santé pour tout conseil médical personnalisé.';
}

