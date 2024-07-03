import unittest
from unittest.mock import patch, MagicMock
from nfc_library import NFCManager
import sqlite3
import requests
import logging

class TestNFCManager(unittest.TestCase):

    def setUp(self):
        self.patcher = patch('nfc.ContactlessFrontend')
        self.MockContactlessFrontend = self.patcher.start()
        self.mock_clf = self.MockContactlessFrontend.return_value
        self.mock_clf.connect.return_value.identifier = 'dummy_token'

    def tearDown(self):
        self.patcher.stop()

    def test_read_and_validate_token_with_function(self):
        manager = NFCManager(validation_function=lambda token: token == 'dummy_token')
        token, is_valid = manager.read_and_validate_token()
        self.assertEqual(token, 'dummy_token')
        self.assertTrue(is_valid)

    def test_read_and_validate_token_with_no_function(self):
        manager = NFCManager()
        token, is_valid = manager.read_and_validate_token()
        self.assertEqual(token, 'dummy_token')
        self.assertFalse(is_valid)

    def test_read_token_no_device(self):
        self.MockContactlessFrontend.side_effect = IOError("No such device")
        with self.assertRaises(IOError):
            manager = NFCManager()

    def test_db_validation_function(self):
        conn = sqlite3.connect(':memory:')
        conn.execute("CREATE TABLE valid_tokens (token TEXT)")
        conn.execute("INSERT INTO valid_tokens (token) VALUES ('valid_token')")
        conn.commit()

        def db_validation_function(token):
            query = "SELECT 1 FROM valid_tokens WHERE token = ?"
            cursor = conn.execute(query, (token,))
            return cursor.fetchone() is not None

        manager = NFCManager(validation_function=db_validation_function)
        token, is_valid = manager.read_and_validate_token()
        self.assertEqual(token, 'dummy_token')
        self.assertFalse(is_valid)

    @patch('requests.post')
    def test_api_validation_function(self, mock_post):
        mock_post.return_value.json.return_value = {'valid': True}

        def api_validation_function(token):
            response = requests.post('https://example.com/validate', json={'token': token})
            return response.json().get('valid', False)

        manager = NFCManager(validation_function=api_validation_function)
        token, is_valid = manager.read_and_validate_token()
        self.assertEqual(token, 'dummy_token')
        self.assertTrue(is_valid)

        mock_post.return_value.json.return_value = {'valid': False}
        token, is_valid = manager.read_and_validate_token()
        self.assertEqual(token, 'dummy_token')
        self.assertFalse(is_valid)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()
