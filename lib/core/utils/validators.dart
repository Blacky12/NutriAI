/// Classe utilitaire pour valider les entrées utilisateur
class Validators {
  /// Valide une adresse email
  static String? validateEmail(String? value) {
    if (value == null || value.isEmpty) {
      return 'L\'email est requis';
    }

    final emailRegex = RegExp(
      r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    );

    if (!emailRegex.hasMatch(value)) {
      return 'Entrez une adresse email valide';
    }

    return null;
  }

  /// Valide un mot de passe
  static String? validatePassword(String? value) {
    if (value == null || value.isEmpty) {
      return 'Le mot de passe est requis';
    }

    if (value.length < 6) {
      return 'Le mot de passe doit contenir au moins 6 caractères';
    }

    return null;
  }

  /// Valide le nom d'utilisateur
  static String? validateName(String? value) {
    if (value == null || value.isEmpty) {
      return 'Le nom est requis';
    }

    if (value.length < 2) {
      return 'Le nom doit contenir au moins 2 caractères';
    }

    return null;
  }

  /// Valide la description d'un repas
  static String? validateMealDescription(String? value) {
    if (value == null || value.isEmpty) {
      return 'Veuillez décrire votre repas';
    }

    if (value.length < 5) {
      return 'La description doit contenir au moins 5 caractères';
    }

    return null;
  }
}

