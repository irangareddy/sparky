"""
Sparky Utilities
Common constants, exceptions, and helper functions
"""

from .constants import (
    MovementDirection,
    MovementQuality, 
    ConnectionMethod,
    DEFAULT_SPEED,
    DEFAULT_DURATION,
    MAX_SPEED,
    MIN_SPEED
)

from .exceptions import (
    SparkyError,
    ConnectionError,
    RobotControlError,
    DataCollectionError,
    ConfigurationError,
    TimeoutError
)

__all__ = [
    # Constants
    "MovementDirection",
    "MovementQuality",
    "ConnectionMethod",
    "DEFAULT_SPEED",
    "DEFAULT_DURATION", 
    "MAX_SPEED",
    "MIN_SPEED",
    
    # Exceptions
    "SparkyError",
    "ConnectionError",
    "RobotControlError",
    "DataCollectionError",
    "ConfigurationError",
    "TimeoutError"
]