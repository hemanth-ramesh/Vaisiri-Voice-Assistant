"""
Text-to-Speech Engine with Direct pyttsx3 Integration
"""
import pyttsx3
import threading
import queue
import time
from ..utils.logger import logger

class TextToSpeechEngine:
    """TTS Engine with single pyttsx3 instance and main thread execution"""

    def __init__(self, config):
        self.config = config
        self.engine = None
        self.speech_queue = queue.Queue()
        self.is_speaking = False
        self.shutdown_requested = False
        
        # Initialize pyttsx3 engine
        self._initialize_engine()
        
        # Start speech worker thread
        self.speech_thread = threading.Thread(target=self._speech_worker, daemon=True)
        self.speech_thread.start()

    def _initialize_engine(self):
        """Initialize pyttsx3 engine with proper settings"""
        try:
            print("🔧 Initializing TTS engine...")
            self.engine = pyttsx3.init()
            
            # Get available voices
            voices = self.engine.getProperty('voices')
            print(f"🔍 Available voices:")
            for i, voice in enumerate(voices):
                print(f"  {i}: {voice.name} - {voice.id}")
            
            # Configure voice (prefer female voice)
            if len(voices) > 1:
                self.engine.setProperty('voice', voices[1].id)  # Usually female
                print(f"🎤 Selected female voice: {voices[1].name}")
            else:
                self.engine.setProperty('voice', voices[0].id)
                print(f"🎤 Selected voice: {voices[0].name}")
            
            # Set speech properties
            self.engine.setProperty('rate', 150)    # Words per minute
            self.engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)
            
            print("✅ TTS engine initialized successfully")
            
        except Exception as e:
            logger.error(f"TTS engine initialization failed: {e}")
            print(f"❌ TTS engine initialization failed: {e}")
            self.engine = None

    def _speech_worker(self):
        """Background worker to handle speech queue"""
        while not self.shutdown_requested:
            try:
                # Wait for speech request with timeout
                try:
                    text = self.speech_queue.get(timeout=1.0)
                except queue.Empty:
                    continue
                
                if text and self.engine:
                    self._speak_directly(text)
                    
            except Exception as e:
                print(f"❌ Speech worker error: {e}")
                time.sleep(0.1)

    def _speak_directly(self, text):
        """Directly speak text using pyttsx3"""
        try:
            print(f"🔊 TTS speaking: '{text[:60]}...'")
            self.is_speaking = True
            
            # Clear any existing speech
            self.engine.stop()
            
            # Speak the text
            self.engine.say(text)
            self.engine.runAndWait()
            
            self.is_speaking = False
            print("✅ TTS speech completed")
            
        except Exception as e:
            print(f"❌ TTS speech error: {e}")
            self.is_speaking = False

    def speak(self, text):
        """Queue text for speech (thread-safe)"""
        if not text or not text.strip():
            print("⚠️ TTS: Empty text, skipping")
            return
            
        # Clean text for better speech
        cleaned_text = self._clean_text_for_speech(text)
        
        if not cleaned_text:
            print("⚠️ TTS: No content after cleaning, skipping")
            return
            
        # Add to speech queue
        try:
            self.speech_queue.put(cleaned_text, block=False)
            print(f"📤 TTS: Queued for speech: '{cleaned_text[:50]}...'")
        except queue.Full:
            print("⚠️ TTS: Speech queue full, skipping")

    def _clean_text_for_speech(self, text):
        """Clean text for better TTS output"""
        if not text:
            return ""
            
        # Remove common TTS problematic characters
        text = text.replace('\n', ' ').replace('\r', ' ')
        text = text.replace('  ', ' ')  # Multiple spaces
        
        # Limit length for better speech flow
        if len(text) > 300:
            # Find last complete sentence within limit
            truncated = text[:300]
            last_period = truncated.rfind('.')
            last_exclamation = truncated.rfind('!')
            last_question = truncated.rfind('?')
            
            last_sentence_end = max(last_period, last_exclamation, last_question)
            
            if last_sentence_end > 100:  # If we found a good break point
                text = truncated[:last_sentence_end + 1]
            else:
                text = truncated + "..."
        
        return text.strip()

    def stop_speaking(self):
        """Stop current speech"""
        try:
            if self.engine:
                self.engine.stop()
            self.is_speaking = False
            print("🛑 TTS: Speech stopped")
        except Exception as e:
            print(f"❌ TTS stop error: {e}")

    def is_busy(self):
        """Check if TTS is currently speaking"""
        return self.is_speaking

    def shutdown(self):
        """Shutdown TTS engine"""
        print("🔄 Shutting down TTS engine...")
        self.shutdown_requested = True
        self.stop_speaking()
        
        # Wait for speech thread to finish
        if self.speech_thread.is_alive():
            self.speech_thread.join(timeout=2.0)
        
        try:
            if self.engine:
                del self.engine
                self.engine = None
        except:
            pass
        
        print("✅ TTS engine shutdown complete")
