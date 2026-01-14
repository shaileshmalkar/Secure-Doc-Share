import os
import uuid
from pathlib import Path
from fastapi import UploadFile
from typing import Optional
import aioboto3
from botocore.exceptions import ClientError, BotoCoreError
from app.core.config import (
    S3_BUCKET_NAME, S3_REGION, AWS_ACCESS_KEY_ID, 
    AWS_SECRET_ACCESS_KEY, S3_ENDPOINT_URL, MAX_FILE_SIZE
)
from app.services.encryption import encryption_service

class S3StorageService:
    def __init__(self):
        self.bucket_name = S3_BUCKET_NAME
        self.region = S3_REGION
        self.session = aioboto3.Session()
        
        # Validate S3 configuration
        if not self.bucket_name:
            raise ValueError("S3_BUCKET_NAME environment variable is required when USE_S3=true")
        
        # Create S3 client configuration
        self.s3_config = {
            'service_name': 's3',
            'region_name': self.region,
        }
        
        if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
            self.s3_config['aws_access_key_id'] = AWS_ACCESS_KEY_ID
            self.s3_config['aws_secret_access_key'] = AWS_SECRET_ACCESS_KEY
        
        if S3_ENDPOINT_URL:
            self.s3_config['endpoint_url'] = S3_ENDPOINT_URL
    
    async def validate_bucket(self) -> bool:
        """
        Validate that the S3 bucket exists and is accessible.
        Returns True if valid, raises exception if not.
        """
        try:
            async with self.session.client(**self.s3_config) as s3_client:
                # Check if bucket exists
                try:
                    await s3_client.head_bucket(Bucket=self.bucket_name)
                except ClientError as e:
                    error_code = e.response.get('Error', {}).get('Code', '')
                    if error_code == '404':
                        raise ValueError(f"S3 bucket '{self.bucket_name}' does not exist")
                    elif error_code == '403':
                        raise ValueError(f"Access denied to S3 bucket '{self.bucket_name}'. Check your AWS credentials.")
                    else:
                        raise ValueError(f"Error accessing S3 bucket: {str(e)}")
                
                # Test write permissions
                test_key = f".test/{uuid.uuid4()}"
                try:
                    await s3_client.put_object(
                        Bucket=self.bucket_name,
                        Key=test_key,
                        Body=b"test"
                    )
                    # Clean up test object
                    await s3_client.delete_object(
                        Bucket=self.bucket_name,
                        Key=test_key
                    )
                except ClientError as e:
                    raise ValueError(f"No write permission to S3 bucket '{self.bucket_name}': {str(e)}")
                
                return True
        except BotoCoreError as e:
            raise ValueError(f"Failed to connect to S3: {str(e)}")
        except Exception as e:
            raise ValueError(f"S3 validation error: {str(e)}")
    
    def generate_unique_filename(self, original_filename: str) -> str:
        """
        Generate a unique filename to handle duplicates.
        Uses UUID to ensure uniqueness across all users and instances.
        """
        ext = Path(original_filename).suffix
        unique_id = str(uuid.uuid4())
        return f"{unique_id}{ext}"
    
    async def save_encrypted_file(self, file: UploadFile, encrypted_filename: str) -> int:
        """
        Save and encrypt uploaded file to S3.
        Returns the file size.
        """
        # Read file content
        content = await file.read()
        
        # Check file size
        if len(content) > MAX_FILE_SIZE:
            raise ValueError(f"File size exceeds maximum allowed size of {MAX_FILE_SIZE / (1024*1024)}MB")
        
        # Encrypt the content
        encrypted_content = encryption_service.encrypt(content)
        
        # Upload to S3
        try:
            async with self.session.client(**self.s3_config) as s3_client:
                await s3_client.put_object(
                    Bucket=self.bucket_name,
                    Key=encrypted_filename,
                    Body=encrypted_content,
                    ServerSideEncryption='AES256'  # Additional S3 server-side encryption
                )
        except ClientError as e:
            raise ValueError(f"Failed to upload file to S3: {str(e)}")
        
        return len(content)  # Return original file size
    
    async def get_decrypted_file(self, encrypted_filename: str) -> bytes:
        """
        Retrieve and decrypt file from S3.
        """
        try:
            async with self.session.client(**self.s3_config) as s3_client:
                # Get object from S3
                response = await s3_client.get_object(
                    Bucket=self.bucket_name,
                    Key=encrypted_filename
                )
                
                # Read encrypted content
                encrypted_content = await response['Body'].read()
                
                # Decrypt the content
                decrypted_content = encryption_service.decrypt(encrypted_content)
                
                return decrypted_content
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            if error_code == 'NoSuchKey':
                raise FileNotFoundError(f"File not found in S3: {encrypted_filename}")
            else:
                raise ValueError(f"Failed to retrieve file from S3: {str(e)}")
    
    async def delete_file(self, encrypted_filename: str) -> bool:
        """
        Delete encrypted file from S3.
        """
        try:
            async with self.session.client(**self.s3_config) as s3_client:
                await s3_client.delete_object(
                    Bucket=self.bucket_name,
                    Key=encrypted_filename
                )
                return True
        except ClientError as e:
            # Log error but don't fail if file doesn't exist
            return False

# Singleton instance (will be initialized if USE_S3 is True)
s3_storage_service: Optional[S3StorageService] = None

async def get_s3_storage_service() -> Optional[S3StorageService]:
    """Get or initialize S3 storage service"""
    global s3_storage_service
    if s3_storage_service is None:
        try:
            s3_storage_service = S3StorageService()
            await s3_storage_service.validate_bucket()
        except Exception as e:
            raise ValueError(f"S3 storage initialization failed: {str(e)}")
    return s3_storage_service
