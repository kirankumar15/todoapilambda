import unittest
from src.mock_todo_service import MockTodoService

class TestTodoService(unittest.TestCase):
    
    def setUp(self):
        self.service = MockTodoService()
    
    def test_create_todo(self):
        todo = self.service.create("Test todo")
        
        self.assertEqual(todo['title'], "Test todo")
        self.assertFalse(todo['completed'])
        self.assertIn('id', todo)
    
    def test_create_empty_title_raises_error(self):
        with self.assertRaises(ValueError):
            self.service.create("")
    
    def test_get_all_todos(self):
        self.service.create("Todo 1")
        self.service.create("Todo 2")
        
        todos = self.service.get_all()
        self.assertEqual(len(todos), 2)
    
    def test_get_todos_by_completion_status(self):
        todo1 = self.service.create("Todo 1")
        todo2 = self.service.create("Todo 2")
        
        self.service.update(todo1['id'], completed=True)
        
        completed = self.service.get_all(completed=True)
        incomplete = self.service.get_all(completed=False)
        
        self.assertEqual(len(completed), 1)
        self.assertEqual(len(incomplete), 1)
    
    def test_update_todo(self):
        todo = self.service.create("Original")
        updated = self.service.update(todo['id'], title="Updated", completed=True)
        
        self.assertEqual(updated['title'], "Updated")
        self.assertTrue(updated['completed'])
    
    def test_delete_todo(self):
        todo = self.service.create("To delete")
        result = self.service.delete(todo['id'])
        
        self.assertTrue(result)
        self.assertIsNone(self.service.get_by_id(todo['id']))
    
    def test_delete_nonexistent_todo(self):
        result = self.service.delete("nonexistent")
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
