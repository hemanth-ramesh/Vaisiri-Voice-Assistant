"""
Logging utilities for Vaisiri Voice Assistant
"""
import logging
import sys

class VaisiriLogger:
    """Simple logger for Vaisiri Voice Assistant"""
    
    def __init__(self, name: str = "vaisiri", level: str = "INFO"):
        """Initialize logger"""
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            
    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)
        
    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)
        
    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)

# Global logger instance
logger = VaisiriLogger()

def setup_logger(config):
    """Setup logger with configuration"""
    try:
        level = config.get("logging.level", "INFO")
        return VaisiriLogger(level=level)
    except:
        return VaisiriLogger()
