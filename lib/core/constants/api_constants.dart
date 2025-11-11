/// Constantes pour les API externes
class ApiConstants {
  // OpenRouter API (sera utilisé en Semaine 2)
  static const String openRouterBaseUrl = 'https://openrouter.ai/api/v1';
  static const String openRouterChatEndpoint = '/chat/completions';

  // Modèles IA disponibles
  static const String gpt35Turbo = 'openai/gpt-3.5-turbo';
  static const String gpt4 = 'openai/gpt-4';
  static const String claude3Haiku = 'anthropic/claude-3-haiku';
  static const String llama31 = 'meta-llama/llama-3.1-70b-instruct';
  static const String mistralLarge = 'mistralai/mistral-large';

  // Modèle par défaut (à changer selon vos tests)
  static const String defaultModel = gpt35Turbo;

  // Timeouts
  static const int apiTimeout = 30; // secondes
  static const int maxRetries = 3;
}

