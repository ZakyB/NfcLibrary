import sqlite3
from nfc_library import NFCManager

# Setup in-memory SQLite database for testing
conn = sqlite3.connect(':memory:')
conn.execute("CREATE TABLE valid_tokens (token TEXT)")
conn.execute("INSERT INTO valid_tokens (token) VALUES ('valid_token')")
conn.commit()

def db_validation_function(token):
    query = "SELECT 1 FROM valid_tokens WHERE token = ?"
    cursor = conn.execute(query, (token,))
    return cursor.fetchone() is not None

manager = NFCManager(validation_function=db_validation_function)
token, is_valid = manager.read_and_validate_token()
print(f"Token: {token}, Valid: {is_valid}")
