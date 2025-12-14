"""
Wake word detection for Vaisiri Voice Assistant
"""
from ..utils.helpers import is_wake_word_in_text

class WakeWordDetector:
    """Simple wake word detector"""
    
    def __init__(self, config):
        """Initialize wake word detector"""
        self.config = config
        self.wake_word = config.get_wake_word()
        self.enabled = config.get("wake_word.enabled", True)
        self.callback = None
        print(f"WakeWordDetector initialized for '{self.wake_word}'")
        
    def is_wake_word_enabled(self) -> bool:
        """Check if wake word is enabled"""
        return self.enabled
        
    def get_wake_word(self) -> str:
        """Get wake word"""
        return self.wake_word
        
    def start_listening(self, callback):
        """Start listening for wake word"""
        self.callback = callback
        
    def stop_listening(self):
        """Stop listening"""
        self.callback = None
        
    def check_text_for_wake_word(self, text: str) -> bool:
        """Check if text contains wake word"""
        detected = is_wake_word_in_text(text, self.wake_word)
        if detected and self.callback:
            self.callback()
        return detected
