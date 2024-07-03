# src/nfc_library/nfc_manager.py

from .reader import NFCTokenReader
import logging

class NFCManager:
    def __init__(self, validation_function=None, connection_type='usb'):
        self.reader = NFCTokenReader(connection_type)
        self.validation_function = validation_function

    def read_and_validate_token(self):
        token = self.reader.read_token()
        if token is None:
            return None, False
        
        if self.validation_function:
            is_valid = self.validation_function(token)
            return token, is_valid
        else:
            logging.warning("No validation function provided.")
            return token, False

    def set_validation_function(self, validation_function):
        self.validation_function = validation_function
