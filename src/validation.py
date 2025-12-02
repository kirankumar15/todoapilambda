import re
from typing import Dict, List, Any, Optional
from datetime import datetime

class TodoValidator:
    def __init__(self, max_title_length: int = 200):
        self.max_title_length = max_title_length
        self.title_pattern = re.compile(r'^[a-zA-Z0-9\s\-_.,!?()]+$')
    
    def validate_todo_data(self, data: Dict[str, Any], /) -> Dict[str, List[str]]:
        """Validate todo data using Python 3.8 assignment expressions."""
        errors = {}
        
        # Title validation with walrus operator
        if not (title := data.get('title', '').strip()):
            errors['title'] = ['Title is required']
        elif len(title) > self.max_title_length:
            errors['title'] = [f'Title too long (max {self.max_title_length} chars)']
        elif not self.title_pattern.match(title):
            errors['title'] = ['Title contains invalid characters']
        
        # Completed field validation
        if 'completed' in data and not isinstance(completed := data['completed'], bool):
            errors['completed'] = [f'Expected boolean, got {type(completed).__name__}']
        
        # Date validation with assignment expression
        for field in ['created_at', 'updated_at']:
            if field in data and (date_str := data[field]):
                try:
                    datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                except ValueError:
                    errors.setdefault(field, []).append(f'Invalid date format: {date_str}')
        
        return errors
    
    def validate_batch(self, todos: List[Dict[str, Any]], /) -> Dict[int, Dict[str, List[str]]]:
        """Validate multiple todos with index tracking."""
        batch_errors = {}
        
        # Using assignment expression in comprehension (Python 3.8)
        for i, todo in enumerate(todos):
            if errors := self.validate_todo_data(todo):
                batch_errors[i] = errors
        
        return batch_errors
    
    def sanitize_title(self, title: str, /) -> str:
        """Sanitize title with debugging info."""
        original_length = len(title)
        
        # Strip and normalize whitespace
        if cleaned := title.strip():
            cleaned = re.sub(r'\s+', ' ', cleaned)
        
        # Debug output using f-string = (Python 3.8)
        print(f"Title sanitization: {original_length=}, {len(cleaned)=}")
        
        return cleaned[:self.max_title_length] if cleaned else ''
    
    def check_duplicate_titles(self, todos: List[Dict[str, Any]], /) -> Optional[Dict[str, List[int]]]:
        """Find duplicate titles using assignment expressions."""
        title_indices = {}
        
        for i, todo in enumerate(todos):
            if title := todo.get('title', '').strip().lower():
                title_indices.setdefault(title, []).append(i)
        
        # Return only duplicates using walrus operator
        return {title: indices for title, indices in title_indices.items() 
                if len(indices) > 1} or None
    
    def validate_with_context(self, data: Dict[str, Any], existing_todos: List[Dict[str, Any]], /) -> Dict[str, Any]:
        """Comprehensive validation with context awareness."""
        result = {
            'errors': self.validate_todo_data(data),
            'warnings': [],
            'suggestions': []
        }
        
        # Check for similar titles using assignment expression
        if title := data.get('title', '').strip():
            similar = [
                todo['title'] for todo in existing_todos
                if (similarity := self._calculate_similarity(title, todo.get('title', ''))) > 0.8
            ]
            
            if similar:
                result['warnings'].append(f'Similar titles found: {similar[:3]}')
        
        return result
    
    def _calculate_similarity(self, title1: str, title2: str, /) -> float:
        """Simple similarity calculation."""
        if not title1 or not title2:
            return 0.0
        
        words1 = set(title1.lower().split())
        words2 = set(title2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
