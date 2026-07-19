"""CAIO Translate - Supported Languages Module
Defines all supported languages for the translation service.

Note on Language Support:
- ALPHABETIC LANGUAGES: Support full Word Builder and Sentence Builder games
  (English, Arabic, French, German, Spanish, Italian, Russian, Turkish)
- NON-ALPHABETIC LANGUAGES: Support translation only, with alternative learning activities
  (Japanese, Chinese, Korean, etc.)
"""

# All supported languages for translation
SUPPORTED_LANGUAGES = [
    "English",
    "Arabic",
    "French",
    "German",
    "Spanish",
    "Japanese",
    "Chinese",
    "Italian",
    "Russian",
    "Turkish"
]

# Languages that support alphabetic games (Word Builder, Sentence Builder)
ALPHABETIC_LANGUAGES = {
    "English",
    "Arabic",
    "French",
    "German",
    "Spanish",
    "Italian",
    "Russian",
    "Turkish"
}

# Languages with non-alphabetic writing systems
# These support translation but use alternative learning activities
NON_ALPHABETIC_LANGUAGES = {
    "Japanese",  # Hiragana, Katakana, Kanji
    "Chinese"    # Hanzi (Chinese characters)
}

# Alternative learning activities for non-alphabetic languages
ALTERNATIVE_ACTIVITIES = {
    "Japanese": ["matching", "flashcards", "multiple_choice"],
    "Chinese": ["matching", "flashcards", "multiple_choice"]
}

# Language code mapping for API calls
LANGUAGE_CODES = {
    "English": "en",
    "Arabic": "ar",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Japanese": "ja",
    "Chinese": "zh",
    "Italian": "it",
    "Russian": "ru",
    "Turkish": "tr"
}

def is_valid_language(language: str) -> bool:
    """Check if the language is supported."""
    return language in SUPPORTED_LANGUAGES

def get_language_code(language: str) -> str:
    """Get the language code for a given language name."""
    return LANGUAGE_CODES.get(language, "en")


def is_alphabetic_language(language: str) -> bool:
    """Check if a language supports alphabetic games (Word Builder, Sentence Builder)."""
    return language in ALPHABETIC_LANGUAGES

def is_non_alphabetic_language(language: str) -> bool:
    """Check if a language uses non-alphabetic writing system."""
    return language in NON_ALPHABETIC_LANGUAGES

def get_alternative_activities(language: str) -> list:
    """Get alternative learning activities for non-alphabetic languages."""
    return ALTERNATIVE_ACTIVITIES.get(language, [])
