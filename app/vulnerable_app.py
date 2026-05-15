import sqlite3
import requests

# WARNING:
# This file is intentionally vulnerable for an academic DevSecOps demo.
# Do not copy these patterns into a real application.

ADMIN_USERNAME = "admin"

# Vulnerability 1: hardcoded password.
# Passwords should never be stored directly inside source code.
ADMIN_PASSWORD = "SuperSecretPassword123"

# Vulnerability 2: hardcoded fake API key.
# API keys should be stored in environment variables or a secret manager.
PAYMENT_API_KEY_SECRET = "fake-api-key-123456789"


def create_database():
    connection = sqlite3.connect("demo.db")
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("CREATE TABLE users (username TEXT, password TEXT)")
    cursor.execute(
        "INSERT INTO users VALUES ('admin', 'SuperSecretPassword123')"
    )

    connection.commit()
    connection.close()


def unsafe_login(username, password):
    connection = sqlite3.connect("demo.db")
    cursor = connection.cursor()

    # Vulnerability 3: SQL injection.
    # User input is joined directly into the SQL query.
    query = (
        "SELECT * FROM users WHERE username = '"
        + username
        + "' AND password = '"
        + password
        + "'"
    )

    print("Running query:", query)

    cursor.execute(query)
    result = cursor.fetchone()

    connection.close()

    if result:
        return "Login successful"
    return "Login failed"


def call_payment_provider():
    # This is only here to show an API key being used incorrectly.
    # It is fake and will not connect to a real payment provider.
    headers = {"Authorization": "Bearer " + PAYMENT_API_KEY_SECRET}

    response = requests.get(
        "https://example.com/api/payments",
        headers=headers,
        timeout=5,
    )

    return response.status_code


if __name__ == "__main__":
    create_database()

    print("Normal login:")
    print(unsafe_login("admin", "wrongpassword"))

    print("\nSQL injection login:")
    print(unsafe_login("admin", "' OR '1'='1"))
