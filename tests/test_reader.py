# tests/test_reader.py

import unittest
from unittest.mock import patch, MagicMock
from nfc_library.reader import NFCTokenReader

class TestNFCTokenReader(unittest.TestCase):
    @patch('nfc.ContactlessFrontend')
    def test_read_token(self, MockContactlessFrontend):
        # Configurer le mock
        mock_clf = MockContactlessFrontend.return_value
        mock_clf.connect.return_value.identifier = 'dummy_token'

        reader = NFCTokenReader()
        token = reader.read_token()

        # Vérifier que le token est lu correctement
        self.assertEqual(token, 'dummy_token')

    @patch('nfc.ContactlessFrontend')
    def test_validate_token(self, MockContactlessFrontend):
        reader = NFCTokenReader()
        token = "dummy_token"
        self.assertTrue(reader.validate_token(token))

if __name__ == '__main__':
    unittest.main()
