from enum import Enum


from .MessageConstans import logger

class MessageImportance(Enum):
    """Enum class"""
    logger.start()
    LOW = 10
    MEDIUM = 20
    HIGH = 30
    logger.end()
