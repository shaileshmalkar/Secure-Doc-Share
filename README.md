# Secure Document Sharing

[![GitHub](https://img.shields.io/badge/GitHub-shaileshmalkar-blue)](https://github.com/shaileshmalkar/Secure-Doc-Share)

A secure document sharing application with encryption, multi-user support, and load balancer compatibility.

## Features

- 🔒 **End-to-End Encryption**: Files are encrypted at rest using AES-256 encryption
- 👥 **Multi-User Support**: Handles multiple users simultaneously with proper data isolation
- ⚖️ **Load Balancer Compatible**: Stateless design works seamlessly with load balancers
- 📱 **Responsive Design**: Beautiful UI that works on mobile and desktop
- 🔐 **Secure Passcode Protection**: Bcrypt hashed passcodes for document access
- ⏰ **Auto-Expiration**: Documents expire after 24 hours
- 📁 **Duplicate Handling**: Unique file naming prevents conflicts

## Architecture

### Backend (FastAPI)
- **Database**: SQLAlchemy with SQLite (dev) / PostgreSQL (production)
- **Encryption**: Fernet (AES-128) with PBKDF2 key derivation
- **Storage**: Encrypted files stored with UUID-based unique names
- **API**: RESTful API with proper error handling

### Frontend (Vue.js 3)
- **Framework**: Vue 3 with Vue Router
- **Build Tool**: Vite
- **Styling**: Modern CSS with responsive design
- **Features**: Drag & drop upload, file download, passcode protection

## Setup

### Backend

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Set environment variables (optional):
```bash
export ENCRYPTION_KEY="your-32-character-secret-key"
export DATABASE_URL="postgresql+asyncpg://user:pass@localhost/dbname"  # For production
```

3. Start the server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

## API Endpoints

- `POST /api/upload` - Upload a document with passcode
- `POST /api/access/{doc_id}` - Verify passcode and get document info
- `GET /api/download/{doc_id}?passcode=xxx` - Download decrypted document
- `DELETE /api/documents/{doc_id}?passcode=xxx` - Delete a document

## Load Balancer Configuration

The application is designed to work with load balancers:

1. **Stateless Design**: All state is stored in the database
2. **Shared Storage**: Files are stored in a shared storage directory (can be mounted volume or S3)
3. **Database**: Use a shared database (PostgreSQL/MySQL) for all instances
4. **Session Affinity**: Not required - any instance can handle any request

### Production Deployment

For production with load balancers:

1. Use PostgreSQL or MySQL instead of SQLite
2. Use shared file storage (S3, NFS, or similar)
3. Set `ENCRYPTION_KEY` as an environment variable (same across all instances)
4. Configure CORS for your frontend domain
5. Use environment variables for database connection

## Security Features

- Files encrypted at rest using AES-256
- Passcodes hashed with bcrypt
- Unique file naming prevents conflicts
- Automatic expiration after 24 hours
- Proper error handling without information leakage

## License

MIT
