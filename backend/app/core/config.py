import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Storage directory for encrypted files
STORAGE_DIR = BASE_DIR / "storage"
STORAGE_DIR.mkdir(exist_ok=True)

# Encryption key - in production, use environment variable
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "your-secret-key-32-chars-long!!")[:32].encode()

# Database URL - SQLite for development, can be swapped for PostgreSQL/MySQL
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite+aiosqlite:///{BASE_DIR}/documents.db")

# File upload settings
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
ALLOWED_EXTENSIONS = None  # None means all files allowed

# S3 Configuration
USE_S3 = os.getenv("USE_S3", "false").lower() == "true"
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "")
S3_REGION = os.getenv("S3_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL", None)  # For S3-compatible services like MinIO
