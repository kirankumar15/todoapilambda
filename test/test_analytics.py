import unittest
from src.analytics import TodoAnalytics, TodoStats

class TestTodoAnalytics(unittest.TestCase):
    
    def setUp(self):
        self.sample_todos = [
            {'id': '1', 'title': 'Test todo 1', 'completed': False, 'created_at': '2023-01-01T10:00:00Z', 'updated_at': '2023-01-01T10:00:00Z'},
            {'id': '2', 'title': 'Test todo 2', 'completed': True, 'created_at': '2023-01-01T11:00:00Z', 'updated_at': '2023-01-01T12:00:00Z'},
            {'id': '3', 'title': 'Another test', 'completed': True, 'created_at': '2023-01-01T13:00:00Z', 'updated_at': '2023-01-01T14:00:00Z'}
        ]
        self.analytics = TodoAnalytics(self.sample_todos)
    
    def test_stats_calculation(self):
        stats = self.analytics.stats
        self.assertEqual(stats['total_count'], 3)
        self.assertEqual(stats['completed_count'], 2)
        self.assertEqual(stats['pending_count'], 1)
        self.assertAlmostEqual(stats['completion_rate'], 2/3, places=2)
    
    def test_filter_by_status(self):
        completed = self.analytics.filter_by_status('completed')
        self.assertEqual(len(completed), 2)
        
        pending = self.analytics.filter_by_status('pending')
        self.assertEqual(len(pending), 1)
        
        all_todos = self.analytics.filter_by_status('all')
        self.assertEqual(len(all_todos), 3)
    
    def test_generate_report_json(self):
        report = self.analytics.generate_report(format_type='json')
        self.assertIn('stats', report)
        self.assertIn('trends', report)
    
    def test_generate_report_summary(self):
        report = self.analytics.generate_report(format_type='summary')
        self.assertIn('Todo Analytics Report', report)
        self.assertIn("stats['total_count']=3", report)

if __name__ == '__main__':
    unittest.main()
