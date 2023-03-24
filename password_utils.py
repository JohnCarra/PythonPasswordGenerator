
import string
import secrets
import zxcvbn
import cryptography.fernet
import ctypes


def create_valid_password(password_length):
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation.replace('"', '').replace("'", "")

    while True:
        password = (
            ''.join(secrets.choice(lowercase) for _ in range(2))
            + ''.join(secrets.choice(uppercase) for _ in range(2))
            + ''.join(secrets.choice(digits) for _ in range(2))
            + ''.join(secrets.choice(symbols) for _ in range(2))
            + ''.join(secrets.choice(lowercase + uppercase + digits + symbols)
                      for _ in range(password_length - 8))
        )
        if (any(c.islower() for c in password) and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password) and any(c in symbols for c in password)):
            break

    return password


def get_password_strength(password):
    result = zxcvbn.zxcvbn(password)
    score = result["score"]

    if score == 0:
        strength = "Weak"
    elif score == 1 or score == 2:
        strength = "Average"
    elif score == 3:
        strength = "Strong"
    else:
        strength = "Very Strong"

    return score, strength


def encrypt_password(password):
    key = cryptography.fernet.Fernet.generate_key()
    cipher = cryptography.fernet.Fernet(key)
    encrypted_password = cipher.encrypt(password.encode())

    return encrypted_password


def overwrite_password_with_random_data(password):
    length = len(password.encode())
    buf = ctypes.create_string_buffer(length)
    ctypes.memset(buf, 0, length)
    del password
