import unittest
from src.validation import TodoValidator

class TestTodoValidator(unittest.TestCase):
    
    def setUp(self):
        self.validator = TodoValidator(max_title_length=50)
    
    def test_validate_valid_todo(self):
        data = {'title': 'Valid todo', 'completed': False}
        errors = self.validator.validate_todo_data(data)
        self.assertEqual(errors, {})
    
    def test_validate_empty_title(self):
        data = {'title': '', 'completed': False}
        errors = self.validator.validate_todo_data(data)
        self.assertIn('title', errors)
    
    def test_validate_long_title(self):
        data = {'title': 'x' * 100, 'completed': False}
        errors = self.validator.validate_todo_data(data)
        self.assertIn('title', errors)
    
    def test_validate_batch(self):
        todos = [
            {'title': 'Valid todo'},
            {'title': ''},
            {'title': 'Another valid todo'}
        ]
        batch_errors = self.validator.validate_batch(todos)
        self.assertEqual(len(batch_errors), 1)
        self.assertIn(1, batch_errors)
    
    def test_sanitize_title(self):
        title = '  Test   title  with   spaces  '
        sanitized = self.validator.sanitize_title(title)
        self.assertEqual(sanitized, 'Test title with spaces')
    
    def test_check_duplicate_titles(self):
        todos = [
            {'title': 'Duplicate'},
            {'title': 'Unique'},
            {'title': 'duplicate'}  # case insensitive
        ]
        duplicates = self.validator.check_duplicate_titles(todos)
        self.assertIsNotNone(duplicates)
        self.assertIn('duplicate', duplicates)

if __name__ == '__main__':
    unittest.main()
