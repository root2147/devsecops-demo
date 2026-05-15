import sqlite3
import subprocess
import requests

# WARNING:
# This file is intentionally vulnerable for an academic DevSecOps demo.
# Do not copy these patterns into a real application.

ADMIN_USERNAME = "admin"

# Vulnerability 1: hardcoded password.
ADMIN_PASSWORD = "SuperSecretPassword123"

# Vulnerability 2: hardcoded fake API key.
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


def dangerous_file_backup(file_name):
    # Vulnerability 4: command injection.
    # User-controlled input is joined into an operating system command.
    command = "tar -czf backup.tar.gz " + file_name
    subprocess.Popen(command, shell=True)


def call_payment_provider():
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
