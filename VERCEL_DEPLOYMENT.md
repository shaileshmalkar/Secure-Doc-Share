# Vercel Deployment Guide

## Important Notes

⚠️ **Vercel only deploys the frontend**. Your FastAPI backend needs to be deployed separately on:
- Railway (recommended)
- Render
- Heroku
- AWS/GCP/Azure
- Or any Python hosting service

## Step 1: Deploy Backend First

### Option A: Railway (Recommended)

1. Go to https://railway.app
2. Create new project
3. Add PostgreSQL database (or use SQLite for dev)
4. Deploy from GitHub repository
5. Set root directory to `backend`
6. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
7. Add environment variables:
   - `ENCRYPTION_KEY` (32 character secret)
   - `DATABASE_URL` (if using PostgreSQL)
   - `USE_S3` (true/false)
   - S3 credentials if using S3

### Option B: Render

1. Go to https://render.com
2. Create new Web Service
3. Connect GitHub repository
4. Set:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables

## Step 2: Deploy Frontend to Vercel

### Method 1: Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel

# Follow prompts:
# - Set root directory: ./frontend
# - Override settings: Yes
# - Build command: npm run build
# - Output directory: dist
```

### Method 2: GitHub Integration (Recommended)

1. Go to https://vercel.com
2. Click "Add New Project"
3. Import your GitHub repository: `shaileshmalkar/Secure-Doc-Share`
4. Configure project:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`
5. Add Environment Variable:
   - **Name**: `VITE_API_URL`
   - **Value**: Your backend URL (e.g., `https://your-app.railway.app/api`)
6. Click "Deploy"

## Step 3: Configure Environment Variables

In Vercel dashboard, go to Settings > Environment Variables:

- `VITE_API_URL`: Your backend API URL (e.g., `https://your-backend.railway.app/api`)

## Step 4: Update CORS in Backend

Make sure your backend allows requests from Vercel domain:

```python
# In backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://your-app.vercel.app",  # Add your Vercel URL
        "https://*.vercel.app"  # Or allow all Vercel subdomains
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Troubleshooting

### 404 Error on Vercel

**Cause**: Vercel can't find the build output or routing is misconfigured.

**Solution**:
1. Check `vercel.json` is in root directory
2. Verify build output directory is `frontend/dist`
3. Ensure `rewrites` rule is configured for SPA routing

### API Calls Failing

**Cause**: Backend URL not configured or CORS issues.

**Solution**:
1. Set `VITE_API_URL` environment variable in Vercel
2. Update backend CORS to allow Vercel domain
3. Check backend is deployed and accessible

### Build Fails

**Cause**: Missing dependencies or build errors.

**Solution**:
1. Check `frontend/package.json` has all dependencies
2. Verify Node.js version (Vercel auto-detects, but can set in settings)
3. Check build logs in Vercel dashboard

## Quick Deploy Commands

```bash
# Deploy to Vercel
cd frontend
vercel --prod

# Or use GitHub integration (automatic on push to main)
git push origin main
```

## Project Structure for Vercel

```
secure-doc-share/
├── vercel.json          # Vercel configuration
├── .vercelignore        # Files to ignore
├── frontend/            # Frontend code (deployed to Vercel)
│   ├── dist/           # Build output (generated)
│   ├── src/
│   ├── package.json
│   └── vite.config.js
└── backend/            # Backend code (deployed separately)
    └── ...
```

## Environment Variables Reference

### Frontend (Vercel)
- `VITE_API_URL`: Backend API URL

### Backend (Railway/Render/etc)
- `ENCRYPTION_KEY`: 32 character encryption key
- `DATABASE_URL`: Database connection string
- `USE_S3`: true/false
- `S3_BUCKET_NAME`: S3 bucket name (if using S3)
- `AWS_ACCESS_KEY_ID`: AWS access key (if using S3)
- `AWS_SECRET_ACCESS_KEY`: AWS secret key (if using S3)
