import sqlite3
from nfc_library import NFCManager

conn = sqlite3.connect('tokens.db')
conn.execute("CREATE TABLE IF NOT EXISTS valid_tokens (token TEXT)")
conn.execute("INSERT INTO valid_tokens (token) VALUES ('valid_token1')")
conn.execute("INSERT INTO valid_tokens (token) VALUES ('valid_token2')")
conn.commit()

def db_validation_function(token):
    query = "SELECT 1 FROM valid_tokens WHERE token = ?"
    cursor = conn.execute(query, (token,))
    return cursor.fetchone() is not None

manager = NFCManager(validation_function=db_validation_function)
token = 'valid_token1'
is_valid = manager.validate_token(token)
print(f"Token: {token}, Valid: {is_valid}")
