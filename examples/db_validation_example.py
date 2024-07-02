import sqlite3
from nfc_library.reader import NFCTokenReader

def db_validation_function(token):
    conn = sqlite3.connect('tokens.db')
    query = "SELECT 1 FROM valid_tokens WHERE token = ?"
    cursor = conn.execute(query, (token,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Créer une instance de NFCTokenReader avec la fonction de validation de la base de données
reader = NFCTokenReader(validation_function=db_validation_function)
token = reader.read_token()
is_valid = reader.validate_token(token)
print(f"Token is valid: {is_valid}")
