"""
Enhanced LLM Manager with Gemini 2.5 Flash-Lite Integration
Priority: Knowledge Base → Gemini → Intelligent Fallback
"""
import os
from ..utils.logger import logger

# Import Gemini client
try:
    from .remote_gemini import RemoteGemini
except ImportError:
    RemoteGemini = None

class LLMManager:
    """KB → Gemini 2.5 Flash-Lite → Fallback"""

    def __init__(self, config):
        self.config = config
        self.gemini = RemoteGemini() if RemoteGemini else None
        
        if self.gemini and self.gemini.enabled:
            print("✅ LLM Manager initialized - KB + Gemini 2.5 Flash-Lite ready!")
        else:
            print("✅ LLM Manager initialized - KB + Fallback only")

    def generate_response(self, user_input: str) -> str:
        """Generate response with priority system"""
        ui = (user_input or "").strip()
        if not ui:
            return "I'm here to help! What would you like to know?"

        # Priority 1: Knowledge Base (instant)
        kb_response = self._get_knowledge_base_response(ui)
        if kb_response:
            return kb_response

        # Priority 2: Gemini API (intelligent)
        if self.gemini and self.gemini.enabled:
            gemini_response = self.gemini.generate(ui)
            if gemini_response and self._is_quality_response(gemini_response):
                return gemini_response

        # Priority 3: Intelligent Fallback
        return self._generate_intelligent_fallback(ui)

    def _get_knowledge_base_response(self, user_input: str) -> str | None:
        """Enhanced Knowledge Base with common questions"""
        u = user_input.lower().strip()

        # === IDENTITY & CAPABILITIES ===
        if any(k in u for k in ["what is your name", "who are you", "what are you"]):
            return "I'm Vaisiri, an AI assistant."

        if any(k in u for k in ["what can you do", "your capabilities", "help me"]):
            return "I can answer questions about science, technology, programming, engineering, mathematics, business, and education. Ask me anything!"

        # === CORE SUBJECTS ===
        if any(k in u for k in ["what is computer science", "computer science"]):
            return "Computer Science studies algorithms, programming, software systems, and AI to solve problems using computers and technology."

        if any(k in u for k in ["what is programming", "define programming"]):
            return "Programming is writing step-by-step instructions for computers using languages like Python, Java, or JavaScript to create software and applications."

        if any(k in u for k in ["what is python", "define python"]):
            return "Python is a popular, readable programming language used for web development, data analysis, artificial intelligence, and automation."

        if any(k in u for k in ["what is java", "define java"]):
            return "Java is an object-oriented programming language that runs on any device with the Java Virtual Machine, popular for enterprise and Android apps."

        if any(k in u for k in ["what is artificial intelligence", "what is ai", "define ai"]):
            return "AI enables machines to perform tasks requiring human intelligence, like learning, reasoning, and pattern recognition."

        if any(k in u for k in ["what is science", "define science"]):
            return "Science is the systematic study of the natural world through observation, experimentation, and evidence to understand how things work."

        if any(k in u for k in ["what is education", "define education"]):
            return "Education is the process of learning knowledge, skills, and values through teaching, study, and experience to develop understanding."

        # === TECHNOLOGY ===
        if any(k in u for k in ["what is computer", "define computer"]):
            return "A computer is an electronic device that processes data using hardware and software to perform calculations, run applications, and communicate."

        if any(k in u for k in ["what is cloud computing", "cloud computing"]):
            return "Cloud computing delivers computing services like storage, processing, and software over the internet, accessible from anywhere without local hardware."

        # === UTILITIES ===
        if any(k in u for k in ["time", "current time", "what time"]):
            from datetime import datetime
            now = datetime.now()
            return f"The current time is {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d, %Y')}."

        # === SOCIAL ===
        if any(k in u for k in ["hello", "hi", "hey", "greetings"]):
            return "Hello! I'm excited to help you learn. What would you like to know about—science, technology, programming, or something else?"

        if any(k in u for k in ["thank you", "thanks", "appreciate"]):
            return "You're very welcome! I'm always happy to help with questions and learning. Feel free to ask me anything else!"

        if any(k in u for k in ["joke", "tell me a joke", "funny"]):
            import random
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "How do you comfort a JavaScript bug? You console it!",
                "What's a computer's favorite snack? Microchips!",
                "Why did the computer keep sneezing? It had a virus!"
            ]
            return random.choice(jokes)

        # No KB match
        return None

    def _generate_intelligent_fallback(self, user_input: str) -> str:
        """Smart fallback responses"""
        u = user_input.lower()
        
        if any(word in u for word in ["learn", "study", "education", "school"]):
            return "Learning is most effective with active practice and curiosity. What specific subject would you like help with?"
        
        if any(word in u for word in ["career", "job", "work", "profession"]):
            return "Career success comes from developing skills, building projects, and continuous learning. Which field interests you most?"
        
        if any(word in u for word in ["technology", "tech", "computer", "software"]):
            return "Technology is rapidly evolving with AI, cloud computing, and automation. What aspect would you like to explore?"
        
        if any(word in u for word in ["science", "research", "discovery"]):
            return "Science helps us understand the world through observation and experimentation. What scientific topic interests you?"
        
        return f"That's an interesting question about '{user_input}'. I'd be happy to help explain it further. Could you provide more specific details about what you'd like to know?"

    def _is_quality_response(self, response: str) -> bool:
        """Check if response meets quality standards"""
        if not response or len(response.strip()) < 15:
            return False
        
        # Filter out poor responses
        bad_phrases = [
            "i don't know",
            "i'm not sure",
            "i can't help",
            "no information",
            "unable to provide"
        ]
        
        return not any(phrase in response.lower() for phrase in bad_phrases)
