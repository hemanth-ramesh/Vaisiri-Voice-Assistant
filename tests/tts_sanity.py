import time
import pyttsx3

def fresh_engine_with_zira():
    eng = pyttsx3.init('sapi5')
    voices = eng.getProperty('voices')
    zira = next((v for v in voices if 'zira' in v.name.lower()), None)
    if zira:
        eng.setProperty('voice', zira.id)
        print(f"🎤 Using: {zira.name}")
    else:
        print("⚠️ Zira not found, using default")
    eng.setProperty('rate', 180)
    eng.setProperty('volume', 1.0)
    return eng

def speak_once(text):
    print(f"🔊 Speaking: {text}")
    eng = fresh_engine_with_zira()
    try:
        eng.say(text)
        eng.runAndWait()
        print("✅ Done\n")
    finally:
        # Explicitly delete engine to release SAPI handle
        del eng
        time.sleep(0.25)  # small gap so OS releases audio

if __name__ == "__main__":
    speak_once("Hello. This is Microsoft Zira. T T S sanity test line one.")
    speak_once("Line two. If this is audible, the system audio path is good.")
    speak_once("Line three. We will proceed to integrate with the assistant.")
