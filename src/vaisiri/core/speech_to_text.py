"""
Speech-to-Text for Vaisiri Voice Assistant
"""
try:
    import speech_recognition as sr
    SR_AVAILABLE = True
    print("✅ SpeechRecognition imported")
except ImportError as e:
    SR_AVAILABLE = False
    print(f"❌ SpeechRecognition import failed: {e}")

import tempfile
import wave
import os
from ..utils.logger import logger

class SpeechToTextEngine:
    """Speech-to-Text engine with debugging"""
    
    def __init__(self, config):
        """Initialize STT engine"""
        self.config = config
        self.recognizer = None
        
        if SR_AVAILABLE:
            try:
                self.recognizer = sr.Recognizer()
                # Adjust for ambient noise
                self.recognizer.energy_threshold = 300
                self.recognizer.dynamic_energy_threshold = True
                self.recognizer.pause_threshold = 0.8
                print("✅ SpeechToTextEngine initialized")
            except Exception as e:
                print(f"❌ STT initialization failed: {e}")
        else:
            print("❌ SpeechToTextEngine initialized without speech recognition")
        
    def transcribe_audio_data(self, audio_data: bytes, sample_rate: int) -> str:
        """Transcribe audio data with debugging"""
        if not self.recognizer or not SR_AVAILABLE:
            print("⚠️ No recognizer available - returning test text")
            return "hello google this is a test"
            
        if len(audio_data) < 1000:
            print(f"⚠️ Audio data too short: {len(audio_data)} bytes")
            return ""
            
        print(f"🎤 Transcribing {len(audio_data)} bytes of audio...")
        
        # Save to temporary WAV file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
            temp_path = tmp_file.name
            
        try:
            # Write WAV file
            with wave.open(temp_path, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sample_rate)
                wf.writeframes(audio_data)
                
            print(f"💾 Saved audio to {temp_path}")
                
            # Transcribe using speech_recognition
            with sr.AudioFile(temp_path) as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.record(source)
                
                print("🔄 Calling Google Speech Recognition...")
                text = self.recognizer.recognize_google(audio)
                print(f"✅ Transcribed: '{text}'")
                return text
                
        except sr.UnknownValueError:
            print("⚠️ Google Speech Recognition could not understand audio")
            return ""
        except sr.RequestError as e:
            print(f"❌ Google Speech Recognition service error: {e}")
            logger.error(f"STT service error: {e}")
            return ""
        except Exception as e:
            print(f"❌ STT error: {e}")
            logger.error(f"STT error: {e}")
            return ""
        finally:
            # Clean up
            try:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
            except:
                pass
                
    def listen_and_transcribe(self, audio_manager, duration: float = 5.0):
        """Listen and transcribe with debugging"""
        try:
            print(f"🎧 Starting transcription for {duration} seconds...")
            
            # Record audio
            audio_data = audio_manager.record_audio_for_duration(duration)
            
            if not audio_data:
                print("❌ No audio data recorded")
                return None, False
                
            print(f"📊 Recorded {len(audio_data)} bytes")
            
            # Transcribe
            text = self.transcribe_audio_data(audio_data, audio_manager.sample_rate)
            
            if text and text.strip():
                print(f"✅ Final transcription: '{text}'")
                return text.strip(), True
            else:
                print("❌ No text transcribed")
                return None, False
                
        except Exception as e:
            print(f"❌ Listen and transcribe error: {e}")
            logger.error(f"Listen and transcribe error: {e}")
            return None, False
