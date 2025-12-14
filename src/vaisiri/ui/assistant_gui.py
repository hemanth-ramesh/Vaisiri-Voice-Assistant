"""
Modern Google Assistant-style UI for Vaisiri Voice Assistant
"""
import tkinter as tk
from tkinter import ttk
import threading
import time
from datetime import datetime
import math

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Import Vaisiri core components
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


class VaisiriAssistantGUI:
    """Modern Google Assistant-style GUI"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_components()
        self.setup_ui()
        self.setup_bindings()
        
        # State variables
        self.listening = False
        self.session_active = False
        self.last_response = ""
        self.animation_running = False
        
    def setup_window(self):
        """Configure main window"""
        self.root.title("Vaisiri Assistant")
        self.root.geometry("400x600")
        self.root.configure(bg="#0f1419")  # Dark theme like Google Assistant
        self.root.resizable(True, True)
        
        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def setup_components(self):
        """Initialize Vaisiri components"""
        try:
            print("🔧 Initializing Vaisiri components...")
            self.config = Config()
            self.audio_manager = AudioManager(self.config)
            self.wake_word_detector = WakeWordDetector(self.config)
            self.stt_engine = SpeechToTextEngine(self.config)
            self.llm_manager = LLMManager(self.config)
            self.tts_engine = TextToSpeechEngine(self.config)
            print("✅ All components initialized!")
        except Exception as e:
            print(f"❌ Component initialization failed: {e}")
            
    def setup_ui(self):
        """Create the modern UI"""
        # Main container
        main_frame = tk.Frame(self.root, bg="#0f1419")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header with app name
        header_frame = tk.Frame(main_frame, bg="#0f1419")
        header_frame.pack(fill="x", pady=(0, 30))
        
        title_label = tk.Label(
            header_frame, 
            text="Vaisiri", 
            font=("Segoe UI", 28, "bold"),
            fg="#ffffff", 
            bg="#0f1419"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Your AI Assistant",
            font=("Segoe UI", 12),
            fg="#8e9aaf",
            bg="#0f1419"
        )
        subtitle_label.pack()
        
        # Status display
        self.status_frame = tk.Frame(main_frame, bg="#0f1419")
        self.status_frame.pack(fill="x", pady=(0, 20))
        
        self.status_label = tk.Label(
            self.status_frame,
            text="Ready to help!",
            font=("Segoe UI", 14),
            fg="#4fc3f7",
            bg="#0f1419"
        )
        self.status_label.pack()
        
        # Microphone button (large, Google Assistant style)
        self.mic_frame = tk.Frame(main_frame, bg="#0f1419")
        self.mic_frame.pack(expand=True)
        
        # Create circular mic button
        self.mic_button = tk.Button(
            self.mic_frame,
            text="🎤",
            font=("Segoe UI", 48),
            width=4,
            height=2,
            bg="#4fc3f7",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.toggle_listening
        )
        self.mic_button.pack()
        
        # Listening animation (dots)
        self.animation_frame = tk.Frame(main_frame, bg="#0f1419")
        self.animation_frame.pack(pady=20)
        
        self.dot_labels = []
        for i in range(3):
            dot = tk.Label(
                self.animation_frame,
                text="●",
                font=("Segoe UI", 16),
                fg="#4fc3f7",
                bg="#0f1419"
            )
            dot.pack(side="left", padx=5)
            self.dot_labels.append(dot)
            
        # Response area
        response_frame = tk.Frame(main_frame, bg="#0f1419")
        response_frame.pack(fill="both", expand=True, pady=(20, 0))
        
        tk.Label(
            response_frame,
            text="Last Response:",
            font=("Segoe UI", 12, "bold"),
            fg="#ffffff",
            bg="#0f1419"
        ).pack(anchor="w")
        
        # Response text with scrollbar
        text_frame = tk.Frame(response_frame, bg="#0f1419")
        text_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        self.response_text = tk.Text(
            text_frame,
            wrap="word",
            height=6,
            font=("Segoe UI", 11),
            bg="#1e2328",
            fg="#ffffff",
            relief="flat",
            padx=15,
            pady=15
        )
        
        scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=self.response_text.yview)
        self.response_text.configure(yscrollcommand=scrollbar.set)
        
        self.response_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Control buttons
        control_frame = tk.Frame(main_frame, bg="#0f1419")
        control_frame.pack(fill="x", pady=(20, 0))
        
        # Wake word toggle
        self.wake_button = tk.Button(
            control_frame,
            text="Wake Word: ON",
            font=("Segoe UI", 10),
            bg="#2d3748",
            fg="#ffffff",
            relief="flat",
            padx=15,
            pady=5,
            command=self.toggle_wake_word
        )
        self.wake_button.pack(side="left")
        
        # Settings button
        settings_button = tk.Button(
            control_frame,
            text="⚙️",
            font=("Segoe UI", 14),
            bg="#2d3748",
            fg="#ffffff",
            relief="flat",
            width=3,
            height=1,
            command=self.show_settings
        )
        settings_button.pack(side="right")
        
        # Initially hide animation
        self.hide_animation()
        
    def setup_bindings(self):
        """Setup keyboard shortcuts and events"""
        self.root.bind("<space>", lambda e: self.toggle_listening())
        self.root.bind("<Escape>", lambda e: self.stop_listening())
        self.root.focus_set()  # Allow keyboard shortcuts
        
    def toggle_listening(self):
        """Toggle listening state"""
        if not self.listening:
            self.start_listening()
        else:
            self.stop_listening()
            
    def start_listening(self):
        """Start listening for voice input"""
        if self.listening:
            return
            
        self.listening = True
        self.session_active = True
        
        # Update UI
        self.mic_button.configure(bg="#ff4444", text="⏹️")
        self.status_label.configure(text="Listening... Speak now!", fg="#ff4444")
        self.show_animation()
        
        # Start listening in background thread
        threading.Thread(target=self._listen_worker, daemon=True).start()
        
    def stop_listening(self):
        """Stop listening"""
        self.listening = False
        self.mic_button.configure(bg="#4fc3f7", text="🎤")
        self.status_label.configure(text="Processing...", fg="#ffa726")
        self.hide_animation()
        
    def _listen_worker(self):
        """Background worker for voice recognition"""
        try:
            # Listen for speech
            text, success = self.stt_engine.listen_and_transcribe(self.audio_manager, duration=5.0)
            
            if success and text:
                # Update UI on main thread
                self.root.after(0, self._process_speech, text)
            else:
                self.root.after(0, self._listening_failed)
                
        except Exception as e:
            print(f"❌ Listening error: {e}")
            self.root.after(0, self._listening_failed)
            
    def _process_speech(self, text):
        """Process recognized speech"""
        self.status_label.configure(text=f"You said: {text}", fg="#4fc3f7")
        
        # Generate response in background
        threading.Thread(target=self._generate_response, args=(text,), daemon=True).start()
        
    def _generate_response(self, text):
        """Generate AI response"""
        try:
            response = self.llm_manager.generate_response(text)
            
            # Update UI on main thread
            self.root.after(0, self._display_response, text, response)
            
            # Speak response
            self.tts_engine.speak(response)
            
        except Exception as e:
            print(f"❌ Response generation error: {e}")
            self.root.after(0, self._response_failed)
            
    def _display_response(self, question, response):
        """Display the response in UI"""
        self.last_response = response
        
        # Clear and update response text
        self.response_text.delete(1.0, tk.END)
        self.response_text.insert(1.0, f"You: {question}\n\nVaisiri: {response}")
        
        # Update status
        self.status_label.configure(text="Ready for next question!", fg="#4fc3f7")
        self._reset_listening_state()
        
    def _listening_failed(self):
        """Handle listening failure"""
        self.status_label.configure(text="Didn't catch that. Try again!", fg="#ff9800")
        self._reset_listening_state()
        
    def _response_failed(self):
        """Handle response generation failure"""
        self.status_label.configure(text="Sorry, had trouble with that.", fg="#ff9800")
        self._reset_listening_state()
        
    def _reset_listening_state(self):
        """Reset UI to ready state"""
        self.listening = False
        self.mic_button.configure(bg="#4fc3f7", text="🎤")
        self.hide_animation()
        
    def show_animation(self):
        """Show listening animation"""
        if not self.animation_running:
            self.animation_running = True
            self._animate_dots()
            
    def hide_animation(self):
        """Hide listening animation"""
        self.animation_running = False
        for dot in self.dot_labels:
            dot.configure(fg="#0f1419")  # Hide dots
            
    def _animate_dots(self):
        """Animate listening dots"""
        if not self.animation_running:
            return
            
        # Cycle through dots
        for i, dot in enumerate(self.dot_labels):
            delay = i * 200  # 200ms delay between dots
            self.root.after(delay, lambda d=dot: d.configure(fg="#4fc3f7"))
            self.root.after(delay + 600, lambda d=dot: d.configure(fg="#2d3748"))
            
        # Repeat animation
        self.root.after(1000, self._animate_dots)
        
    def toggle_wake_word(self):
        """Toggle wake word detection"""
        # This would integrate with wake word detection
        current_text = self.wake_button.cget("text")
        if "ON" in current_text:
            self.wake_button.configure(text="Wake Word: OFF", bg="#ff4444")
        else:
            self.wake_button.configure(text="Wake Word: ON", bg="#2d3748")
            
    def show_settings(self):
        """Show settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("300x200")
        settings_window.configure(bg="#0f1419")
        
        tk.Label(
            settings_window,
            text="Settings",
            font=("Segoe UI", 16, "bold"),
            fg="#ffffff",
            bg="#0f1419"
        ).pack(pady=20)
        
        tk.Label(
            settings_window,
            text="• Voice: Female (Zira)\n• Wake Word: 'vimtech'\n• Language: English\n• Theme: Dark",
            font=("Segoe UI", 11),
            fg="#8e9aaf",
            bg="#0f1419",
            justify="left"
        ).pack()
        
    def run(self):
        """Start the GUI application"""
        print("🚀 Starting Vaisiri Assistant GUI...")
        self.root.mainloop()


def main():
    """Entry point for GUI application"""
    app = VaisiriAssistantGUI()
    app.run()


if __name__ == "__main__":
    main()
