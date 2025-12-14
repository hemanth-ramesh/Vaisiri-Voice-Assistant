"""
Helper utilities for Vaisiri Voice Assistant
"""
import time
from functools import wraps

def retry_on_failure(max_retries: int = 2):
    """Retry decorator"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries:
                        raise e
                    time.sleep(1)
            return None
        return wrapper
    return decorator

def normalize_text(text: str) -> str:
    """Normalize text"""
    if not text:
        return ""
    return text.lower().strip()

def is_wake_word_in_text(text: str, wake_word: str) -> bool:
    """Check if wake word is in text"""
    return normalize_text(wake_word) in normalize_text(text)
