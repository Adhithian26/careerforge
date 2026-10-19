# CareerForge AI - Google Cloud Run PowerShell Deployment Script
param (
    [string]$ProjectId = $(gcloud config get-value project 2>$null),
    [string]$Region = "us-central1"
)

if (-not $ProjectId) {
    Write-Error "No Google Cloud Project ID configured. Run 'gcloud auth login' and 'gcloud config set project <ID>'"
    exit 1
}

Write-Host "🚀 Deploying CareerForge AI to Google Cloud Run (Project: $ProjectId, Region: $Region)..." -ForegroundColor Cyan

# 1. Enable Services
Write-Host "Enabling Google Cloud APIs..." -ForegroundColor Yellow
gcloud services enable run.googleapis.com secretmanager.googleapis.com containerregistry.googleapis.com artifactregistry.googleapis.com --project=$ProjectId

# 2. Build & Deploy Backend
Write-Host "Building and deploying backend..." -ForegroundColor Yellow
gcloud builds submit --tag "gcr.io/$ProjectId/careerforge-backend:latest" -f backend/Dockerfile . --project=$ProjectId
gcloud run deploy careerforge-backend `
    --image="gcr.io/$ProjectId/careerforge-backend:latest" `
    --platform=managed `
    --region=$Region `
    --allow-unauthenticated `
    --port=8080 `
    --memory=512Mi `
    --min-instances=0 `
    --max-instances=3 `
    --set-env-vars="ENVIRONMENT=production,DEBUG=False" `
    --project=$ProjectId

$BackendUrl = $(gcloud run services describe careerforge-backend --platform=managed --region=$Region --format="value(status.url)" --project=$ProjectId)
Write-Host "✅ Backend deployed at: $BackendUrl" -ForegroundColor Green

# 3. Build & Deploy Frontend
Write-Host "Building and deploying frontend..." -ForegroundColor Yellow
gcloud builds submit --tag "gcr.io/$ProjectId/careerforge-frontend:latest" -f frontend/Dockerfile . --project=$ProjectId
gcloud run deploy careerforge-frontend `
    --image="gcr.io/$ProjectId/careerforge-frontend:latest" `
    --platform=managed `
    --region=$Region `
    --allow-unauthenticated `
    --port=8080 `
    --memory=256Mi `
    --min-instances=0 `
    --max-instances=3 `
    --project=$ProjectId

$FrontendUrl = $(gcloud run services describe careerforge-frontend --platform=managed --region=$Region --format="value(status.url)" --project=$ProjectId)
Write-Host "🎉 CareerForge AI Frontend Live at: $FrontendUrl" -ForegroundColor Green
