from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import os
from app.core.config import ENCRYPTION_KEY

class EncryptionService:
    def __init__(self):
        # Derive a key from the encryption key using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'secure_doc_share_salt',  # In production, use a random salt per file
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(ENCRYPTION_KEY))
        self.cipher = Fernet(key)
    
    def encrypt(self, data: bytes) -> bytes:
        """Encrypt file data"""
        return self.cipher.encrypt(data)
    
    def decrypt(self, encrypted_data: bytes) -> bytes:
        """Decrypt file data"""
        return self.cipher.decrypt(encrypted_data)

# Singleton instance
encryption_service = EncryptionService()
