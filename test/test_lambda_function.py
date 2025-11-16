import json
import unittest
from unittest.mock import patch, MagicMock
from src.lambda_function import lambda_handler
from src.mock_todo_service import MockTodoService

class TestLambdaHandler(unittest.TestCase):
    
    def setUp(self):
        self.mock_service = MockTodoService()
        # Patch the global todo_service with our mock
        self.patcher = patch('src.lambda_function.todo_service', self.mock_service)
        self.patcher.start()
    
    def tearDown(self):
        self.patcher.stop()
    
    def test_get_todos_with_filter(self):
        # Create test data
        self.mock_service.create("Todo 1")
        todo2 = self.mock_service.create("Todo 2")
        self.mock_service.update(todo2['id'], completed=True)
        
        # Test completed filter
        event = {
            'httpMethod': 'GET',
            'path': '/todos',
            'queryStringParameters': {'completed': 'true'}
        }
        result = lambda_handler(event, MagicMock())
        
        self.assertEqual(result['statusCode'], 200)
        todos = json.loads(result['body'])
        self.assertEqual(len(todos), 1)
        self.assertTrue(todos[0]['completed'])
    
    def test_get_single_todo(self):
        todo = self.mock_service.create("Test todo")
        
        event = {
            'httpMethod': 'GET',
            'path': f'/todos/{todo["id"]}'
        }
        result = lambda_handler(event, MagicMock())
        
        self.assertEqual(result['statusCode'], 200)
        body = json.loads(result['body'])
        self.assertEqual(body['title'], "Test todo")
    
    def test_create_todo_validation(self):
        event = {
            'httpMethod': 'POST',
            'path': '/todos',
            'body': json.dumps({'title': '   '})  # Empty title
        }
        result = lambda_handler(event, MagicMock())
        
        self.assertEqual(result['statusCode'], 400)
    
    def test_update_todo_full_flow(self):
        todo = self.mock_service.create("Original")
        
        event = {
            'httpMethod': 'PUT',
            'path': f'/todos/{todo["id"]}',
            'body': json.dumps({'title': 'Updated', 'completed': True})
        }
        result = lambda_handler(event, MagicMock())
        
        self.assertEqual(result['statusCode'], 200)
        body = json.loads(result['body'])
        self.assertEqual(body['title'], 'Updated')
        self.assertTrue(body['completed'])
    
    def test_cors_headers(self):
        event = {'httpMethod': 'GET', 'path': '/todos'}
        result = lambda_handler(event, MagicMock())
        
        self.assertIn('Access-Control-Allow-Origin', result['headers'])
        self.assertEqual(result['headers']['Access-Control-Allow-Origin'], '*')
    
    def test_invalid_json_body(self):
        event = {
            'httpMethod': 'POST',
            'path': '/todos',
            'body': 'invalid json'
        }
        result = lambda_handler(event, MagicMock())
        
        self.assertEqual(result['statusCode'], 400)
        self.assertIn('Invalid JSON', result['body'])

if __name__ == '__main__':
    unittest.main()
