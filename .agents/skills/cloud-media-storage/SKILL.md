---
name: cloud-media-storage
description: Production cloud media storage patterns for Django and Next.js using S3-compatible object storage (AWS S3, Cloudflare R2, MinIO). Covers django-storages, presigned upload URLs, private medical document encryption, and WebP optimization.
keywords:
  - media-storage
  - s3
  - cloudflare-r2
  - minio
  - django-storages
  - presigned-urls
  - uploads
  - nextjs
  - medical-documents
license: MIT
---

# Cloud & S3 Media Storage Architecture

A comprehensive production guide for handling user uploads, high-resolution medical imagery, clinical PDFs, and public magazine media using S3-compatible object storage (AWS S3, Cloudflare R2, MinIO, ArvanCloud) with **Django** and **Next.js**.

---

## 1. Two-Tier Storage Architecture

In healthcare and editorial platforms, media MUST be separated into two distinct storage policies:

1. **Public Bucket (`pezeshkan-public-media`):**
   - Articles cover images, doctor avatars, cluster infographics.
   - Public read access via CDN (`https://cdn.pezeshkan.com/...`).
   - Long-term browser caching (`Cache-Control: public, max-age=31536000, immutable`).
2. **Private Encrypted Bucket (`pezeshkan-private-clinical`):**
   - Patient test results, prescription scans, medical records (PHI).
   - Zero public access; Server-Side Encryption (SSE-S3 or SSE-KMS).
   - Time-limited Presigned URLs only (expire after 10–15 minutes).

---

## 2. Django Backend Integration (`django-storages` + `boto3`)

### Installation:
```bash
pip install django-storages[boto3] pillow
```

### Storage Backends Configuration (`core/storage_backends.py`):
```python
from storages.backends.s3boto3 import S3Boto3Storage

class PublicMediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False

class PrivateMedicalStorage(S3Boto3Storage):
    location = 'clinical_records'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False  # Always use signed S3 URLs
```

### Django Settings (`settings.py`):
```python
import os

AWS_ACCESS_KEY_ID = os.environ.get('S3_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('S3_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'pezeshkan-media')
AWS_S3_ENDPOINT_URL = os.environ.get('S3_ENDPOINT_URL') # e.g. https://<account_id>.r2.cloudflarestorage.com
AWS_S3_REGION_NAME = os.environ.get('S3_REGION', 'auto')
AWS_DEFAULT_ACL = None
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_FILE_OVERWRITE = False

# Default storage classes
DEFAULT_FILE_STORAGE = 'core.storage_backends.PublicMediaStorage'
PRIVATE_FILE_STORAGE = 'core.storage_backends.PrivateMedicalStorage'
```

### Model Usage:
```python
from django.db import models
from core.storage_backends import PublicMediaStorage, PrivateMedicalStorage

class Article(models.Model):
    title = models.CharField(max_length=255)
    # Stored publicly on CDN
    cover_image = models.ImageField(storage=PublicMediaStorage(), upload_to='articles/%Y/%m/')

class PatientRecord(models.Model):
    patient_id = models.CharField(max_length=64)
    # Encrypted private storage with restricted access
    medical_scan = models.FileField(storage=PrivateMedicalStorage(), upload_to='scans/%Y/')
```

---

## 3. High-Performance Direct Upload via Presigned URLs

Do not route large image and video uploads through Django server processes — it ties up WSGI/ASGI workers. Instead, have Django generate a **Presigned URL**, and let Next.js upload directly to S3.

### Django Presigned URL Endpoint (`api/views.py`):
```python
import boto3
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

class GeneratePresignedUploadUrl(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file_name = request.data.get('filename')
        file_type = request.data.get('filetype')
        folder = request.data.get('folder', 'uploads')

        s3_client = boto3.client(
            's3',
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )

        key = f"{folder}/{request.user.id}_{file_name}"

        presigned_post = s3_client.generate_presigned_post(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=key,
            Fields={"Content-Type": file_type},
            Conditions=[
                {"Content-Type": file_type},
                ["content-length-range", 100, 10 * 1024 * 1024] # Max 10MB
            ],
            ExpiresIn=300 # 5 minutes
        )

        return Response(presigned_post)
```

### Next.js Client Upload:
```typescript
export async function uploadFileToS3(file: File, folder: string = 'articles'): Promise<string> {
  // 1. Get presigned post data from Django
  const token = localStorage.getItem('access_token');
  const res = await fetch('/api/v1/media/presigned-url/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ filename: file.name, filetype: file.type, folder }),
  });
  
  const presigned = await res.json();

  // 2. Upload directly to S3/R2
  const formData = new FormData();
  Object.entries(presigned.fields).forEach(([key, val]) => {
    formData.append(key, val as string);
  });
  formData.append('file', file);

  const uploadRes = await fetch(presigned.url, {
    method: 'POST',
    body: formData,
  });

  if (!uploadRes.ok) throw new Error('بارگذاری فایل ناموفق بود');

  return `${presigned.url}/${presigned.fields.key}`;
}
```

---

## 4. Production Checklist

- [ ] CORS configuration in S3/R2 bucket allows `PUT` and `POST` from `https://pezeshkan.com`.
- [ ] Automated WebP conversion configured (via Lambda, Cloudflare Image Resizing, or Celery).
- [ ] Max file size bounded at API level (prevent storage exhaustion attacks).
- [ ] MIME-type validation prevents uploading executable scripts (`.php`, `.exe`, `.sh`).
