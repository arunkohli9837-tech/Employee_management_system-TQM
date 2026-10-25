"""Create the first administrator for a fresh local installation."""
from getpass import getpass

from database.database import get_connection, initialize_database
from services.auth_service import create_user


def main():
    initialize_database()
    connection = get_connection()
    try:
        count = connection.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    finally:
        connection.close()

    if count:
        print("A user account already exists. Refusing to create another bootstrap administrator.")
        print("If you need an additional account, sign in as Admin and use User Management.")
        return

    username = input("Choose administrator username: ").strip()
    password = getpass("Choose administrator password (minimum 8 characters): ")
    confirmation = getpass("Confirm password: ")
    if password != confirmation:
        print("Passwords do not match. No account was created.")
        return
    try:
        create_user(username, password, "Admin")
    except Exception as error:
        print(f"Administrator was not created: {error}")
        return
    print("Administrator created successfully. Start the application with: python main.py")


if __name__ == "__main__":
    main()
