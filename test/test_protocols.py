import unittest
from src.protocols import ProtocolValidator, SimpleTodoProcessor, MemoryTodoStorage

class TestProtocols(unittest.TestCase):
    
    def setUp(self):
        self.validator = ProtocolValidator()
        self.processor = SimpleTodoProcessor()
        self.storage = MemoryTodoStorage()
    
    def test_processor_protocol_compliance(self):
        self.assertTrue(self.validator.check_processor(self.processor))
    
    def test_storage_protocol_compliance(self):
        self.assertTrue(self.validator.check_storage(self.storage))
    
    def test_simple_processor_functionality(self):
        todos = [
            {'title': 'Test 1', 'completed': False},
            {'title': 'Test 2', 'completed': True}
        ]
        result = self.processor.process(todos)
        self.assertEqual(result['total'], 2)
        self.assertEqual(result['completed'], 1)
        self.assertEqual(result['completion_rate'], 0.5)
    
    def test_memory_storage_functionality(self):
        todo = {'title': 'Test todo', 'completed': False}
        
        # Test save
        todo_id = self.storage.save(todo)
        self.assertIsNotNone(todo_id)
        
        # Test load
        loaded = self.storage.load(todo_id)
        self.assertEqual(loaded['title'], 'Test todo')
        
        # Test delete
        deleted = self.storage.delete(todo_id)
        self.assertTrue(deleted)
        
        # Verify deletion
        self.assertIsNone(self.storage.load(todo_id))
    
    def test_validate_all_protocols(self):
        # Mock analyzer for testing
        class MockAnalyzer:
            @property
            def metrics(self):
                return {}
            def analyze_batch(self, todos):
                return {}
        
        analyzer = MockAnalyzer()
        results = self.validator.validate_all(self.processor, self.storage, analyzer)
        
        self.assertTrue(results['processor_valid'])
        self.assertTrue(results['storage_valid'])
        self.assertTrue(results['analyzer_valid'])

if __name__ == '__main__':
    unittest.main()
