import uuid
import os
from pathlib import Path
from fastapi import UploadFile
from typing import Union
from app.core.config import STORAGE_DIR, MAX_FILE_SIZE, USE_S3
from app.services.encryption import encryption_service

class LocalStorageService:
    def __init__(self):
        self.storage_dir = Path(STORAGE_DIR)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_unique_filename(self, original_filename: str) -> str:
        """
        Generate a unique filename to handle duplicates.
        Uses UUID to ensure uniqueness across all users and instances.
        """
        # Get file extension
        ext = Path(original_filename).suffix
        # Generate unique filename with UUID
        unique_id = str(uuid.uuid4())
        return f"{unique_id}{ext}"
    
    async def save_encrypted_file(self, file: UploadFile, encrypted_filename: str) -> int:
        """
        Save and encrypt uploaded file.
        Returns the file size.
        """
        # Read file content
        content = await file.read()
        
        # Check file size
        if len(content) > MAX_FILE_SIZE:
            raise ValueError(f"File size exceeds maximum allowed size of {MAX_FILE_SIZE / (1024*1024)}MB")
        
        # Encrypt the content
        encrypted_content = encryption_service.encrypt(content)
        
        # Save encrypted file with unique filename
        file_path = self.storage_dir / encrypted_filename
        with open(file_path, 'wb') as f:
            f.write(encrypted_content)
        
        return len(content)  # Return original file size
    
    async def get_decrypted_file(self, encrypted_filename: str) -> bytes:
        """
        Retrieve and decrypt file.
        """
        file_path = self.storage_dir / encrypted_filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {encrypted_filename}")
        
        # Read encrypted file
        with open(file_path, 'rb') as f:
            encrypted_content = f.read()
        
        # Decrypt the content
        decrypted_content = encryption_service.decrypt(encrypted_content)
        
        return decrypted_content
    
    def delete_file(self, encrypted_filename: str) -> bool:
        """
        Delete encrypted file from storage.
        """
        file_path = self.storage_dir / encrypted_filename
        
        if file_path.exists():
            file_path.unlink()
            return True
        return False

# Storage service factory
async def get_storage_service():
    """
    Get the appropriate storage service based on configuration.
    Returns S3StorageService if USE_S3=true, otherwise LocalStorageService.
    """
    if USE_S3:
        from app.services.s3_storage import get_s3_storage_service
        return await get_s3_storage_service()
    else:
        return LocalStorageService()

# Singleton instance for local storage (backward compatibility)
storage_service = LocalStorageService()
