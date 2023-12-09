"""
    Runtime validation using type hints.
"""

__version__ = "1.0.0"

from .validation import (TypeInspector, UnsupportedType, can_validate,
                         validate, validation_aliases)
from .validation_failure import (get_validation_failure,
                                 latest_validation_failure)

# re-export all encodings and functions.
__all__ = [
    "validate",
    "can_validate",
    "validation_aliases",
    "TypeInspector",
    "UnsupportedType",
    "get_validation_failure",
    "latest_validation_failure",
]
