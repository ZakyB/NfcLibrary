# src/nfc_library/nfc_manager.py

import logging

class NFCManager:
    def __init__(self, validation_function=None):
        self.validation_function = validation_function

    def validate_token(self, token):
        if self.validation_function:
            return self.validation_function(token)
        else:
            logging.warning("No validation function provided.")
            return False
