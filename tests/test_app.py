import unittest
from app import app  # Adjust the import based on your file structure

class TodoAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_add_empty_task(self):
        response = self.app.post('/add', data={'task': ''})
        self.assertEqual(response.status_code, 400)  # Expecting Bad Request
        self.assertIn(b'Invalid task', response.data)  # Check for error message

    def test_add_invalid_task(self):
        response = self.app.post('/add', data={'task': ' '})  # Space is invalid
        self.assertEqual(response.status_code, 400)  # Expecting Bad Request
        self.assertIn(b'Invalid task', response.data)  # Check for error message

    def test_delete_task(self):
        # First add a task
        self.app.post('/add', data={'task': 'Test Task'})
        # Now delete the task
        response = self.app.post('/delete/0')  # Assuming task ID 0
        self.assertEqual(response.status_code, 302)  # Check for redirect
        # Now check if the task is really deleted
        response = self.app.get('/')
        self.assertNotIn(b'Test Task', response.data)  # Ensure the task is not present

    def test_add_valid_task(self):
        response = self.app.post('/add', data={'task': 'New Task'})
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        response = self.app.get('/')
        self.assertIn(b'New Task', response.data)  # Ensure the task is present

    def test_delete_non_existent_task(self):
        response = self.app.post('/delete/999')  # Attempt to delete a non-existent task
        self.assertEqual(response.status_code, 302)  # Still expect a redirect
        response = self.app.get('/')
        self.assertNotIn(b'Task that does not exist', response.data)  # Ensure it doesn't crash

    def test_add_task_with_special_characters(self):
        response = self.app.post('/add', data={'task': 'Task with @#$'})
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        response = self.app.get('/')
        self.assertIn(b'Task with @#$', response.data)  # Ensure the task is present

    def test_add_task_with_long_text(self):
        response = self.app.post('/add', data={'task': 'Task with very long text that exceeds the limit'})
        self.assertEqual(response.status_code, 400)  # Expecting Bad Request
        self.assertIn(b'Task is too long', response.data)  # Check for error message

if __name__ == '__main__':
    unittest.main()