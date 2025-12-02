from typing import Protocol, List, Dict, Any, Optional, runtime_checkable
from abc import abstractmethod

@runtime_checkable
class TodoProcessor(Protocol):
    """Protocol for todo processing implementations."""
    
    def process(self, todos: List[Dict[str, Any]], /) -> Dict[str, Any]:
        """Process todos and return results."""
        ...
    
    def validate_input(self, data: Dict[str, Any], /) -> bool:
        """Validate input data structure."""
        ...

@runtime_checkable  
class TodoStorage(Protocol):
    """Protocol for todo storage backends."""
    
    def save(self, todo: Dict[str, Any], /) -> str:
        """Save todo and return ID."""
        ...
    
    def load(self, todo_id: str, /) -> Optional[Dict[str, Any]]:
        """Load todo by ID."""
        ...
    
    def delete(self, todo_id: str, /) -> bool:
        """Delete todo by ID."""
        ...

@runtime_checkable
class TodoAnalyzer(Protocol):
    """Protocol for todo analysis implementations."""
    
    @property
    def metrics(self) -> Dict[str, float]:
        """Get current metrics."""
        ...
    
    def analyze_batch(self, todos: List[Dict[str, Any]], /) -> Dict[str, Any]:
        """Analyze a batch of todos."""
        ...

class ProtocolValidator:
    """Validates objects against protocols at runtime."""
    
    def check_processor(self, obj: Any, /) -> bool:
        """Check if object implements TodoProcessor protocol."""
        return isinstance(obj, TodoProcessor)
    
    def check_storage(self, obj: Any, /) -> bool:
        """Check if object implements TodoStorage protocol.""" 
        return isinstance(obj, TodoStorage)
    
    def check_analyzer(self, obj: Any, /) -> bool:
        """Check if object implements TodoAnalyzer protocol."""
        return isinstance(obj, TodoAnalyzer)
    
    def validate_all(self, processor: Any, storage: Any, analyzer: Any, /) -> Dict[str, bool]:
        """Validate multiple objects against their protocols."""
        return {
            'processor_valid': self.check_processor(processor),
            'storage_valid': self.check_storage(storage), 
            'analyzer_valid': self.check_analyzer(analyzer)
        }

# Concrete implementations for demonstration
class SimpleTodoProcessor:
    """Simple implementation of TodoProcessor protocol."""
    
    def process(self, todos: List[Dict[str, Any]], /) -> Dict[str, Any]:
        completed = sum(1 for t in todos if t.get('completed', False))
        return {
            'total': len(todos),
            'completed': completed,
            'completion_rate': completed / len(todos) if todos else 0.0
        }
    
    def validate_input(self, data: Dict[str, Any], /) -> bool:
        return 'title' in data and isinstance(data['title'], str)

class MemoryTodoStorage:
    """In-memory implementation of TodoStorage protocol."""
    
    def __init__(self):
        self._storage: Dict[str, Dict[str, Any]] = {}
        self._counter = 0
    
    def save(self, todo: Dict[str, Any], /) -> str:
        self._counter += 1
        todo_id = f"todo_{self._counter}"
        self._storage[todo_id] = todo.copy()
        return todo_id
    
    def load(self, todo_id: str, /) -> Optional[Dict[str, Any]]:
        return self._storage.get(todo_id)
    
    def delete(self, todo_id: str, /) -> bool:
        return self._storage.pop(todo_id, None) is not None
