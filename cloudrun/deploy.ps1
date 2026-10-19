# CareerForge AI - Google Cloud Run PowerShell Deployment Script
param (
    [string]$ProjectId = "",
    [string]$Region = "us-central1"
)

# 1. Automatically locate and prepend gcloud to PATH if not already in session PATH
if (-not (Get-Command gcloud -ErrorAction SilentlyContinue)) {
    $potentialGcloudPaths = @(
        "E:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin",
        "C:\Users\$($env:USERNAME)\OneDrive\Desktop\google-cloud-sdk\bin",
        "$env:LOCALAPPDATA\Google\Cloud SDK\google-cloud-sdk\bin",
        "C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin",
        "C:\Program Files\Google\Cloud SDK\google-cloud-sdk\bin"
    )
    foreach ($p in $potentialGcloudPaths) {
        if (Test-Path (Join-Path $p "gcloud.cmd")) {
            $env:PATH = "$p;" + $env:PATH
            Write-Host "Detected Google Cloud SDK: $p" -ForegroundColor Cyan
            break
        }
    }
}

if (-not (Get-Command gcloud -ErrorAction SilentlyContinue)) {
    Write-Error "Google Cloud SDK ('gcloud') not found in PATH or standard install directories. Please add it to PATH."
    exit 1
}

# Resolve project root automatically
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (Test-Path (Join-Path $ScriptDir "..\backend\Dockerfile")) {
    $ProjectRoot = Resolve-Path (Join-Path $ScriptDir "..")
    Set-Location $ProjectRoot
}

# Resolve ProjectId if not passed
if (-not $ProjectId) {
    $ProjectId = $(gcloud config get-value project 2>$null)
}

if (-not $ProjectId) {
    Write-Error "No Google Cloud Project ID configured. Run 'gcloud auth login' and 'gcloud config set project <ID>', or pass -ProjectId <ID>"
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
gcloud services enable run.googleapis.com cloudbuild.googleapis.com secretmanager.googleapis.com artifactregistry.googleapis.com --project=$ProjectId --quiet

# 2. Build & Deploy Backend
Write-Host "Building and deploying backend container..." -ForegroundColor Yellow
gcloud builds submit --tag "gcr.io/$ProjectId/careerforge-backend:latest" -f backend/Dockerfile . --project=$ProjectId --quiet

$backendEnv = "ENVIRONMENT=production,DEBUG=False,GEMINI_MODEL=gemini-flash-lite-latest,CORS_ORIGINS=*"
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
    --project=$ProjectId `
    --quiet

$BackendUrl = $(gcloud run services describe careerforge-backend --platform=managed --region=$Region --format="value(status.url)" --project=$ProjectId)
Write-Host "✅ Backend deployed at: $BackendUrl" -ForegroundColor Green

# 3. Configure Frontend with Backend URL
Write-Host "Configuring frontend build with backend endpoint: $BackendUrl/api/v1" -ForegroundColor Cyan
"VITE_API_BASE=$BackendUrl/api/v1" | Out-File -FilePath "frontend\.env.production" -Encoding utf8

# 4. Build & Deploy Frontend
Write-Host "Building and deploying frontend container..." -ForegroundColor Yellow
gcloud builds submit --tag "gcr.io/$ProjectId/careerforge-frontend:latest" -f frontend/Dockerfile . --project=$ProjectId --quiet

gcloud run deploy careerforge-frontend `
    --image="gcr.io/$ProjectId/careerforge-frontend:latest" `
    --platform=managed `
    --region=$Region `
    --allow-unauthenticated `
    --port=8080 `
    --memory=256Mi `
    --min-instances=0 `
    --max-instances=3 `
    --project=$ProjectId `
    --quiet

$FrontendUrl = $(gcloud run services describe careerforge-frontend --platform=managed --region=$Region --format="value(status.url)" --project=$ProjectId)
Write-Host "`n========================================================" -ForegroundColor Green
Write-Host "🎉 CareerForge AI Frontend Live at: $FrontendUrl" -ForegroundColor Green
Write-Host "⚡ Backend API Live at:             $BackendUrl" -ForegroundColor Green
Write-Host "🔍 Health Check:                    $BackendUrl/health" -ForegroundColor Green
Write-Host "========================================================`n" -ForegroundColor Green
