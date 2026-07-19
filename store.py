"""
CAIO Translate - Data Store Module
Handles persistence of settings and translations using JSON file storage.
"""

import json
import os
from typing import Any, Dict, List
from datetime import datetime

STORE_FILE = "store.json"

class Store:
    """
    Persistent storage for CAIO Translate application.
    Manages settings (target language) and saved translations.
    """
    
    def __init__(self, store_file: str = STORE_FILE):
        """Initialize the store with optional custom file path."""
        self.store_file = store_file
        self.data = self._load()
    
    def _load(self) -> Dict[str, Any]:
        """
        Load data from JSON file or return default structure.
        
        Returns:
            Dictionary with target_language and saved_translations
        """
        if os.path.exists(self.store_file):
            try:
                with open(self.store_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self._get_default_data()
        return self._get_default_data()
    
    def _get_default_data(self) -> Dict[str, Any]:
        """Get default data structure."""
        return {
            "target_language": "English",
            "saved_translations": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
    
    def _save(self) -> None:
        """
        Save data to JSON file.
        Updates the modified timestamp.
        """
        self.data["updated_at"] = datetime.now().isoformat()
        try:
            with open(self.store_file, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving store: {e}")
    
    def get_settings(self) -> Dict[str, str]:
        """
        Get current settings.
        
        Returns:
            Dictionary with target_language
        """
        return {
            "target_language": self.data.get("target_language", "English")
        }
    
    def update_settings(self, target_language: str) -> None:
        """
        Update target language setting.
        
        Args:
            target_language: The target language for translations
        """
        self.data["target_language"] = target_language
        self._save()
    
    def save_translation(self, original: str, translation: str) -> None:
        """
        Save a translation pair to the store.
        
        Args:
            original: The original text
            translation: The translated text
        """
        translation_entry = {
            "original": original,
            "translation": translation,
            "timestamp": datetime.now().isoformat()
        }
        self.data["saved_translations"].append(translation_entry)
        self._save()
    
    def get_saved_translations(self) -> List[Dict[str, str]]:
        """
        Get all saved translations.
        
        Returns:
            List of translation pairs
        """
        return self.data.get("saved_translations", [])
    
    def clear_translations(self) -> None:
        """Clear all saved translations."""
        self.data["saved_translations"] = []
        self._save()
    
    def reset(self) -> None:
        """Reset store to default state."""
        self.data = self._get_default_data()
        self._save()


# Global store instance
store = Store()
