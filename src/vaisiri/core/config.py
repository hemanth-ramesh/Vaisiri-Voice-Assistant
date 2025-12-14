"""
Configuration management for Vaisiri Voice Assistant (Gemini-enabled)
"""
import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv


class Config:
    """Configuration manager for Vaisiri Voice Assistant"""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration manager

        Args:
            config_path: Optional path to a YAML config file
        """
        # Load environment variables from .env (if present)
        load_dotenv()

        self.config_path = config_path or self._get_default_config_path()
        self.config_data: Dict[str, Any] = {}

        # Load configuration (YAML or defaults)
        self.load_config()

    # -----------------------------
    # Internal loading helpers
    # -----------------------------
    def _get_default_config_path(self) -> str:
        """Get default configuration file path"""
        # src/vaisiri/core/config.py -> go up 4 levels to project root
        current_dir = Path(__file__).parent.parent.parent.parent
        return str(current_dir / "config" / "settings.yaml")

    def load_config(self) -> None:
        """Load configuration from YAML file if available"""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.config_data = yaml.safe_load(f) or {}
        except FileNotFoundError:
            print(f"Warning: Configuration file not found: {self.config_path}")
            self.config_data = self._get_default_config()
        except yaml.YAMLError as e:
            print(f"Error parsing configuration file: {e}")
            self.config_data = self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Default configuration used if no YAML file is found"""
        return {
            "wake_word": {
                "enabled": True,
                "keyword": "vaisiri",
                "sensitivity": 0.5,
                "timeout": 5.0,
            },
            "audio": {
                "sample_rate": 16000,
                "chunk_size": 1024,
                "channels": 1,
            },
            "stt": {
                "primary_engine": "google",  # google (SpeechRecognition)
            },
            "llm": {
                "provider": "gemini",                  # gemini (google-generativeai)
                "model": "models/gemini-2.5-flash",    # uses your available model
                "max_tokens": 150,                     # concise voice replies
                "temperature": 0.7,
                "system_prompt": (
                    "You are Vaisiri, a helpful voice assistant. "
                    "Keep responses short, friendly, and conversational. "
                    "Limit answers to 1-2 sentences for voice interaction."
                ),
            },
            "tts": {
                "engine": "pyttsx3",
            },
            "logging": {
                "level": "INFO",
            },
        }

    # -----------------------------
    # Generic getters
    # -----------------------------
    def get(self, key: str, default: Any = None) -> Any:
        """
        Read a nested config value using dot notation.

        Example:
            get('llm.model', 'models/gemini-2.5-flash')
        """
        keys = key.split(".")
        value: Any = self.config_data

        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    # -----------------------------
    # Environment helpers
    # -----------------------------
    def get_env(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Read an environment variable with optional default"""
        return os.getenv(key, default)

    # -----------------------------
    # API keys
    # -----------------------------
    def get_gemini_api_key(self) -> Optional[str]:
        """Return the Google Gemini API key from environment (.env)"""
        # Expecting: GEMINI_API_KEY=AIza...
        return self.get_env("GEMINI_API_KEY")

    # -----------------------------
    # Wake word / audio
    # -----------------------------
    def is_wake_word_enabled(self) -> bool:
        return bool(self.get("wake_word.enabled", True))

    def get_wake_word(self) -> str:
        return str(self.get("wake_word.keyword", "vaisiri"))

    def get_sample_rate(self) -> int:
        return int(self.get("audio.sample_rate", 16000))

    def get_chunk_size(self) -> int:
        return int(self.get("audio.chunk_size", 1024))

    # -----------------------------
    # STT
    # -----------------------------
    def get_stt_engine(self) -> str:
        return str(self.get("stt.primary_engine", "google"))

    # -----------------------------
    # LLM
    # -----------------------------
    def get_llm_provider(self) -> str:
        return str(self.get("llm.provider", "gemini"))

    def get_llm_model(self) -> str:
        """
        Get LLM model name. Defaults to an available model from your list.
        Example: 'models/gemini-2.5-flash'
        """
        return str(self.get("llm.model", "models/gemini-2.5-flash"))

    def get_system_prompt(self) -> str:
        return str(
            self.get(
                "llm.system_prompt",
                "You are Vaisiri, a helpful voice assistant. Keep responses short.",
            )
        )

    def get_llm_max_tokens(self) -> int:
        return int(self.get("llm.max_tokens", 150))

    def get_llm_temperature(self) -> float:
        try:
            return float(self.get("llm.temperature", 0.7))
        except (TypeError, ValueError):
            return 0.7

    # -----------------------------
    # TTS
    # -----------------------------
    def get_tts_engine(self) -> str:
        return str(self.get("tts.engine", "pyttsx3"))

    # -----------------------------
    # Logging
    # -----------------------------
    def get_log_level(self) -> str:
        return str(self.get("logging.level", "INFO"))
