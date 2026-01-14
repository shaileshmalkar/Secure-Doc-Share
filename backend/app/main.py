
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import documents, health
from app.core.database import engine, Base

app = FastAPI(title="Secure Document Sharing")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database tables and validate S3 on startup
@app.on_event("startup")
async def init_db():
    # Initialize database
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Validate S3 bucket if S3 is enabled
    from app.core.config import USE_S3
    if USE_S3:
        try:
            from app.services.s3_storage import get_s3_storage_service
            s3_storage = await get_s3_storage_service()
            await s3_storage.validate_bucket()
            print(f"✓ S3 bucket validated successfully: {s3_storage.bucket_name}")
        except Exception as e:
            print(f"⚠ Warning: S3 validation failed: {str(e)}")
            print("⚠ Application will continue but S3 operations may fail")

app.include_router(documents.router, prefix="/api")
app.include_router(health.router, prefix="/api")