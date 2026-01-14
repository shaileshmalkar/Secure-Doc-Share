from sqlalchemy import Column, String, DateTime, Text, Integer
from sqlalchemy.sql import func
from app.core.database import Base
import uuid

class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    original_filename = Column(String, nullable=False)
    encrypted_filename = Column(String, nullable=False, unique=True)
    passcode_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String, nullable=True)
    
    # For multi-user support and load balancer compatibility
    # Each document is isolated by its unique ID
    # No user-specific data needed as documents are accessed via share link
