# src/nfc_library/reader.py

import nfc
import logging

class NFCTokenReader:
    def __init__(self, validation_function=None, connection_type='usb'):
        self.clf = None
        self.connection_type = connection_type
        self.validation_function = validation_function
        self._setup_reader()

    def _setup_reader(self):
        try:
            self.clf = nfc.ContactlessFrontend(self.connection_type)
            logging.info(f"Connected to NFC reader via {self.connection_type}")
        except IOError as e:
            logging.error(f"Failed to connect to NFC reader: {e}")
            raise

    def read_token(self):
        try:
            tag = self.clf.connect(rdwr={'on-connect': lambda tag: False})
            logging.info(f"Token read successfully: {tag.identifier}")
            return tag.identifier
        except Exception as e:
            logging.error(f"Failed to read token: {e}")
            return None

    def validate_token(self, token):
        if self.validation_function:
            return self.validation_function(token)
        logging.warning("No validation function provided.")
        return False
