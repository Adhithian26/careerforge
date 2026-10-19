#!/usr/bin/env bash
# CareerForge AI - Google Cloud Run Automated Deployment Script
set -e

PROJECT_ID=${1:-$(gcloud config get-value project)}
REGION=${2:-"us-central1"}

if [ -z "$PROJECT_ID" ]; then
  echo "Error: No Google Cloud Project ID provided or configured."
  echo "Usage: ./deploy.sh <PROJECT_ID> [REGION]"
  exit 1
fi

echo "🚀 Deploying CareerForge AI to Google Cloud Run (Project: $PROJECT_ID, Region: $REGION)..."

# 1. Enable Required Google Cloud APIs
echo "Enabling Cloud Run, Secret Manager, and Container Registry APIs..."
gcloud services enable run.googleapis.com \
  secretmanager.googleapis.com \
  containerregistry.googleapis.com \
  artifactregistry.googleapis.com \
  --project="$PROJECT_ID"

# 2. Build and Push Backend Container
echo "Building backend container..."
gcloud builds submit --tag "gcr.io/$PROJECT_ID/careerforge-backend:latest" -f backend/Dockerfile . --project="$PROJECT_ID"

# 3. Deploy Backend Service to Cloud Run
echo "Deploying backend service..."
gcloud run deploy careerforge-backend \
  --image="gcr.io/$PROJECT_ID/careerforge-backend:latest" \
  --platform=managed \
  --region="$REGION" \
  --allow-unauthenticated \
  --port=8080 \
  --memory=512Mi \
  --min-instances=0 \
  --max-instances=3 \
  --set-env-vars="ENVIRONMENT=production,DEBUG=False" \
  --project="$PROJECT_ID"

BACKEND_URL=$(gcloud run services describe careerforge-backend --platform=managed --region="$REGION" --format="value(status.url)" --project="$PROJECT_ID")
echo "✅ Backend successfully deployed to: $BACKEND_URL"

# 4. Build and Deploy Frontend Container
echo "Building frontend container..."
gcloud builds submit --tag "gcr.io/$PROJECT_ID/careerforge-frontend:latest" -f frontend/Dockerfile . --project="$PROJECT_ID"

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
  --project="$PROJECT_ID"

FRONTEND_URL=$(gcloud run services describe careerforge-frontend --platform=managed --region="$REGION" --format="value(status.url)" --project="$PROJECT_ID")
echo "✅ Frontend successfully deployed to: $FRONTEND_URL"
echo "🎉 CareerForge AI is now live on Google Cloud Run!"
