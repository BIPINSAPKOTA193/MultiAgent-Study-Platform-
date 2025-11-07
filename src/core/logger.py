"""Centralized logging system with Streamlit support"""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime


class StreamlitHandler(logging.Handler):
    """Custom handler to mirror logs to Streamlit"""
    
    def __init__(self):
        super().__init__()
        self.logs = []
        self.max_logs = 100  # Keep last 100 logs
    
    def emit(self, record):
        """Emit log record to Streamlit-compatible format"""
        log_entry = self.format(record)
        self.logs.append(log_entry)
        
        # Keep only last max_logs entries
        if len(self.logs) > self.max_logs:
            self.logs.pop(0)
    
    def get_logs(self, level: Optional[str] = None) -> list:
        """Get logs, optionally filtered by level"""
        if level:
            return [log for log in self.logs if level.upper() in log]
        return self.logs
    
    def clear(self):
        """Clear stored logs"""
        self.logs = []


class Logger:
    """Centralized logger for the platform"""
    
    _instance: Optional['Logger'] = None
    _logger: Optional[logging.Logger] = None
    _streamlit_handler: Optional[StreamlitHandler] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._logger is None:
            self._setup_logger()
    
    def _setup_logger(self):
        """Setup logger with file and console handlers"""
        self._logger = logging.getLogger("multiagent_learn")
        self._logger.setLevel(logging.DEBUG)
        
        # Avoid duplicate handlers
        if self._logger.handlers:
            return
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_format)
        self._logger.addHandler(console_handler)
        
        # File handler
        log_dir = Path(__file__).parent.parent.parent / "logs"
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        self._logger.addHandler(file_handler)
        
        # Streamlit handler
        self._streamlit_handler = StreamlitHandler()
        self._streamlit_handler.setLevel(logging.INFO)
        self._streamlit_handler.setFormatter(console_format)
        self._logger.addHandler(self._streamlit_handler)
    
    def get_logger(self) -> logging.Logger:
        """Get the underlying logger"""
        return self._logger
    
    def get_streamlit_logs(self, level: Optional[str] = None) -> list:
        """Get logs for Streamlit display"""
        if self._streamlit_handler:
            return self._streamlit_handler.get_logs(level)
        return []
    
    def clear_streamlit_logs(self):
        """Clear Streamlit log buffer"""
        if self._streamlit_handler:
            self._streamlit_handler.clear()
    
    def debug(self, message: str):
        """Log debug message"""
        self._logger.debug(message)
    
    def info(self, message: str):
        """Log info message"""
        self._logger.info(message)
    
    def warning(self, message: str):
        """Log warning message"""
        self._logger.warning(message)
    
    def error(self, message: str):
        """Log error message"""
        self._logger.error(message)
    
    def exception(self, message: str):
        """Log exception with traceback"""
        self._logger.exception(message)


# Global logger instance
logger = Logger()

