import os
import logging
from datetime import datetime


# ===============================
# Main Logger Setup
# ===============================

def setup_application_logger(name: str = __name__, log_level: str = "DEBUG") -> logging.Logger:
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    logger = logging.getLogger(name)
    
    level = getattr(logging, log_level.upper())
    logger.setLevel(level)
    
    if not logger.handlers:
        file_formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
        )
        console_formatter = logging.Formatter(
            '%(levelname)s | %(message)s'
        )
        
        today = datetime.now().strftime('%Y-%m-%d')
        file_handler = logging.FileHandler(
            f"{log_dir}/{today}.log",
            encoding='utf-8'
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.DEBUG)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(level)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger
