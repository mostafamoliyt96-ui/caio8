"""
CAIO Translate - Widget Router Module
Routes and formats data for UI widgets (translate and settings).
"""

from typing import Any, Dict, Optional, List
from .languages import SUPPORTED_LANGUAGES


def get_translate_widget_data(
    translation: str,
    original: Optional[str] = None,
    target_language: str = "English"
) -> Dict[str, Any]:
    """
    Generate data structure for the translate widget.
    
    Args:
        translation: The translated text
        original: The original source text (optional)
        target_language: The target language for display
    
    Returns:
        Dictionary with widget type and data
    """
    return {
        "type": "translate",
        "data": {
            "translation": translation,
            "original": original,
            "target_language": target_language
        }
    }


def get_settings_widget_data(
    settings: Dict[str, str],
    languages: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Generate data structure for the settings widget.
    
    Args:
        settings: Current settings dictionary
        languages: List of supported languages (uses default if None)
    
    Returns:
        Dictionary with widget type and data
    """
    if languages is None:
        languages = SUPPORTED_LANGUAGES
    
    return {
        "type": "settings",
        "data": {
            "settings": settings,
            "languages": languages
        }
    }


def get_ai_recommendations_widget_data(
    recommendations: List[Dict[str, str]]
) -> Dict[str, Any]:
    """
    Generate data structure for AI recommendations widget.
    
    Args:
        recommendations: List of recommended words/phrases to learn
    
    Returns:
        Dictionary with widget type and data
    """
    return {
        "type": "ai_recommendations",
        "data": {
            "recommendations": recommendations
        }
    }


def get_word_builder_widget_data(
    word: str,
    meaning: str,
    letters: List[str]
) -> Dict[str, Any]:
    """
    Generate data structure for word builder widget.
    
    Args:
        word: The word to build
        meaning: The meaning/translation of the word
        letters: List of letters (shuffled)
    
    Returns:
        Dictionary with widget type and data
    """
    return {
        "type": "word_builder",
        "data": {
            "word": word,
            "meaning": meaning,
            "letters": letters
        }
    }


def get_sentence_builder_widget_data(
    sentence: str,
    words: List[str]
) -> Dict[str, Any]:
    """
    Generate data structure for sentence builder widget.
    
    Args:
        sentence: The sentence to arrange
        words: List of words (shuffled)
    
    Returns:
        Dictionary with widget type and data
    """
    return {
        "type": "sentence_builder",
        "data": {
            "sentence": sentence,
            "words": words
        }
    }
