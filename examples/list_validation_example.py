from nfc_library.reader import NFCTokenReader

valid_tokens = ["token1", "token2", "token3"]

def list_validation_function(token):
    return token in valid_tokens

# Créer une instance de NFCTokenReader avec la fonction de validation de la liste
reader = NFCTokenReader(validation_function=list_validation_function)
token = reader.read_token()
is_valid = reader.validate_token(token)
print(f"Token is valid: {is_valid}")
