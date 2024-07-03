import unittest
from unittest.mock import patch
from nfc_library import NFCManager
import sqlite3
import requests

class TestNFCManager(unittest.TestCase):

    def test_validate_token_with_function(self):
        manager = NFCManager(validation_function=lambda token: 'User' if token == 'valid_token' else None)
        self.assertEqual(manager.validate_token('valid_token'), 'User')
        self.assertIsNone(manager.validate_token('invalid_token'))

    def test_validate_token_with_no_function(self):
        manager = NFCManager()
        self.assertFalse(manager.validate_token('valid_token'))

    def test_db_validation_function(self):
        conn = sqlite3.connect(':memory:')
        conn.execute("CREATE TABLE users (name TEXT, token TEXT)")
        conn.execute("INSERT INTO users (name, token) VALUES ('Alice', 'token_alice')")
        conn.commit()

        def db_validation_function(token):
            query = "SELECT name FROM users WHERE token = ?"
            cursor = conn.execute(query, (token,))
            result = cursor.fetchone()
            return result[0] if result else None

        manager = NFCManager(validation_function=db_validation_function)
        self.assertEqual(manager.validate_token('token_alice'), 'Alice')
        self.assertIsNone(manager.validate_token('invalid_token'))

    @patch('requests.post')
    def test_api_validation_function(self, mock_post):
        mock_post.return_value.json.return_value = {'valid': True}

        def api_validation_function(token):
            response = requests.post('https://example.com/validate', json={'token': token})
            return 'API_User' if response.json().get('valid', False) else None

        manager = NFCManager(validation_function=api_validation_function)
        self.assertEqual(manager.validate_token('dummy_token'), 'API_User')

        mock_post.return_value.json.return_value = {'valid': False}
        self.assertIsNone(manager.validate_token('dummy_token'))

if __name__ == '__main__':
    unittest.main()
