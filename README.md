# Vaisiri Voice Assistant

Vaisiri Voice Assistant is a Python-based desktop voice assistant with a modern GUI, wake-word activation, and conversational AI. It uses Google Speech Recognition for speech-to-text, a modular LLM/knowledge-base layer for responses, and Windows text-to-speech for natural spoken output.

## Features

- Wake word activation (e.g., “why siri” or custom phrase)  
- Speech-to-text using Google Speech Recognition (via `speech_recognition`)  
- Conversational responses powered by an LLM (Gemini Flash-Lite + KB)  
- Text-to-speech using Windows voices (e.g., Microsoft Zira)  
- Tkinter-based GUI with:
  - Status indicators (listening / processing / speaking)
  - MIC ON/OFF toggle
  - Visual wave/dot animation during listening
- Support for Bluetooth and external microphones (configurable device index)  
- Modular architecture:
  - `AudioManager`
  - `WakeWordDetector`
  - `SpeechToTextEngine`
  - `LLMManager`
  - `TextToSpeechEngine`
  - `VaisiriAdvancedGUI`

## Tech Stack

- Python 3.8+  
- Tkinter (GUI)  
- `speech_recognition` (Google STT)  
- Windows SAPI / `pyttsx3` or similar for TTS (depending on your implementation)  
- Gemini / Gemini Flash-Lite client for LLM + KB  
- Optional: `pyaudio` / `sounddevice` for audio capture  
- Pillow (for logo/images)

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/vaisiri-voice-assistant.git
cd vaisiri-voice-assistant
```

### 2. Create and activate virtual environment (Windows)

```bash
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
```

### 3. Install dependencies

If you have `requirements.txt`:

```bash
pip install -r requirements.txt
```

Otherwise, install the core packages you use, for example:

```bash
pip install SpeechRecognition pillow pyaudio sounddevice
# plus any others: gemini client, pyttsx3, etc.
```

> Note: On Windows, if `pyaudio` fails to install via pip, use:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

### 4. Configure environment (optional)

If you use any environment variables (e.g., mic index, API keys), document them here, for example:

```bash
set VAISIRI_MIC_INDEX=9
```

If you use Google Cloud STT instead of the free web API, also set:

```bash
set GOOGLE_APPLICATION_CREDENTIALS=path\to\service-account.json
```

## Running the Assistant

From the project root with the virtual environment activated:

```bash
python -m vaisiri.main --gui
```

Then:

1. Ensure your preferred microphone/headset is connected (Bluetooth recommended).  
2. Speak the wake word (e.g., “why siri”).  
3. Ask your question or give a command after the greeting.

## Project Structure (example)

```text
vaisiri_voice_assistant/
├─ src/
│  └─ vaisiri/
│     ├─ core/
│     │  ├─ audio_manager.py
│     │  ├─ speech_to_text.py
│     │  ├─ text_to_speech.py
│     │  ├─ wake_word.py
│     │  ├─ llm_manager.py
│     │  └─ config.py
│     └─ ui/
│        └─ modern_gui.py
├─ vaisiri-logo.jpg
├─ requirements.txt
└─ main.py
```

Adjust the structure to match your actual layout.

## Usage

- Say the wake word to start a session.  
- Ask questions like:
  - “What is your name?”  
  - “Tell me about Vaisiri Institute.”  
- Say “stop”, “goodbye”, or “bye” to end the conversation.

## Highlights

- Custom, open, and fully controllable voice assistant  
- Real-time GUI feedback and smooth user experience  
- Strong integration of STT → LLM → TTS pipeline  
- Easily extensible with new commands, skills, or integrations

## Future Improvements

- Add offline STT option (e.g., Whisper or Vosk)  
- Add command-specific actions (open apps, control system, etc.)  
- Add multi-language support  
- Package as an executable for easy installation
