from fastapi import APIRouter, UploadFile, Form, HTTPException, Depends, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
import bcrypt
import uuid
import io

from app.core.database import get_db, engine, Base
from app.models.document import Document
from app.services.storage import get_storage_service
from app.core.config import USE_S3

router = APIRouter()

class AccessRequest(BaseModel):
    passcode: str

@router.post("/upload")
async def upload(
    file: UploadFile, 
    passcode: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload a document with encryption and unique filename handling.
    Supports multiple users and is load balancer compatible.
    """
    try:
        # Get storage service (S3 or local)
        storage = await get_storage_service()
        
        # Generate unique document ID
        doc_id = str(uuid.uuid4())
        
        # Generate unique encrypted filename to handle duplicates
        encrypted_filename = storage.generate_unique_filename(file.filename)
        
        # Save and encrypt the file
        file_size = await storage.save_encrypted_file(file, encrypted_filename)
        
        # Hash the passcode
        passcode_hash = bcrypt.hashpw(passcode.encode(), bcrypt.gensalt()).decode()
        
        # Calculate expiration time
        expires_at = datetime.utcnow() + timedelta(hours=24)
        
        # Create database record
        document = Document(
            id=doc_id,
            original_filename=file.filename,
            encrypted_filename=encrypted_filename,
            passcode_hash=passcode_hash,
            expires_at=expires_at,
            file_size=file_size,
            mime_type=file.content_type
        )
        
        db.add(document)
        await db.commit()
        await db.refresh(document)
        
        return {"link": f"/view/{doc_id}", "doc_id": doc_id}
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log the full error for debugging
        import traceback
        error_trace = traceback.format_exc()
        print(f"Upload error: {str(e)}")
        print(f"Traceback: {error_trace}")
        
        # Clean up file if database operation fails
        if 'encrypted_filename' in locals() and 'storage' in locals():
            try:
                if USE_S3:
                    await storage.delete_file(encrypted_filename)
                else:
                    storage.delete_file(encrypted_filename)
            except:
                pass  # Ignore cleanup errors
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.post("/access/{doc_id}")
async def access(
    doc_id: str, 
    request: AccessRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Verify passcode and grant access to document.
    Works with load balancers as it's stateless (uses database).
    """
    # Query database (works across multiple instances)
    result = await db.execute(select(Document).where(Document.id == doc_id))
    doc = result.scalar_one_or_none()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check expiration
    if datetime.utcnow() > doc.expires_at:
        raise HTTPException(status_code=410, detail="Document has expired")
    
    # Verify passcode
    if not bcrypt.checkpw(request.passcode.encode(), doc.passcode_hash.encode()):
        raise HTTPException(status_code=403, detail="Invalid passcode")
    
    return {
        "message": "Access granted",
        "filename": doc.original_filename,
        "mime_type": doc.mime_type,
        "file_size": doc.file_size
    }

@router.get("/download/{doc_id}")
async def download(
    doc_id: str,
    passcode: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Download decrypted document after passcode verification.
    Supports multiple users and load balancers.
    """
    # Query database
    result = await db.execute(select(Document).where(Document.id == doc_id))
    doc = result.scalar_one_or_none()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check expiration
    if datetime.utcnow() > doc.expires_at:
        raise HTTPException(status_code=410, detail="Document has expired")
    
    # Verify passcode
    if not bcrypt.checkpw(passcode.encode(), doc.passcode_hash.encode()):
        raise HTTPException(status_code=403, detail="Invalid passcode")
    
    try:
        # Get storage service
        storage = await get_storage_service()
        
        # Get and decrypt file
        decrypted_content = await storage.get_decrypted_file(doc.encrypted_filename)
        
        # Create file-like object for streaming
        file_stream = io.BytesIO(decrypted_content)
        
        # Return file as streaming response
        return StreamingResponse(
            io.BytesIO(decrypted_content),
            media_type=doc.mime_type or "application/octet-stream",
            headers={
                "Content-Disposition": f'attachment; filename="{doc.original_filename}"',
                "Content-Length": str(doc.file_size)
            }
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found in storage")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve file: {str(e)}")

@router.delete("/documents/{doc_id}")
async def delete_document(
    doc_id: str,
    passcode: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a document after passcode verification.
    Useful for cleanup operations.
    """
    result = await db.execute(select(Document).where(Document.id == doc_id))
    doc = result.scalar_one_or_none()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Verify passcode
    if not bcrypt.checkpw(passcode.encode(), doc.passcode_hash.encode()):
        raise HTTPException(status_code=403, detail="Invalid passcode")
    
    # Get storage service and delete file
    storage = await get_storage_service()
    if USE_S3:
        await storage.delete_file(doc.encrypted_filename)
    else:
        storage.delete_file(doc.encrypted_filename)
    
    # Delete database record
    await db.execute(delete(Document).where(Document.id == doc_id))
    await db.commit()
    
    return {"message": "Document deleted successfully"}
