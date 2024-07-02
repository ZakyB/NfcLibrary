# src/nfc_library/reader.py

import nfc

class NFCTokenReader:
    def __init__(self):
        self.clf = nfc.ContactlessFrontend('usb')

    def read_token(self):
        tag = self.clf.connect(rdwr={'on-connect': lambda tag: False})
        return tag.identifier

    def validate_token(self, token):
        # Ajoutez votre logique de validation ici
        return True
