import hashlib


def hashtext(text):
    return hashlib.sha224(f"{text}".encode()).hexdigest()
