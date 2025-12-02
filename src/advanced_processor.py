from typing import Dict, List, Any, Union, Optional
from .protocols import TodoProcessor, TodoStorage, TodoAnalyzer
from .constants import DEFAULT_CONFIG, ERROR_MESSAGES, VALIDATION_MODES

class AdvancedTodoProcessor:
    """Advanced processor that uses protocol-based dependencies."""
    
    def __init__(self, 
                 storage: TodoStorage,
                 analyzer: TodoAnalyzer, 
                 processor: TodoProcessor,
                 /,
                 *,
                 config: Optional[Dict[str, Any]] = None):
        self._storage = storage
        self._analyzer = analyzer  
        self._processor = processor
        self._config = config or DEFAULT_CONFIG.copy()
    
    def process_with_validation(self, 
                              todos: List[Dict[str, Any]], 
                              /,
                              *,
                              mode: VALIDATION_MODES = 'strict') -> Dict[str, Any]:
        """Process todos with protocol-based validation."""
        
        # Validate using protocol methods
        valid_todos = []
        errors = []
        
        for i, todo in enumerate(todos):
            if self._processor.validate_input(todo):
                valid_todos.append(todo)
            else:
                errors.append({
                    'index': i,
                    'todo': todo,
                    'error': ERROR_MESSAGES['TITLE_REQUIRED']
                })
        
        # Process valid todos
        results = {
            'processed': self._processor.process(valid_todos),
            'analysis': self._analyzer.analyze_batch(valid_todos) if valid_todos else {},
            'errors': errors,
            'validation_mode': mode
        }
        
        # Store results if configured
        if self._config.get('cache_results', False):
            for todo in valid_todos:
                if todo_id := self._storage.save(todo):
                    results.setdefault('stored_ids', []).append(todo_id)
        
        return results
    
    def get_stored_todo(self, todo_id: str, /) -> Optional[Dict[str, Any]]:
        """Retrieve stored todo using protocol method."""
        return self._storage.load(todo_id)
    
    def cleanup_storage(self, todo_ids: List[str], /) -> Dict[str, bool]:
        """Clean up stored todos using protocol methods."""
        return {
            todo_id: self._storage.delete(todo_id) 
            for todo_id in todo_ids
        }
    
    def validate_protocols(self) -> Dict[str, bool]:
        """Validate that all dependencies implement required protocols."""
        from .protocols import ProtocolValidator
        
        validator = ProtocolValidator()
        return validator.validate_all(
            self._processor,
            self._storage, 
            self._analyzer
        )
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information using protocol introspection."""
        return {
            'storage_type': type(self._storage).__name__,
            'analyzer_type': type(self._analyzer).__name__,
            'processor_type': type(self._processor).__name__,
            'config': self._config,
            'protocol_compliance': self.validate_protocols()
        }
