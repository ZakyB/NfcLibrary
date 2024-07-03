from nfc_library import NFCManager

valid_tokens = ["token1", "token2", "token3"]

def list_validation_function(token):
    return token in valid_tokens

manager = NFCManager(validation_function=list_validation_function)
token = 'token1'
is_valid = manager.validate_token(token)
print(f"Token: {token}, Valid: {is_valid}")
