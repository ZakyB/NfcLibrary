import requests
from nfc_library.reader import NFCTokenReader

def api_validation_function(token):
    response = requests.post('https://example.com/validate', json={'token': token})
    return response.json().get('valid', False)

# Créer une instance de NFCTokenReader avec la fonction de validation de l'API externe
reader = NFCTokenReader(validation_function=api_validation_function)
token = reader.read_token()
is_valid = reader.validate_token(token)
print(f"Token is valid: {is_valid}")
