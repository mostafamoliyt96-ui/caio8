"""
CAIO Translate - MCP Server Implementation
Model Context Protocol server for ChatGPT Apps integration.
Provides translation, settings management, and AI recommendations.
"""

import asyncio
import json
import sys
import os
from typing import Any, Dict, List, Optional

# MCP imports
from mcp.server import Server
import mcp.types as types
from mcp.server.stdio import stdio_server

# Local imports
from .store import store
from .languages import SUPPORTED_LANGUAGES, is_valid_language
from .widget_router import (
    get_translate_widget_data,
    get_settings_widget_data,
    get_ai_recommendations_widget_data,
    get_word_builder_widget_data,
    get_sentence_builder_widget_data
)


# Initialize MCP Server
app = Server("caio-translate")


@app.list_tools()
async def list_tools() -> List[types.Tool]:
    """
    List all available tools for the MCP server.
    These tools are exposed to ChatGPT for use in conversations.
    """
    return [
        types.Tool(
            name="caio-initialize",
            description="Initialize the CAIO Translate application and return current settings.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="caio-update-settings",
            description="Update the target language for translations.",
            inputSchema={
                "type": "object",
                "properties": {
                    "target_language": {
                        "type": "string",
                        "description": "The target language for translations (e.g., Arabic, French, Spanish)"
                    }
                },
                "required": ["target_language"]
            }
        ),
        types.Tool(
            name="caio-get-settings",
            description="Retrieve current application settings including target language.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="caio-translate",
            description="Translate text into the selected target language.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to translate"
                    },
                    "target_language": {
                        "type": "string",
                        "description": "Optional: Override the default target language"
                    }
                },
                "required": ["text"]
            }
        ),
        types.Tool(
            name="caio-save",
            description="Save a translation pair for future reference.",
            inputSchema={
                "type": "object",
                "properties": {
                    "original": {
                        "type": "string",
                        "description": "The original text"
                    },
                    "translation": {
                        "type": "string",
                        "description": "The translated text"
                    }
                },
                "required": ["original", "translation"]
            }
        ),
        types.Tool(
            name="caio-get-saved-translations",
            description="Retrieve all saved translations.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="caio-get-ai-recommendations",
            description="Get AI-recommended words/phrases to learn from the translated text.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to extract recommendations from"
                    },
                    "count": {
                        "type": "integer",
                        "description": "Number of recommendations (default: 3-5)"
                    }
                },
                "required": ["text"]
            }
        ),
        types.Tool(
            name="caio-get-word-builder",
            description="Generate a word builder exercise for learning.",
            inputSchema={
                "type": "object",
                "properties": {
                    "word": {
                        "type": "string",
                        "description": "The word to build"
                    },
                    "meaning": {
                        "type": "string",
                        "description": "The meaning/translation of the word"
                    }
                },
                "required": ["word", "meaning"]
            }
        ),
        types.Tool(
            name="caio-get-sentence-builder",
            description="Generate a sentence builder exercise for learning.",
            inputSchema={
                "type": "object",
                "properties": {
                    "sentence": {
                        "type": "string",
                        "description": "The sentence to arrange"
                    }
                },
                "required": ["sentence"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Execute a tool call from ChatGPT.
    Routes to appropriate handler based on tool name.
    """
    
    if name == "caio-initialize":
        return await handle_initialize()
    
    elif name == "caio-update-settings":
        return await handle_update_settings(arguments)
    
    elif name == "caio-get-settings":
        return await handle_get_settings()
    
    elif name == "caio-translate":
        return await handle_translate(arguments)
    
    elif name == "caio-save":
        return await handle_save(arguments)
    
    elif name == "caio-get-saved-translations":
        return await handle_get_saved_translations()
    
    elif name == "caio-get-ai-recommendations":
        return await handle_get_ai_recommendations(arguments)
    
    elif name == "caio-get-word-builder":
        return await handle_get_word_builder(arguments)
    
    elif name == "caio-get-sentence-builder":
        return await handle_get_sentence_builder(arguments)
    
    else:
        error_msg = f"Unknown tool: {name}"
        return [types.TextContent(type="text", text=json.dumps({
            "error": error_msg,
            "status": "error"
        }))]


async def handle_initialize() -> List[types.TextContent]:
    """Initialize the application and return current settings."""
    settings = store.get_settings()
    response = {
        "status": "initialized",
        "message": "CAIO Translate initialized successfully",
        "settings": settings,
        "supported_languages": SUPPORTED_LANGUAGES
    }
    return [types.TextContent(type="text", text=json.dumps(response))]


async def handle_update_settings(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Update application settings (target language)."""
    target_language = arguments.get("target_language", "").strip()
    
    if not target_language:
        return [types.TextContent(type="text", text=json.dumps({
            "error": "target_language is required",
            "status": "error"
        }))]
    
    if not is_valid_language(target_language):
        return [types.TextContent(type="text", text=json.dumps({
            "error": f"Unsupported language: {target_language}",
            "supported": SUPPORTED_LANGUAGES,
            "status": "error"
        }))]
    
    store.update_settings(target_language)
    response = {
        "status": "success",
        "message": f"Target language updated to {target_language}",
        "settings": store.get_settings()
    }
    return [types.TextContent(type="text", text=json.dumps(response))]


async def handle_get_settings() -> List[types.TextContent]:
    """Get current application settings."""
    settings = store.get_settings()
    response = {
        "status": "success",
        "settings": settings,
        "supported_languages": SUPPORTED_LANGUAGES
    }
    return [types.TextContent(type="text", text=json.dumps(response))]


async def handle_translate(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle translation requests."""
    text = arguments.get("text", "").strip()
    target_language = arguments.get("target_language") or store.get_settings()["target_language"]
    
    if not text:
        return [types.TextContent(type="text", text=json.dumps({
            "error": "text is required",
            "status": "error"
        }))]
    
    if not is_valid_language(target_language):
        return [types.TextContent(type="text", text=json.dumps({
            "error": f"Unsupported language: {target_language}",
            "status": "error"
        }))]
    
    # In production, this would call an actual translation API (e.g., Google Translate, OpenAI)
    # For now, we return a placeholder with the widget data structure
    translation_placeholder = f"[Translation to {target_language}]: {text}"
    
    widget_data = get_translate_widget_data(
        translation=translation_placeholder,
        original=text,
        target_language=target_language
    )
    
    response = {
        "status": "success",
        "original": text,
        "translation": translation_placeholder,
        "target_language": target_language,
        "widget": widget_data
    }
    return [types.TextContent(type="text", text=json.dumps(response))]


async def handle_save(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Save a translation pair."""
    original = arguments.get("original", "").strip()
    translation = arguments.get("translation", "").strip()
    
    if not original or not translation:
        return [types.TextContent(type="text", text=json.dumps({
            "error": "Both 'original' and 'translation' are required",
            "status": "error"
        }))]
    
    store.save_translation(original, translation)
    response = {
        "status": "success",
        "message": "Translation saved successfully",
        "saved": {
            "original": original,
            "translation": translation
        }
    }
    return [types.TextContent(type="text", text=json.dumps(response))]


async def handle_get_saved_translations() -> List[types.TextContent]:
    """Get all saved translations."""
    saved = store.get_saved_translations()
    response = {
        "status": "success",
        "count": len(saved),
        "translations": saved
    }
    return [types.TextContent(type="text", text=json.dumps(response))]


async def handle_get_ai_recommendations(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Get AI recommendations for words to learn."""
    text = arguments.get("text", "").strip()
    count = arguments.get("count", 3)
    
    if not text:
        return [types.TextContent(type="text", text=json.dumps({
            "error": "text is required",
            "status": "error"
        }))]
    
    # Extract words from text (simple implementation)
    words = text.split()[:count]
    recommendations = [{"word": word, "type": "word"} for word in words]
    
    widget_data = get_ai_recommendations_widget_data(recommendations)
    response = {
        "status": "success",
        "recommendations": recommendations,
        "widget": widget_data
    }
    return [types.TextContent(type="text", text=json.dumps(response))]


async def handle_get_word_builder(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Generate a word builder exercise."""
    word = arguments.get("word", "").strip()
    meaning = arguments.get("meaning", "").strip()
    
    if not word or not meaning:
        return [types.TextContent(type="text", text=json.dumps({
            "error": "Both 'word' and 'meaning' are required",
            "status": "error"
        }))]
    
    # Shuffle letters
    import random
    letters = list(word.lower())
    random.shuffle(letters)
    
    widget_data = get_word_builder_widget_data(word, meaning, letters)
    response = {
        "status": "success",
        "word": word,
        "meaning": meaning,
        "letters": letters,
        "widget": widget_data
    }
    return [types.TextContent(type="text", text=json.dumps(response))]


async def handle_get_sentence_builder(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Generate a sentence builder exercise."""
    sentence = arguments.get("sentence", "").strip()
    
    if not sentence:
        return [types.TextContent(type="text", text=json.dumps({
            "error": "sentence is required",
            "status": "error"
        }))]
    
    # Split and shuffle words
    import random
    words = sentence.split()
    shuffled_words = words.copy()
    random.shuffle(shuffled_words)
    
    widget_data = get_sentence_builder_widget_data(sentence, shuffled_words)
    response = {
        "status": "success",
        "sentence": sentence,
        "words": shuffled_words,
        "widget": widget_data
    }
    return [types.TextContent(type="text", text=json.dumps(response))]


async def main():
    """Main entry point for the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
