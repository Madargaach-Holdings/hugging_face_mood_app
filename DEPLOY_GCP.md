# GCP Cloud Run Deployment Guide

Complete step-by-step guide for deploying the API-based Mood App to Google Cloud Platform's Cloud Run.

## Prerequisites

- GCP account with billing enabled (Free Tier is sufficient)
- `gcloud` CLI installed ([Installation Guide](https://cloud.google.com/sdk/docs/install))
- Hugging Face API token (`HF_TOKEN`)

## Step 1: Set up GCP Environment

### 1.1 Install and Initialize gcloud CLI

```bash
# If not installed, download from: https://cloud.google.com/sdk/docs/install
# Then initialize:
gcloud init

# Select your project or create a new one
# Choose a default region (e.g., us-central1)
```

### 1.2 Enable Required APIs

```bash
# Enable Artifact Registry API (for storing Docker images)
gcloud services enable artifactregistry.googleapis.com

# Enable Cloud Run API (for deploying containers)
gcloud services enable run.googleapis.com

# Enable Cloud Build API (for building images)
gcloud services enable cloudbuild.googleapis.com
```

### 1.3 Create Artifact Registry Repository

```bash
# Set variables (customize as needed)
export REGION=us-central1
export REPOSITORY_NAME=mood-app-repo
export PROJECT_ID=$(gcloud config get-value project)

# Create Docker repository
gcloud artifacts repositories create $REPOSITORY_NAME \
  --repository-format=docker \
  --location=$REGION \
  --description="Docker repository for mood app API"

# Configure Docker authentication
gcloud auth configure-docker ${REGION}-docker.pkg.dev
```

## Step 2: Build and Push Docker Image

### Option A: Build and Push in One Step (Recommended)

```bash
# This builds the image in the cloud and pushes it automatically
gcloud builds submit --tag ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY_NAME}/mood-app-api:latest
```

### Option B: Build Locally, Tag, and Push

```bash
# Build locally
docker build -t mood-app-api:latest .

# Tag for Artifact Registry
docker tag mood-app-api:latest \
  ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY_NAME}/mood-app-api:latest

# Push to Artifact Registry
docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY_NAME}/mood-app-api:latest
```

## Step 3: Deploy to Cloud Run

```bash
# Deploy the service
gcloud run deploy mood-app-api \
  --image ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY_NAME}/mood-app-api:latest \
  --platform managed \
  --region ${REGION} \
  --allow-unauthenticated \
  --set-env-vars HF_TOKEN=your_huggingface_token_here \
  --port 8080

# Note: Replace 'your_huggingface_token_here' with your actual HF_TOKEN
```

**Important Flags:**
- `--allow-unauthenticated`: Makes your service publicly accessible (required for assignment)
- `--set-env-vars HF_TOKEN=...`: Sets your Hugging Face token as an environment variable
- `--port 8080`: Cloud Run's default port (our app reads PORT env var automatically)

## Step 4: Verify Deployment

After deployment, Cloud Run will display your service URL. Test it:

```bash
# Get the service URL
SERVICE_URL=$(gcloud run services describe mood-app-api \
  --region ${REGION} \
  --format 'value(status.url)')

echo "Your app is available at: $SERVICE_URL"

# Test the endpoint
curl $SERVICE_URL
```

Open the URL in your browser to verify the Gradio interface is working.

## Step 5: Set up Cost Monitoring

### 5.1 Create a Budget Alert

1. Go to [GCP Console → Billing](https://console.cloud.google.com/billing)
2. Select your billing account
3. Navigate to **Budgets & Alerts** in the left menu
4. Click **CREATE BUDGET**

### 5.2 Configure Budget

- **Budget name:** `Mood App Free Tier Monitor`
- **Scope:** Select your project
- **Budget amount:** 
  - Budget type: `Specified amount`
  - Amount: `$1.00 USD` (low threshold to catch any charges early)

### 5.3 Set Alert Thresholds

- **Thresholds:** 
  - 10% (early warning)
  - 50% (mid-point)
  - 90% (approaching limit)
  - 100% (budget exceeded)

### 5.4 Configure Recipients

- Add your email address to receive alerts
- You can add multiple email addresses

### 5.5 Finalize

- Click **CREATE** or **FINISH** to save the budget

### Why This Works

- GCP Free Tier includes **2 million requests per month** for Cloud Run
- Setting a $1 budget ensures you get notified immediately if you exceed free tier
- Alerts give you time to stop/delete resources before incurring significant charges

## Troubleshooting

### Issue: "Permission denied" when pushing image

**Solution:**
```bash
gcloud auth configure-docker ${REGION}-docker.pkg.dev
```

### Issue: "API not enabled"

**Solution:**
```bash
gcloud services enable artifactregistry.googleapis.com
gcloud services enable run.googleapis.com
```

### Issue: App not responding

**Check:**
1. Verify `HF_TOKEN` is set correctly: `gcloud run services describe mood-app-api --region ${REGION}`
2. Check logs: `gcloud run services logs read mood-app-api --region ${REGION}`
3. Verify port: Cloud Run sets `PORT=8080` automatically (our app reads this)

### Issue: "Container failed to start"

**Check logs:**
```bash
gcloud run services logs read mood-app-api --region ${REGION} --limit 50
```

Common causes:
- Missing `HF_TOKEN` environment variable
- Port mismatch (should be 8080 for Cloud Run)

## Clean Up (When Done)

To avoid any charges after the assignment:

```bash
# Delete Cloud Run service
gcloud run services delete mood-app-api --region ${REGION}

# Delete Artifact Registry repository (optional)
gcloud artifacts repositories delete ${REPOSITORY_NAME} \
  --location=${REGION}
```

## Resources

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Artifact Registry Documentation](https://cloud.google.com/artifact-registry/docs)
- [GCP Free Tier Limits](https://cloud.google.com/free/docs/free-program)

