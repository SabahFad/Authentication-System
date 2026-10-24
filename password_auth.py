
import hashlib
import secrets
import hmac
from pathlib import Path

# Store the data file in the same folder as this program
DATA_FILE = Path(__file__).resolve().parent / "users.txt"


def hash_password(password, salt):
    combined = (password + salt).encode("utf-8")
    return hashlib.sha256(combined).hexdigest()


def read_users():
    users = {}

    if not DATA_FILE.exists():
        return users

    with DATA_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            parts = line.rstrip("\n").split(":")

            if len(parts) == 3:
                username, salt, password_hash = parts
                users[username] = (salt, password_hash)

    return users


def register():
    username = input("Enter username: ").strip()

    if not username or ":" in username:
        print("Invalid username.")
        return

    users = read_users()

    if username in users:
        print("Username already exists.")
        return

    password = input("Enter password: ")

    if not password:
        print("Password cannot be empty.")
        return

    # Generate a unique random salt for this user
    salt = secrets.token_hex(16)

    # Hash the password with the salt
    password_hash = hash_password(password, salt)

    # Save username, salt, and hash to the text file
    with DATA_FILE.open("a", encoding="utf-8") as file:
        file.write(f"{username}:{salt}:{password_hash}\n")

    print("Registration successful!")


def login():
    username = input("Enter username: ").strip()
    password = input("Enter password: ")

    users = read_users()

    if username not in users:
        print("Login failed. User not found.")
        return

    salt, saved_hash = users[username]
    entered_hash = hash_password(password, salt)

    if hmac.compare_digest(entered_hash, saved_hash):
        print("Login successful! Welcome.")
    else:
        print("Login failed. Incorrect password.")


def main():
    while True:
        print("\n===== User Authentication System =====")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Program closed.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
