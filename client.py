import requests
import base64
import hashlib
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class EncryptionManager:
    def __init__(self):
        self.key = os.urandom(32)
        self.iv = os.urandom(16)
        self.mac_key = os.urandom(32)
        aes_context = Cipher(algorithms.AES(self.key), modes.CTR(self.iv), backend=default_backend())
        self.encryptor = aes_context.encryptor()
        self.decryptor = aes_context.decryptor()

    def update_encryptor(self, plaintext):
        return self.encryptor.update(plaintext)

    def finalize_encryptor(self):
        return self.encryptor.finalize()

    def update_decryptor(self, ciphertext):
        return self.decryptor.update(ciphertext)

    def finalize_decryptor(self):
        return self.decryptor.finalize()

def generate_hmac(data, key):
    h = hmac.new(key, data, hashlib.sha256)
    return h.digest()

def main():
    encryption_manager = EncryptionManager()

    email = input("Enter email: ")
    password = input("Enter password: ")

    session_keys = base64.b64encode(encryption_manager.key + encryption_manager.mac_key + encryption_manager.iv).decode()

    plaintext = f"{email}\n{password}".encode()
    ciphertext = base64.b64encode(encryption_manager.update_encryptor(plaintext) + encryption_manager.finalize_encryptor()).decode()

    hmac_value = base64.b64encode(generate_hmac(plaintext, encryption_manager.mac_key)).decode()

    data = {
        'session_keys': session_keys,
        'cyphertext': ciphertext,
        'hmac': hmac_value
    }

    response = requests.post('http://localhost:5000/login', data=data)

    print("Response Code:", response.status_code)
    if response.status_code == 200:
        print("Session ID:", response.cookies['session_id'])

if __name__ == "__main__":
    main()
