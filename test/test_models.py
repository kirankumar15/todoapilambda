import unittest
from datetime import datetime
from src.models import Todo

class TestTodoModel(unittest.TestCase):
    
    def test_todo_creation(self):
        todo = Todo(title="Test todo")
        
        self.assertEqual(todo.title, "Test todo")
        self.assertFalse(todo.completed)
        self.assertIsNotNone(todo.id)
        self.assertIsNotNone(todo.created_at)
        self.assertIsNotNone(todo.updated_at)
    
    def test_todo_update(self):
        todo = Todo(title="Original")
        original_updated = todo.updated_at
        
        todo.update(title="Updated", completed=True)
        
        self.assertEqual(todo.title, "Updated")
        self.assertTrue(todo.completed)
        self.assertNotEqual(todo.updated_at, original_updated)
    
    def test_todo_to_dict(self):
        todo = Todo(title="Test")
        data = todo.to_dict()
        
        self.assertIn('id', data)
        self.assertIn('title', data)
        self.assertIn('completed', data)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)
    
    def test_todo_from_dict(self):
        data = {
            'title': 'Test',
            'completed': True,
            'id': 'test-id'
        }
        todo = Todo.from_dict(data)
        
        self.assertEqual(todo.title, 'Test')
        self.assertTrue(todo.completed)
        self.assertEqual(todo.id, 'test-id')

if __name__ == '__main__':
    unittest.main()
