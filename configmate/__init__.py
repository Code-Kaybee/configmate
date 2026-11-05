"""ConfigMate - Advanced configuration management utility."""

from .config import Config, ValidationError
from .stellar import StellarConfig, StellarEndpointError

# Convenience instance
config = Config()

# Public API
__all__ = [
    "Config",
    "ValidationError",
    "StellarConfig",
    "StellarEndpointError",
    "config",
]