#!/usr/bin/env bash
# CareerForge AI - Google Cloud Run Automated Deployment Script
set -e

PROJECT_ID=${1:-$(gcloud config get-value project 2>/dev/null)}
REGION=${2:-"us-central1"}

if [ -z "$PROJECT_ID" ]; then
  echo "Error: No Google Cloud Project ID provided or configured."
  echo "Usage: ./deploy.sh <PROJECT_ID> [REGION]"
  exit 1
fi

echo "🚀 Deploying CareerForge AI to Google Cloud Run (Project: $PROJECT_ID, Region: $REGION)..."

# Extract Gemini API Key if present in .env
GEMINI_KEY=""
if [ -f ".env" ]; then
  GEMINI_KEY=$(grep -E '^GEMINI_API_KEY=' .env | cut -d '=' -f2- | tr -d '\r\n')
fi

# 1. Enable Required Google Cloud APIs
echo "Enabling Cloud Run, Cloud Build, and Artifact Registry APIs..."
gcloud services enable run.googleapis.com \
  cloudbuild.googleapis.com \
  secretmanager.googleapis.com \
  artifactregistry.googleapis.com \
  --project="$PROJECT_ID" --quiet

# 2. Build and Push Backend Container
echo "Building backend container..."
gcloud builds submit --tag "gcr.io/$PROJECT_ID/careerforge-backend:latest" -f backend/Dockerfile . --project="$PROJECT_ID" --quiet

# 3. Deploy Backend Service to Cloud Run
echo "Deploying backend service..."
BACKEND_ENV="ENVIRONMENT=production,DEBUG=False,GEMINI_MODEL=gemini-flash-lite-latest,CORS_ORIGINS=*"
if [ -n "$GEMINI_KEY" ]; then
  BACKEND_ENV="$BACKEND_ENV,GEMINI_API_KEY=$GEMINI_KEY"
fi

gcloud run deploy careerforge-backend \
  --image="gcr.io/$PROJECT_ID/careerforge-backend:latest" \
  --platform=managed \
  --region="$REGION" \
  --allow-unauthenticated \
  --port=8080 \
  --memory=512Mi \
  --min-instances=0 \
  --max-instances=3 \
  --set-env-vars="$BACKEND_ENV" \
  --project="$PROJECT_ID" \
  --quiet

BACKEND_URL=$(gcloud run services describe careerforge-backend --platform=managed --region="$REGION" --format="value(status.url)" --project="$PROJECT_ID")
echo "✅ Backend successfully deployed to: $BACKEND_URL"

# 4. Inject Backend URL into Frontend build
echo "Configuring frontend build with backend URL: $BACKEND_URL/api/v1"
echo "VITE_API_BASE=$BACKEND_URL/api/v1" > frontend/.env.production

# 5. Build and Deploy Frontend Container
echo "Building frontend container..."
gcloud builds submit --tag "gcr.io/$PROJECT_ID/careerforge-frontend:latest" -f frontend/Dockerfile . --project="$PROJECT_ID" --quiet

echo "Deploying frontend service..."
gcloud run deploy careerforge-frontend \
  --image="gcr.io/$PROJECT_ID/careerforge-frontend:latest" \
  --platform=managed \
  --region="$REGION" \
  --allow-unauthenticated \
  --port=8080 \
  --memory=256Mi \
  --min-instances=0 \
  --max-instances=3 \
  --project="$PROJECT_ID" \
  --quiet

FRONTEND_URL=$(gcloud run services describe careerforge-frontend --platform=managed --region="$REGION" --format="value(status.url)" --project="$PROJECT_ID")
echo ""
echo "========================================================"
echo "🎉 CareerForge AI Frontend Live at: $FRONTEND_URL"
echo "⚡ Backend API Live at:             $BACKEND_URL"
echo "🔍 Health Check:                    $BACKEND_URL/health"
echo "========================================================"
