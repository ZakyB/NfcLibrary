import requests
from nfc_library import NFCManager

def api_validation_function(token):
    response = requests.post('https://example.com/validate', json={'token': token})
    return response.json().get('valid', False)

manager = NFCManager(validation_function=api_validation_function)
token, is_valid = manager.read_and_validate_token()
print(f"Token: {token}, Valid: {is_valid}")
