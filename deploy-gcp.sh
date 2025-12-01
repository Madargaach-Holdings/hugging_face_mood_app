#!/bin/bash
# Quick deployment script for GCP Cloud Run
# Usage: ./deploy-gcp.sh [REGION] [REPOSITORY_NAME] [HF_TOKEN]

set -e  # Exit on error

# Configuration (can be overridden by command line args)
REGION=${1:-us-central1}
REPOSITORY_NAME=${2:-mood-app-repo}
HF_TOKEN=${3:-${HF_TOKEN}}

# Get project ID
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)

if [ -z "$PROJECT_ID" ]; then
    echo "❌ Error: No GCP project selected. Run 'gcloud init' first."
    exit 1
fi

if [ -z "$HF_TOKEN" ]; then
    echo "❌ Error: HF_TOKEN not set. Provide it as argument or set environment variable."
    echo "Usage: ./deploy-gcp.sh [REGION] [REPOSITORY_NAME] [HF_TOKEN]"
    exit 1
fi

echo "🚀 Deploying Mood App API to GCP Cloud Run"
echo "📍 Project: $PROJECT_ID"
echo "🌍 Region: $REGION"
echo "📦 Repository: $REPOSITORY_NAME"
echo ""

# Step 1: Enable APIs
echo "📋 Step 1: Enabling required APIs..."
gcloud services enable artifactregistry.googleapis.com --quiet
gcloud services enable run.googleapis.com --quiet
gcloud services enable cloudbuild.googleapis.com --quiet
echo "✅ APIs enabled"
echo ""

# Step 2: Create Artifact Registry repository (if it doesn't exist)
echo "📋 Step 2: Setting up Artifact Registry..."
if ! gcloud artifacts repositories describe $REPOSITORY_NAME --location=$REGION &>/dev/null; then
    echo "Creating repository $REPOSITORY_NAME in $REGION..."
    gcloud artifacts repositories create $REPOSITORY_NAME \
        --repository-format=docker \
        --location=$REGION \
        --description="Docker repository for mood app API" \
        --quiet
    echo "✅ Repository created"
else
    echo "✅ Repository already exists"
fi

# Configure Docker authentication
gcloud auth configure-docker ${REGION}-docker.pkg.dev --quiet
echo ""

# Step 3: Build and push image
echo "📋 Step 3: Building and pushing Docker image..."
IMAGE_URL="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY_NAME}/mood-app-api:latest"
gcloud builds submit --tag $IMAGE_URL
echo "✅ Image built and pushed: $IMAGE_URL"
echo ""

# Step 4: Deploy to Cloud Run
echo "📋 Step 4: Deploying to Cloud Run..."
gcloud run deploy mood-app-api \
    --image $IMAGE_URL \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --set-env-vars HF_TOKEN=$HF_TOKEN \
    --port 8080 \
    --quiet

echo "✅ Deployment complete!"
echo ""

# Step 5: Get service URL
SERVICE_URL=$(gcloud run services describe mood-app-api \
    --region $REGION \
    --format 'value(status.url)')

echo "🌐 Your app is live at:"
echo "   $SERVICE_URL"
echo ""
echo "📝 Next steps:"
echo "   1. Test the URL in your browser"
echo "   2. Set up cost monitoring in GCP Console → Billing → Budgets & Alerts"
echo "   3. Add the URL to the class Google Sheet"
echo ""

