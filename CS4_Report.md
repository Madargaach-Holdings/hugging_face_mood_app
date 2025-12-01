# DS/CS553 - Machine Learning Development and Operations (MLOps)
## Case Study 4: Cloud Deployment Report

**Group Members:** Ujjwal Pandit
**Date:** December 1, 2025
**Project:** API-Based Mood App - Cloud Deployment

---

## Executive Summary

This report documents the deployment of our API-based product from Case Study 1 to three major cloud platforms: Google Cloud Platform (GCP), Microsoft Azure, and Amazon Web Services (AWS). The application generates positive motivational messages using Hugging Face's Inference API and has been containerized using Docker for seamless cloud deployment.

---

## 1. GCP Cloud Run Deployment

### 1.1 Account Setup

**Process:**
1. Created a new GCP project: `mlops-cs4-mood-app`
2. Enabled billing account (required even for Free Tier usage)
3. Linked billing account `01777E-45F772-FDB743` to the project

**Challenges:**
- Initial API enablement failed due to billing not being linked
- Resolved by linking billing account via CLI: `gcloud billing projects link`

**Free Tier Benefits:**
- 2 million requests per month for Cloud Run
- 0.5 GB storage for Artifact Registry
- 120 build-minutes per day for Cloud Build

### 1.2 Cost Monitoring Setup

**Configuration:**
- Created budget alert in GCP Console → Billing → Budgets & Alerts
- Budget amount: $1.00 USD (low threshold to catch any charges early)
- Alert thresholds: 10%, 50%, 90%, 100% of budget
- Email notifications configured for immediate alerts

**Rationale:**
Setting a $1 budget ensures immediate notification if usage exceeds Free Tier limits, providing time to stop or delete resources before incurring significant charges.

### 1.3 Deployment Process

#### Step 1: Environment Setup
```bash
# Enable required APIs
gcloud services enable artifactregistry.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

#### Step 2: Artifact Registry Repository
```bash
# Create Docker repository
gcloud artifacts repositories create mood-app-repo \
  --repository-format=docker \
  --location=us-central1 \
  --description="Docker repository for mood app API"

# Configure Docker authentication
gcloud auth configure-docker us-central1-docker.pkg.dev
```

#### Step 3: Build and Push Docker Image
```bash
# Build and push in one step using Cloud Build
gcloud builds submit \
  --tag us-central1-docker.pkg.dev/mlops-cs4-mood-app/mood-app-repo/mood-app-api:latest
```

**Build Details:**
- Base image: `python:3.10-slim`
- Dependencies: `gradio>=4.0`, `huggingface-hub>=0.20`
- Build time: ~1 minute 10 seconds
- Image size: Optimized for fast startup

#### Step 4: Deploy to Cloud Run
```bash
gcloud run deploy mood-app-api \
  --image us-central1-docker.pkg.dev/mlops-cs4-mood-app/mood-app-repo/mood-app-api:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars HF_TOKEN=your_huggingface_token_here \
  --port 8080
