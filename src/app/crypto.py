import os

from cryptography.fernet import Fernet


def get_fernet() -> Fernet:
    key = os.getenv("FERNET_KEY")
    if not key:
        key = Fernet.generate_key().decode()
    return Fernet(key.encode())


fernet = get_fernet()
