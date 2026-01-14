from fastapi import APIRouter, HTTPException
from app.core.config import USE_S3

router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    status = {
        "status": "healthy",
        "storage": "S3" if USE_S3 else "Local"
    }
    
    if USE_S3:
        try:
            from app.services.s3_storage import get_s3_storage_service
            s3_storage = await get_s3_storage_service()
            await s3_storage.validate_bucket()
            status["s3_bucket"] = s3_storage.bucket_name
            status["s3_status"] = "connected"
        except Exception as e:
            status["s3_status"] = "error"
            status["s3_error"] = str(e)
    
    return status
