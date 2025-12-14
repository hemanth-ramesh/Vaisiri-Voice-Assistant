"""
Gemini 2.5 Flash-Lite Client for Vaisiri
High-throughput, concise responses optimized for voice assistant
"""
import os
import time
import hashlib
import json

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

class RemoteGemini:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY", "").strip()
        self.model_name = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash-lite")
        self.max_tokens = int(os.environ.get("GEMINI_MAX_TOKENS", "200"))
        self.temperature = float(os.environ.get("GEMINI_TEMPERATURE", "0.7"))
        
        self.enabled = bool(self.api_key and GEMINI_AVAILABLE)
        self.model = None
        self.cache = {}  # Simple in-memory cache
        
        if self.enabled:
            self._initialize_client()
        else:
            print("⚠️ Gemini not available (missing API key or SDK)")

    def _initialize_client(self):
        """Initialize Gemini client with optimized settings"""
        try:
            genai.configure(api_key=self.api_key)
            
            generation_config = {
                "temperature": self.temperature,
                "top_p": 0.9,
                "top_k": 40,
                "max_output_tokens": self.max_tokens,
                "response_mime_type": "text/plain"
            }
            
            system_instruction = (
                "You are Vaisiri, an educational AI assistant from Vaisiri Institute. "
                "Give clear, helpful answers in 2-3 sentences maximum. "
                "Be conversational but informative. Focus on practical, accurate information."
            )
            
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=generation_config,
                system_instruction=system_instruction
            )
            
            print(f"✅ Gemini {self.model_name} client initialized")
            
        except Exception as e:
            print(f"❌ Gemini initialization failed: {e}")
            self.enabled = False
            self.model = None

    def generate(self, user_input: str) -> str | None:
        """Generate response with caching and error handling"""
        if not self.enabled or not self.model or not user_input.strip():
            return None
        
        try:
            # Check cache first
            cache_key = hashlib.md5(user_input.lower().encode()).hexdigest()
            if cache_key in self.cache:
                cached_time, cached_response = self.cache[cache_key]
                if time.time() - cached_time < 300:  # 5 minutes cache
                    print("✅ Using cached response")
                    return cached_response
            
            # Generate new response
            prompt = f"Question: {user_input.strip()}\n\nPlease provide a clear, concise answer:"
            
            response = self.model.generate_content(prompt)
            
            if response and hasattr(response, 'text') and response.text:
                text = response.text.strip()
                
                # Clean and format response
                text = self._clean_response(text)
                
                if text and len(text) > 10:
                    # Cache the response
                    self.cache[cache_key] = (time.time(), text)
                    
                    # Limit cache size
                    if len(self.cache) > 100:
                        oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k][0])
                        del self.cache[oldest_key]
                    
                    return text
            
            return None
            
        except Exception as e:
            print(f"❌ Gemini API error: {e}")
            if "429" in str(e):
                print("⚠️ Rate limit reached - falling back")
            return None

    def _clean_response(self, text: str) -> str:
        """Clean and optimize response for TTS"""
        if not text:
            return ""
        
        # Remove markdown and formatting
        text = text.replace("**", "").replace("*", "")
        text = text.replace("#", "").replace("`", "")
        
        # Remove newlines and extra spaces
        text = " ".join(text.split())
        
        # Ensure it ends with punctuation
        if text and text[-1] not in '.!?':
            text += "."
        
        # Limit length for TTS
        if len(text) > 300:
            sentences = text.split('. ')
            if len(sentences) > 2:
                text = '. '.join(sentences[:2]) + "."
        
        return text