```

**Deployment Configuration:**
- Service name: `mood-app-api`
- Region: `us-central1`
- Port: `8080` (Cloud Run default, app reads PORT env var)
- Public access: Enabled (`--allow-unauthenticated`)
- Environment variable: `HF_TOKEN` set securely

### 1.4 Modifications for GCP Environment

**Key Adaptations:**
1. **Port Configuration:** App reads `PORT` environment variable (Cloud Run sets `PORT=8080`)
2. **Public Access:** Enabled unauthenticated access for public API requirement
3. **Environment Variables:** `HF_TOKEN` passed via `--set-env-vars` flag
4. **Image Registry:** Used Artifact Registry (recommended over Container Registry)

**No Code Changes Required:**
- Application code remained unchanged
- Dockerfile worked as-is
- Port binding handled automatically by Cloud Run

### 1.5 Deployment Results

**Service URL:** https://mood-app-api-882683351624.us-central1.run.app

**Verification:**
- ✅ Service deployed successfully
- ✅ Gradio interface accessible via public URL
- ✅ API calls to Hugging Face working correctly
- ✅ Response times: ~5-10 seconds (typical for API-based generation)

**Performance:**
- Cold start time: ~10-15 seconds
- Warm requests: ~5-8 seconds
- Service scales automatically based on traffic

### 1.6 Challenges and Solutions

**Challenge 1: Billing Account Not Linked**
- **Issue:** APIs couldn't be enabled without billing
- **Solution:** Linked existing billing account via CLI

**Challenge 2: Cloud Build Permissions**
- **Issue:** Permission denied when submitting builds
- **Solution:** Granted `roles/cloudbuild.builds.editor` to user account

**Challenge 3: Docker Authentication**
- **Issue:** Warnings about Docker not in PATH
- **Solution:** Configured Docker credential helper for Artifact Registry

---

## 2. Azure Container Apps Deployment

*[To be completed after Azure deployment]*

### 2.1 Account Setup
*[To be filled]*

### 2.2 Cost Monitoring Setup
*[To be filled]*

### 2.3 Deployment Process
*[To be filled]*

### 2.4 Modifications for Azure Environment
*[To be filled]*

### 2.5 Deployment Results
*[To be filled]*

### 2.6 Challenges and Solutions
*[To be filled]*

---

## 3. AWS ECS Deployment

*[To be completed after AWS deployment]*

### 3.1 Account Setup
*[To be filled]*

### 3.2 Cost Monitoring Setup
*[To be filled]*

### 3.3 Deployment Process
*[To be filled]*

### 3.4 Modifications for AWS Environment
*[To be filled]*

### 3.5 Deployment Results
*[To be filled]*

### 3.6 Challenges and Solutions
*[To be filled]*

---

## 4. Additional Insights, Challenges, and Future Improvements

### 4.1 Key Learnings

1. **Containerization Benefits:**
   - Docker enabled consistent deployment across all platforms
   - No code changes needed between platforms
   - Environment variables handled uniformly

2. **Cloud Platform Differences:**
   - GCP Cloud Run: Simplest deployment, automatic scaling
   - Azure Container Apps: [To be updated]
   - AWS ECS: [To be updated]

3. **Cost Management:**
   - Free Tier limits vary by platform
   - Budget alerts are essential for monitoring
   - Early detection prevents unexpected charges

### 4.2 Challenges Faced

1. **Billing Requirements:**
   - All platforms require billing accounts even for Free Tier
   - Initial setup can be confusing for first-time users

2. **Permission Management:**
   - IAM roles and permissions vary by platform
   - Service accounts need proper configuration

3. **Port Configuration:**
   - Different platforms use different default ports
   - Solution: Read PORT from environment variable

### 4.3 Future Improvements

1. **CI/CD Pipeline:**
   - Set up GitHub Actions for automatic deployment
   - Deploy to all three platforms on code push

2. **Monitoring and Logging:**
   - Integrate application-level monitoring
   - Set up centralized logging across platforms

3. **Performance Optimization:**
   - Implement caching for API responses
   - Optimize container image size further

4. **Security Enhancements:**
   - Use secrets management services
   - Implement authentication for production use

5. **Multi-Region Deployment:**
   - Deploy to multiple regions for redundancy
   - Implement load balancing

---

## 5. Comparison of Cloud Platforms

| Aspect | GCP Cloud Run | Azure Container Apps | AWS ECS |
|--------|---------------|----------------------|---------|
| **Ease of Setup** | ⭐⭐⭐⭐⭐ Very Easy | *[To be filled]* | *[To be filled]* |
| **Deployment Time** | ~2 minutes | *[To be filled]* | *[To be filled]* |
| **Free Tier Limits** | 2M requests/month | *[To be filled]* | *[To be filled]* |
| **Scaling** | Automatic | *[To be filled]* | *[To be filled]* |
| **Documentation** | Excellent | *[To be filled]* | *[To be filled]* |
| **Cost Monitoring** | Budget alerts | *[To be filled]* | *[To be filled]* |

---

## 6. Conclusion

The deployment to GCP Cloud Run was successful and straightforward. The containerized application required no code modifications and deployed seamlessly. The Free Tier provides ample resources for development and testing purposes.

*[Azure and AWS sections will be completed after respective deployments]*

---

## Appendix A: Deployment Commands Reference

### GCP Cloud Run
```bash
# Enable APIs
gcloud services enable artifactregistry.googleapis.com run.googleapis.com cloudbuild.googleapis.com

# Create repository
gcloud artifacts repositories create mood-app-repo \
  --repository-format=docker --location=us-central1

# Build and push
gcloud builds submit --tag us-central1-docker.pkg.dev/mlops-cs4-mood-app/mood-app-repo/mood-app-api:latest

# Deploy
gcloud run deploy mood-app-api \
  --image us-central1-docker.pkg.dev/mlops-cs4-mood-app/mood-app-repo/mood-app-api:latest \
  --platform managed --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars HF_TOKEN=your_token \
  --port 8080
```

### Azure Container Apps
*[To be added]*

### AWS ECS
*[To be added]*

---

## Appendix B: Service URLs

- **GCP Cloud Run:** https://mood-app-api-882683351624.us-central1.run.app
- **Azure Container Apps:** *[To be added]*
- **AWS ECS:** *[To be added]*

---

**Report Status:** In Progress - GCP section complete, Azure and AWS sections pending.

