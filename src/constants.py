from typing import Final, Literal

# Python 3.8 Final constants - immutable at runtime
MAX_TITLE_LENGTH: Final[int] = 200
MIN_TITLE_LENGTH: Final[int] = 1
DEFAULT_BATCH_SIZE: Final[int] = 10
MAX_BATCH_SIZE: Final[int] = 100

# Status constants using Literal
TODO_STATUS: Final = Literal['pending', 'completed', 'archived']
PRIORITY_LEVELS: Final = Literal['low', 'medium', 'high', 'urgent']
VALIDATION_MODES: Final = Literal['strict', 'lenient', 'custom']

# Error messages as Final constants
ERROR_MESSAGES: Final[dict] = {
    'TITLE_REQUIRED': 'Title is required and cannot be empty',
    'TITLE_TOO_LONG': f'Title exceeds maximum length of {MAX_TITLE_LENGTH} characters',
    'INVALID_STATUS': 'Status must be pending, completed, or archived',
    'BATCH_TOO_LARGE': f'Batch size cannot exceed {MAX_BATCH_SIZE} items'
}

# Configuration constants
DEFAULT_CONFIG: Final[dict] = {
    'enable_analytics': True,
    'enable_validation': True,
    'enable_batch_processing': True,
    'cache_results': True
}
