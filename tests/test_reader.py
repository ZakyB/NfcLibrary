import unittest
from unittest.mock import patch, MagicMock
from nfc_library.reader import NFCTokenReader
import sqlite3
import requests
import logging

class TestNFCTokenReader(unittest.TestCase):

    def setUp(self):
        self.patcher = patch('nfc.ContactlessFrontend')
        self.MockContactlessFrontend = self.patcher.start()
        self.mock_clf = self.MockContactlessFrontend.return_value
        self.mock_clf.connect.return_value.identifier = 'dummy_token'

    def tearDown(self):
        self.patcher.stop()

    def test_read_token(self):
        reader = NFCTokenReader()
        token = reader.read_token()
        self.assertEqual(token, 'dummy_token')

    def test_validate_token_with_function(self):
        reader = NFCTokenReader(validation_function=lambda token: token == 'dummy_token')
        token = 'dummy_token'
        self.assertTrue(reader.validate_token(token))

    def test_validate_token_with_no_function(self):
        reader = NFCTokenReader()
        token = 'dummy_token'
        self.assertFalse(reader.validate_token(token))

    def test_read_token_no_device(self):
        self.MockContactlessFrontend.side_effect = IOError("No such device")
        with self.assertRaises(IOError):
            reader = NFCTokenReader()

    def test_db_validation_function(self):
        # Setup in-memory SQLite database for testing
        conn = sqlite3.connect(':memory:')
        conn.execute("CREATE TABLE valid_tokens (token TEXT)")
        conn.execute("INSERT INTO valid_tokens (token) VALUES ('valid_token')")
        conn.commit()

        def db_validation_function(token):
            query = "SELECT 1 FROM valid_tokens WHERE token = ?"
            cursor = conn.execute(query, (token,))
            return cursor.fetchone() is not None

        reader = NFCTokenReader(validation_function=db_validation_function)
        self.assertTrue(reader.validate_token('valid_token'))
        self.assertFalse(reader.validate_token('invalid_token'))

    @patch('requests.post')
    def test_api_validation_function(self, mock_post):
        mock_post.return_value.json.return_value = {'valid': True}

        def api_validation_function(token):
            response = requests.post('https://example.com/validate', json={'token': token})
            return response.json().get('valid', False)

        reader = NFCTokenReader(validation_function=api_validation_function)
        self.assertTrue(reader.validate_token('any_token'))

        mock_post.return_value.json.return_value = {'valid': False}
        self.assertFalse(reader.validate_token('any_token'))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()
