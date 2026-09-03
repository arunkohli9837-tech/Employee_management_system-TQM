import base64
import hashlib
import hmac
import secrets


HASH_ALGORITHM = "sha256"
PBKDF2_ITERATIONS = 600_000
SALT_LENGTH = 16

MIN_PASSWORD_LENGTH = 8


def validate_password(password: str) -> None:
    """Validate the password against the application's password policy."""
    if not isinstance(password, str):
        raise ValueError("Password must be text.")

    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValueError(
            f"Password must contain at least {MIN_PASSWORD_LENGTH} characters."
        )


def hash_password(password: str) -> str:
    """Create a salted PBKDF2 password hash."""
    validate_password(password)

    salt = secrets.token_bytes(SALT_LENGTH)

    password_hash = hashlib.pbkdf2_hmac(
        HASH_ALGORITHM,
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
    )

    encoded_salt = base64.b64encode(salt).decode("ascii")
    encoded_hash = base64.b64encode(password_hash).decode("ascii")

    return (
        f"pbkdf2_{HASH_ALGORITHM}$"
        f"{PBKDF2_ITERATIONS}$"
        f"{encoded_salt}$"
        f"{encoded_hash}"
    )


def verify_password(password: str, stored_hash: str) -> bool:
    """Safely verify a password against a stored hash."""
    if not isinstance(password, str) or not isinstance(stored_hash, str):
        return False

    try:
        algorithm, iterations, encoded_salt, encoded_hash = stored_hash.split(
            "$",
            maxsplit=3,
        )

        if algorithm != f"pbkdf2_{HASH_ALGORITHM}":
            return False

        iterations = int(iterations)

        if iterations <= 0:
            return False

        salt = base64.b64decode(encoded_salt)
        expected_hash = base64.b64decode(encoded_hash)

        actual_hash = hashlib.pbkdf2_hmac(
            HASH_ALGORITHM,
            password.encode("utf-8"),
            salt,
            iterations,
        )

        return hmac.compare_digest(actual_hash, expected_hash)

    except (ValueError, TypeError, UnicodeError):
        return False