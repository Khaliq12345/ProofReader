from loguru import logger
import os
from src.core import config

# Ensure logs directory exists
os.makedirs(config.LOG_DIR, exist_ok=True)

# Remove default sink (stderr) to customize logging
logger.remove()

# General application logs (INFO and above)
logger.add(
    os.path.join(config.LOG_DIR, "app.log"),
    level="INFO",
    rotation="5 MB",  # Rotate when file reaches 5 MB
    retention="30 days",  # Keep logs for 30 days
    compression="zip",  # Compress rotated logs
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module} | {message}",
)

# Error-specific logs (ERROR and above)
logger.add(
    os.path.join(config.LOG_DIR, "error.log"),
    level="ERROR",
    rotation="5 MB",
    retention="30 days",
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module} | {message} | {extra}",
    backtrace=True,  # Include stack traces for errors
    diagnose=True,  # Include variable values (disable in production if sensitive)
)
