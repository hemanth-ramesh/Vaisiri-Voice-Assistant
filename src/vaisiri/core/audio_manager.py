"""
Audio management for Vaisiri Voice Assistant
"""
import pyaudio
import wave
import tempfile
import os

class AudioManager:
    """Manages audio recording"""
    
    def __init__(self, config):
        """Initialize audio manager"""
        self.config = config
        self.audio = pyaudio.PyAudio()
        self.sample_rate = config.get_sample_rate()
        self.chunk_size = config.get_chunk_size()
        self.channels = 1
        self.format = pyaudio.paInt16
        print("AudioManager initialized")
        
    def test_microphone(self) -> bool:
        """Test microphone"""
        try:
            stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            data = stream.read(self.chunk_size)
            stream.stop_stream()
            stream.close()
            print("Microphone test passed")
            return True
        except Exception as e:
            print(f"Microphone test failed: {e}")
            return False
            
    def record_audio_for_duration(self, duration: float) -> bytes:
        """Record audio for specified duration"""
        print(f"Recording for {duration} seconds...")
        
        stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )
        
        frames = []
        for _ in range(0, int(self.sample_rate / self.chunk_size * duration)):
            data = stream.read(self.chunk_size)
            frames.append(data)
            
        stream.stop_stream()
        stream.close()
        
        return b''.join(frames)
        
    def save_audio_to_wav(self, audio_data: bytes, filename: str):
        """Save audio data to WAV file"""
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_data)
            
    def start_recording(self):
        """Start recording (stub)"""
        pass
        
    def stop_recording(self):
        """Stop recording (stub)"""
        pass
