import pyttsx3
import threading
import time

class TextToSpeechEngine:
    """Fresh-engine per speak for maximum reliability on Windows SAPI5."""

    def __init__(self, config):
        self.config = config
        self.lock = threading.Lock()

    def _build_engine(self):
        eng = pyttsx3.init('sapi5')
        voices = eng.getProperty('voices')
        # Prefer Zira; else second; else default
        zira = next((v for v in voices if 'zira' in v.name.lower()), None)
        if zira:
            eng.setProperty('voice', zira.id)
            print(f"🎤 Using: {zira.name}")
        elif len(voices) > 1:
            eng.setProperty('voice', voices[1].id)
            print(f"🎤 Using: {voices[1].name}")
        else:
            eng.setProperty('voice', voices[0].id)
            print(f"🎤 Using: {voices[0].name}")
        eng.setProperty('rate', 180)
        eng.setProperty('volume', 1.0)
        return eng

    def speak(self, text: str, blocking: bool = True):
        if not text or not text.strip():
            return
        clean = self._clean(text)
        if not clean:
            return

        def _do_speak():
            with self.lock:
                eng = None
                try:
                    print(f"🔊 TTS speak: '{clean[:80]}...'")
                    eng = self._build_engine()
                    eng.say(clean)
                    eng.runAndWait()
                    print("✅ TTS done")
                except Exception as e:
                    print(f"❌ TTS error: {e}")
                finally:
                    try:
                        del eng
                    except:
                        pass
                    time.sleep(0.15)  # small cooldown

        if blocking:
            _do_speak()
        else:
            threading.Thread(target=_do_speak, daemon=True).start()

    def stop_speaking(self):
        # No global engine to stop in fresh-engine approach
        print("ℹ️ stop_speaking(): no-op for fresh-engine strategy")

    def _clean(self, t: str) -> str:
        t = t.replace("\n", " ").replace("\r", " ")
        while "  " in t:
            t = t.replace("  ", " ")
        return t.strip()
