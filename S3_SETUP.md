# S3 Bucket Setup and Validation

## Overview

The application now supports both **local file storage** (default) and **AWS S3** storage. S3 integration includes comprehensive bucket validation to ensure proper configuration and access.

## Features

✅ **S3 Bucket Validation** - Validates bucket existence and permissions on startup  
✅ **Automatic Fallback** - Uses local storage if S3 is not configured  
✅ **Load Balancer Compatible** - Works seamlessly with multiple backend instances  
✅ **Encryption** - Files are encrypted before upload to S3  
✅ **Server-Side Encryption** - Additional AES256 encryption at S3 level  

## Configuration

### Environment Variables

Set these environment variables to enable S3:

```bash
# Enable S3 storage
USE_S3=true

# Required S3 settings
S3_BUCKET_NAME=your-bucket-name
S3_REGION=us-east-1

# AWS Credentials (or use IAM roles)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key

# Optional: For S3-compatible services (MinIO, DigitalOcean Spaces, etc.)
S3_ENDPOINT_URL=https://s3.example.com
```

### Local Storage (Default)

If `USE_S3` is not set or set to `false`, the application uses local file storage in the `backend/storage/` directory.

## S3 Bucket Validation

The application performs comprehensive validation:

### 1. **Startup Validation**
- Checks if bucket exists
- Verifies read permissions
- Tests write permissions
- Validates AWS credentials

### 2. **Health Check Endpoint**
- `GET /api/health` - Returns storage status and S3 connection status

### 3. **Validation Checks**

#### Bucket Existence
- Verifies the bucket exists using `head_bucket`
- Returns clear error if bucket doesn't exist

#### Access Permissions
- Checks for 403 (Access Denied) errors
- Validates AWS credentials are correct

#### Write Permissions
- Creates a test object in the bucket
- Immediately deletes the test object
- Ensures write operations will work

## Error Messages

The validation provides clear error messages:

- **Bucket doesn't exist**: `S3 bucket 'bucket-name' does not exist`
- **Access denied**: `Access denied to S3 bucket 'bucket-name'. Check your AWS credentials.`
- **Connection error**: `Failed to connect to S3: [error details]`
- **Write permission error**: `No write permission to S3 bucket 'bucket-name': [error details]`

## Usage

### With S3 Enabled

1. Set environment variables:
```bash
export USE_S3=true
export S3_BUCKET_NAME=my-secure-docs
export S3_REGION=us-east-1
export AWS_ACCESS_KEY_ID=AKIA...
export AWS_SECRET_ACCESS_KEY=...
```

2. Start the server - validation runs automatically:
```bash
cd backend
uvicorn app.main:app --reload
```

3. Check health status:
```bash
curl http://localhost:8000/api/health
```

### Without S3 (Local Storage)

Simply don't set `USE_S3` or set it to `false`. The application will use local storage automatically.

## Production Deployment

### Recommended S3 Setup

1. **Create S3 Bucket**:
   - Use a dedicated bucket for encrypted documents
   - Enable versioning (optional)
   - Set lifecycle policies for automatic cleanup

2. **IAM Policy** (Minimum required permissions):
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject",
        "s3:HeadBucket"
      ],
      "Resource": "arn:aws:s3:::your-bucket-name/*"
    },
    {
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::your-bucket-name"
    }
  ]
}
```

3. **Use IAM Roles** (Recommended):
   - Instead of access keys, use IAM roles when running on EC2/ECS/Lambda
   - More secure and easier to manage

4. **Bucket Configuration**:
   - Enable server-side encryption (AES256 or KMS)
   - Set up bucket policies for additional security
   - Configure CORS if needed for direct browser uploads

## S3-Compatible Services

The application also works with S3-compatible services:

- **MinIO** (Self-hosted)
- **DigitalOcean Spaces**
- **Wasabi**
- **Backblaze B2**
- **Any S3-compatible API**

Just set the `S3_ENDPOINT_URL` environment variable.

## Troubleshooting

### Validation Fails on Startup

1. Check bucket name is correct
2. Verify AWS credentials have proper permissions
3. Ensure bucket exists in the specified region
4. Check network connectivity to AWS

### Files Not Uploading

1. Verify write permissions on the bucket
2. Check bucket policy allows PutObject
3. Ensure encryption key is set correctly

### Files Not Downloading

1. Verify read permissions on the bucket
2. Check bucket policy allows GetObject
3. Ensure file exists in the bucket

## Health Check Response

```json
{
  "status": "healthy",
  "storage": "S3",
  "s3_bucket": "your-bucket-name",
  "s3_status": "connected"
}
```

Or if there's an error:

```json
{
  "status": "healthy",
  "storage": "S3",
  "s3_status": "error",
  "s3_error": "Error message here"
}
```
