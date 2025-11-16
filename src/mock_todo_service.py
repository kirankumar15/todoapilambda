from typing import List, Optional, Dict, Any
from .models import Todo

class MockTodoService:
    """Mock TodoService for testing without DynamoDB dependency."""
    
    def __init__(self, table_name: str = 'todos'):
        self._todos: Dict[str, Todo] = {}
    
    def get_all(self, /, completed: Optional[bool] = None) -> List[Dict[str, Any]]:
        todos = list(self._todos.values())
        if completed is not None:
            todos = [t for t in todos if t.completed == completed]
        return sorted([todo.to_dict() for todo in todos], key=lambda x: x['created_at'])
    
    def get_by_id(self, todo_id: str, /) -> Optional[Dict[str, Any]]:
        if todo := self._todos.get(todo_id):
            return todo.to_dict()
        return None
    
    def create(self, title: str, /) -> Dict[str, Any]:
        if not (title := title.strip()):
            raise ValueError("Title cannot be empty")
        
        todo = Todo(title=title)
        self._todos[todo.id] = todo
        return todo.to_dict()
    
    def update(self, todo_id: str, /, **updates) -> Optional[Dict[str, Any]]:
        if todo := self._todos.get(todo_id):
            todo.update(**updates)
            return todo.to_dict()
        return None
    
    def delete(self, todo_id: str, /) -> bool:
        return self._todos.pop(todo_id, None) is not None
    
    def clear_all(self) -> None:
        self._todos.clear()
