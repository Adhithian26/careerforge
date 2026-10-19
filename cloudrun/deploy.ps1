# CareerForge AI - Google Cloud Run PowerShell Deployment Script
param (
    [string]$ProjectId = $(gcloud config get-value project 2>$null),
    [string]$Region = "us-central1"
)

# Resolve project root automatically
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (Test-Path (Join-Path $ScriptDir "..\backend\Dockerfile")) {
    $ProjectRoot = Resolve-Path (Join-Path $ScriptDir "..")
    Set-Location $ProjectRoot
}

if (-not $ProjectId) {
    Write-Error "No Google Cloud Project ID configured. Run 'gcloud auth login' and 'gcloud config set project <ID>'"
    exit 1
}

Write-Host "🚀 Deploying CareerForge AI to Google Cloud Run (Project: $ProjectId, Region: $Region)..." -ForegroundColor Cyan
Write-Host "Working Directory: $(Get-Location)" -ForegroundColor Gray

# Read local .env if available to propagate Gemini key
$GeminiKey = ""
if (Test-Path ".env") {
    $envContent = Get-Content ".env"
    foreach ($line in $envContent) {
        if ($line -match "^GEMINI_API_KEY=(.+)$") {
            $GeminiKey = $matches[1].Trim()
        }
    }
}

# 1. Enable Services
Write-Host "Enabling Google Cloud APIs (Cloud Run, Artifact Registry, Cloud Build)..." -ForegroundColor Yellow
gcloud services enable run.googleapis.com cloudbuild.googleapis.com secretmanager.googleapis.com artifactregistry.googleapis.com --project=$ProjectId

# 2. Build & Deploy Backend
Write-Host "Building and deploying backend container..." -ForegroundColor Yellow
gcloud builds submit --tag "gcr.io/$ProjectId/careerforge-backend:latest" -f backend/Dockerfile . --project=$ProjectId

$backendEnv = "ENVIRONMENT=production,DEBUG=False,GEMINI_MODEL=gemini-flash-lite-latest"
if ($GeminiKey) {
    $backendEnv += ",GEMINI_API_KEY=$GeminiKey"
}

gcloud run deploy careerforge-backend `
    --image="gcr.io/$ProjectId/careerforge-backend:latest" `
    --platform=managed `
    --region=$Region `
    --allow-unauthenticated `
    --port=8080 `
    --memory=512Mi `
    --min-instances=0 `
    --max-instances=3 `
    --set-env-vars="$backendEnv" `
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
