import tkinter as tk
from tkinter import messagebox
import threading
import time
import queue
from PIL import Image, ImageTk
import os

try:
    from vaisiri.core import (
        Config, AudioManager, WakeWordDetector,
        SpeechToTextEngine, LLMManager, TextToSpeechEngine
    )
except ImportError:
    from ..core import (
        Config, AudioManager, WakeWordDetector,
        SpeechToTextEngine, LLMManager, TextToSpeechEngine
    )

class VaisiriAdvancedGUI:
    """
    Vaisiri Voice Assistant GUI with Mic Control
    - Wake word driven conversation
    - KB → Gemini → Fallback response flow
    - Fresh-engine TTS integration
    - Fully functional MIC ON/OFF button
    """

    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_components()
        self.setup_ui()

        # State variables
        self.conversation_active = False
        self.wake_word_listening = True
        self.is_listening = False
        self.is_speaking = False
        self.mic_enabled = True  # Microphone control
        self.shutdown_requested = False
        self.message_queue = queue.Queue()

        self.start_background_services()
        self.root.after(100, self.process_messages)

    def setup_window(self):
        self.root.title("Vaisiri Voice Assistant - VIMTech")
        self.root.geometry("500x700")
        self.root.configure(bg="#0f1419")
        self.root.resizable(True, True)
        self.center_window()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def center_window(self):
        self.root.update_idletasks()
        w, h = self.root.winfo_width(), self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def setup_components(self):
        try:
            self.config = Config()
            self.audio_manager = AudioManager(self.config)
            self.wake_word_detector = WakeWordDetector(self.config)
            self.stt_engine = SpeechToTextEngine(self.config)
            self.llm_manager = LLMManager(self.config)
            self.tts_engine = TextToSpeechEngine(self.config)
            print("✅ All GUI components initialized!")
        except Exception as e:
            messagebox.showerror("Error", f"Component init failed:\n{e}")

    def find_logo_file(self):
        cwd = os.getcwd()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        candidates = [
            os.path.join(cwd, "vaisiri-logo.jpg"),
            os.path.join(script_dir, "vaisiri-logo.jpg"),
            os.path.join(script_dir, "..", "vaisiri-logo.jpg"),
            os.path.join(cwd, "assets", "vaisiri-logo.jpg"),
        ]
        for p in candidates:
            if os.path.exists(p):
                return p
        return None

    def load_logo_image(self):
        path = self.find_logo_file()
        if path:
            img = Image.open(path).resize((420, 120), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        return None

    def setup_ui(self):
        main = tk.Frame(self.root, bg="#0f1419")
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # Header with logo
        header = tk.Frame(main, bg="#0f1419")
        header.pack(fill="x", pady=(0, 10))
        logo_img = self.load_logo_image()
        if logo_img:
            tk.Label(header, image=logo_img, bg="#0f1419").pack(pady=(0, 8))
            self.logo_image = logo_img
        else:
            tk.Label(header, text="VAISIRI INSTITUTE", font=("Segoe UI Light", 22, "bold"),
                     fg="#8B4A9C", bg="#0f1419").pack()
            tk.Label(header, text="OF MANAGEMENT & TECHNOLOGY", font=("Segoe UI", 12, "bold"),
                     fg="#8B4A9C", bg="#0f1419").pack(pady=(2, 8))
        tk.Label(header, text="◉ Vaisiri Voice Assistant", font=("Segoe UI Light", 20, "bold"),
                 fg="#4da6ff", bg="#0f1419").pack()

        # Status indicator
        status = tk.Frame(main, bg="#0f1419")
        status.pack(fill="x", pady=(16, 8))
        self.status_indicator = tk.Label(status, text="●", font=("Segoe UI", 24),
                                         fg="#00ff7f", bg="#0f1419")
        self.status_indicator.pack()
        self.status_label = tk.Label(status, text="🎧 Listening for wake word 'vaisiri'...",
                                     font=("Segoe UI", 14), fg="#ffffff", bg="#0f1419")
        self.status_label.pack(pady=(8, 0))

        # Visual indicator
        visual = tk.Frame(main, bg="#0f1419")
        visual.pack(pady=(18, 8))
        self.visual_indicator = tk.Label(visual, text="🎤", font=("Segoe UI Emoji", 84),
                                         fg="#4da6ff", bg="#0f1419")
        self.visual_indicator.pack()
        self.animation_frame = tk.Frame(main, bg="#0f1419")
        self.animation_frame.pack(pady=10)
        self.create_animation_dots()

        # MIC ON/OFF Button - PROMINENT PLACEMENT
        mic_control_frame = tk.Frame(main, bg="#0f1419")
        mic_control_frame.pack(pady=(15, 10))
        
        self.mic_button = tk.Button(
            mic_control_frame, 
            text="🎤 MIC ON", 
            font=("Segoe UI", 14, "bold"),
            fg="#ffffff", 
            bg="#00aa00", 
            activebackground="#00cc00",
            activeforeground="#ffffff",
            relief="raised", 
            bd=3, 
            padx=25, 
            pady=10,
            cursor="hand2",
            command=self.toggle_microphone
        )
        self.mic_button.pack()

        # Instructions
        tk.Label(main, text="Say 'vaisiri' to start conversation",
                 font=("Segoe UI", 13, "bold"), fg="#ffffff", bg="#0f1419").pack(pady=(15, 6))
        tk.Label(main, text="✓ Personal voice assistant\n✓ Advanced Knowledge Base",
                 font=("Segoe UI", 11), fg="#7a8a99", bg="#0f1419", justify="center").pack()

        # Response display
        self.current_response = tk.Label(main, text="Ready to assist you...", font=("Segoe UI", 12),
                                         fg="#ffffff", bg="#1a1f26", wraplength=420, justify="center",
                                         pady=12)
        self.current_response.pack(fill="x", pady=(16, 6))

        # Footer
        footer = tk.Frame(main, bg="#0f1419")
        footer.pack(fill="x", pady=(8, 4))
        self.footer_left = tk.Label(footer, text="🚀 Powered by AI", 
                                   font=("Segoe UI", 10), fg="#00ff7f", bg="#0f1419")
        self.footer_left.pack(side="left")
        tk.Label(footer, text="VIMT - Tumkur", font=("Segoe UI", 10),
                 fg="#8B4A9C", bg="#0f1419").pack(side="right")

    def create_animation_dots(self):
        self.dot_labels = []
        for _ in range(4):
            dot = tk.Label(self.animation_frame, text="●", font=("Segoe UI", 14),
                           fg="#0f1419", bg="#0f1419")
            dot.pack(side="left", padx=6)
            self.dot_labels.append(dot)

    def toggle_microphone(self):
        """Toggle microphone on/off with full visual feedback"""
        self.mic_enabled = not self.mic_enabled
        
        if self.mic_enabled:
            # Microphone ON
            self.mic_button.config(
                text="🎤 MIC ON", 
                bg="#00aa00", 
                activebackground="#00cc00"
            )
            self.footer_left.config(text="🚀 Powered by AI", fg="#00ff7f")
            
            # Restore listening if not in conversation
            if not self.conversation_active:
                self.wake_word_listening = True
                self.status_label.config(text="🎧 Listening for wake word 'vaisiri'...")
                self.visual_indicator.config(text="🎤", fg="#4da6ff")
                
        else:
            # Microphone OFF
            self.mic_button.config(
                text="🔇 MIC OFF", 
                bg="#aa0000", 
                activebackground="#cc0000"
            )
            self.footer_left.config(text="🔇 Microphone: Disabled", fg="#ff4444")
            
            # Stop all listening activity
            self.wake_word_listening = False
            if self.conversation_active:
                self.conversation_active = False
            self.status_label.config(text="🔇 Microphone disabled - Click MIC ON to enable")
            self.visual_indicator.config(text="🔇", fg="#ff4444")
            self.hide_animation()

    def start_background_services(self):
        threading.Thread(target=self.wake_word_worker, daemon=True).start()

    def wake_word_worker(self):
        while not self.shutdown_requested:
            if not self.wake_word_listening or self.conversation_active or not self.mic_enabled:
                time.sleep(0.5)
                continue
            text, success = self.stt_engine.listen_and_transcribe(self.audio_manager, 3.0)
            if success and text and self.wake_word_detector.check_text_for_wake_word(text):
                self.message_queue.put(("wake_word_detected", text))

    def continuous_conversation_worker(self):
        while self.conversation_active and not self.shutdown_requested and self.mic_enabled:
            if self.is_speaking:
                time.sleep(0.5)
                continue
                
            self.message_queue.put(("listening_start", None))
            text, success = self.stt_engine.listen_and_transcribe(self.audio_manager, 5.0)
            self.message_queue.put(("listening_end", None))
            
            if not success or not text:
                self.message_queue.put(("listening_failed", None))
                continue
                
            lower = text.lower().strip()
            if any(end in lower for end in ["stop", "goodbye", "bye"]):
                self.message_queue.put(("conversation_end", text))
                break
                
            self.message_queue.put(("speech_received", text))
            response = self.llm_manager.generate_response(text)
            self.message_queue.put(("response_generated", (text, response)))

    def process_messages(self):
        while not self.message_queue.empty():
            msg, data = self.message_queue.get_nowait()
            if msg == "wake_word_detected":
                self.handle_wake_word_detected(data)
            elif msg == "listening_start":
                self.handle_listening_start()
            elif msg == "listening_end":
                self.handle_listening_end()
            elif msg == "listening_failed":
                self.handle_listening_failed()
            elif msg == "speech_received":
                self.handle_speech_received(data)
            elif msg == "response_generated":
                text, response = data
                self.handle_response_generated((text, response))
                self.handle_speaking_start(response)
                threading.Thread(target=self._speak_then_ready, args=(response,), daemon=True).start()
            elif msg == "speaking_end":
                self.handle_speaking_end()
            elif msg == "conversation_end":
                self.handle_conversation_end(data)
        if not self.shutdown_requested:
            self.root.after(100, self.process_messages)

    def _speak_then_ready(self, response):
        try:
            try:
                self.audio_manager.stop_recording()
            except:
                pass
            self.tts_engine.speak(response, blocking=True)
        finally:
            self.message_queue.put(("speaking_end", None))

    def handle_wake_word_detected(self, text):
        if not self.mic_enabled:
            return
        self.conversation_active = True
        self.wake_word_listening = False
        self.status_label.config(text="🎉 Wake word detected! Starting conversation...")
        self.visual_indicator.config(text="🟢", fg="#00ff7f")
        threading.Thread(target=self.continuous_conversation_worker, daemon=True).start()
        
        greeting = "Hi! I'm Vaisiri, your personal voice assistant."
        self.handle_speaking_start(greeting)
        threading.Thread(target=self._speak_then_ready, args=(greeting,), daemon=True).start()

    def handle_listening_start(self):
        if not self.is_speaking and self.mic_enabled:
            self.is_listening = True
            self.visual_indicator.config(text="🔴", fg="#ff4757")
            self.status_label.config(text="🎤 Listening... Speak now!")
            self.show_animation()

    def handle_listening_end(self):
        if not self.is_speaking:
            self.is_listening = False
            self.visual_indicator.config(text="🟡", fg="#ffa502")
            self.status_label.config(text="🤔 Processing with...")
            self.hide_animation()

    def handle_listening_failed(self):
        if not self.is_speaking:
            self.visual_indicator.config(text="🟢", fg="#00ff7f")
            self.status_label.config(text="❌ Didn't catch that. Try again!")
            self.hide_animation()

    def handle_speech_received(self, text):
        if not self.is_speaking:
            display_text = text if len(text) < 60 else text[:60] + "..."
            self.current_response.config(text=f"You asked: '{display_text}'")

    def handle_response_generated(self, data):
        if not self.is_speaking:
            _, response = data
            display = response if len(response) < 150 else response[:150] + "..."
            self.current_response.config(text=f"Response ready: {display}")

    def handle_speaking_start(self, response):
        self.is_speaking = True
        self.is_listening = False
        self.hide_animation()
        
        self.visual_indicator.config(text="🔊", fg="#00ff00")
        self.status_label.config(text="🗣️ Speaking response...")
        display = response if len(response) < 150 else response[:150] + "..."
        self.current_response.config(text=f"Speaking: {display}")

    def handle_speaking_end(self):
        self.is_speaking = False
        if self.mic_enabled:
            self.visual_indicator.config(text="🟢", fg="#00ff7f")
            self.status_label.config(text="🎧 Ready for your next question...")
        time.sleep(0.3)

    def handle_conversation_end(self, text):
        self.conversation_active = False
        self.wake_word_listening = self.mic_enabled
        self.current_response.config(text="Session ended. Say 'vaisiri' to talk again.")
        
        if self.mic_enabled:
            self.status_label.config(text="🎧 Listening for wake word 'vaisiri'...")
            self.visual_indicator.config(text="🎤", fg="#4da6ff")
        
        goodbye = "Goodbye! Feel free to ask anytime."
        self.handle_speaking_start(goodbye)
        threading.Thread(target=self._speak_then_ready, args=(goodbye,), daemon=True).start()

    def show_animation(self):
        def animate(i=0):
            if not self.is_listening or self.is_speaking:
                return
            for dot in self.dot_labels:
                dot.config(fg="#2a2f36")
            self.dot_labels[i].config(fg="#4da6ff")
            self.root.after(300, lambda: animate((i+1) % len(self.dot_labels)))
        animate()

    def hide_animation(self):
        for dot in self.dot_labels:
            dot.config(fg="#0f1419")

    def on_closing(self):
        self.shutdown_requested = True
        try:
            self.tts_engine.stop_speaking()
        except:
            pass
        self.root.destroy()

    def run(self):
        self.root.mainloop()
