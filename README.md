---
title: Dual-Mode Mood App
emoji: 🌟
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.19.2
app_file: app.py
pinned: false
---

# 🌟 Dual-Mode Mood App - MLOps Case Study

[![Sync to HF Space](https://github.com/Madargaach-Holdings/hugging_face_mood_app/actions/workflows/test-and-sync.yml/badge.svg)](https://github.com/Madargaach-Holdings/hugging_face_mood_app/actions/workflows/test-and-sync.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Gradio-based web application for generating positive motivational messages using Hugging Face Inference API. Originally built for DS/CS553 – Machine Learning Development and Operations (MLOps) Case Study 1, now updated for Case Study 4 cloud deployment.

**Live Demo on Hugging Face Spaces:**  
👉 [https://huggingface.co/spaces/upandit/mood-app-api-version](https://huggingface.co/spaces/upandit/mood-app-api-version) 👈

## 🚀 Features

- **API-Based Product:** Generates positive motivational messages using Hugging Face Inference API.
- **Cloud-Ready:** Configured for deployment on GCP Cloud Run, Azure Container Apps, and AWS ECS.
- **Docker Support:** Fully containerized with minimal dependencies for efficient cloud deployment.
- **Environment Variable Support:** Uses `PORT` environment variable for cloud platform compatibility.

## 🛠️ Technical Architecture

### Model Used
| Task | Model | Framework | Deployment |
| :--- | :--- | :--- | :--- |
| Text Generation | [`HuggingFaceTB/SmolLM3-3B`](https://huggingface.co/HuggingFaceTB/SmolLM3-3B) | Hugging Face Inference API | Remote API |

### Tech Stack
- **Frontend:** [Gradio](https://www.gradio.app/)
- **API Client:** [Hugging Face Hub](https://huggingface.co/docs/huggingface_hub)
- **Containerization:** Docker
- **Cloud Platforms:** GCP Cloud Run, Azure Container Apps, AWS ECS

## 📦 Installation & Local Run

To run this application locally:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Madargaach-Holdings/hugging_face_mood_app
    cd hugging_face_mood_app
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    # On macOS/Linux:
    source .venv/bin/activate
    # On Windows (Command Prompt):
    .venv\Scripts\activate.bat
    # On Windows (PowerShell):
    .venv\Scripts\Activate.ps1
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set your Hugging Face token:**
    ```bash
    export HF_TOKEN=your_hugging_face_token_here
    ```

5.  **Run the application:**
    ```bash
    python app.py
    ```
    The application will be available at `http://127.0.0.1:7860`.

## 🤖 MLOps Automation

This project demonstrates automated MLOps practices:

1.  **Continuous Deployment:** The `.github/workflows/test-and-sync.yml` workflow automatically pushes all changes from the `main` branch of this repository to the connected Hugging Face Space.
2.  **Secrets Management:** The Hugging Face write token is securely stored as a secret (`HF_TOKEN`) in the GitHub repository settings, enabling secure authentication for the sync process.

## 📊 Key Findings & trade-offs

This project serves as a practical exploration of the trade-offs between different model deployment strategies:

| Aspect | Local Execution | Remote API |
| :--- | :--- | :--- |
| **Latency** | **Fast (~1-2s)**. No network call. | **Slower (~5-10s)**. Network latency + API queue time. |
| **Cost** | **$0** operational cost after download. | **Potential cost** at scale; subject to API pricing tiers. |
| **Reliability** | **High**. No external dependencies. | **Variable**. Depends on API uptime and rate limits. |
| **Scalability** | **Limited** by host hardware (CPU). | **High**. Leverages Hugging Face's infrastructure. |
| **Ease of Setup** | **Simple**. `pip install` and run. | **Complex**. Requires API knowledge, authentication, and handling HTTP errors. |
| **Model Power** | **Limited** to smaller, efficient models. | **High**. Access to very large, state-of-the-art models. |

## 👥 Authors

- [Your Name/Team Name](https://github.com/your-profile)

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

**Note:** This project was created for educational purposes as part of the MLOps course at WPI.

---

## ☁️ Case Study 4: Cloud Deployment

This application has been refactored for cloud deployment on GCP Cloud Run, Azure Container Apps, and AWS ECS. The app now focuses solely on the API-based product (positive thought generation).

### Key Changes for Cloud Deployment

1. **Removed Local Model:** All local model dependencies (transformers, torch) have been removed to reduce container size and startup time.
2. **Simplified Dependencies:** Only `gradio` and `huggingface-hub` are required.
3. **Port Configuration:** The app reads the `PORT` environment variable (defaults to 7860) for cloud platform compatibility.
4. **Streamlined Dockerfile:** Minimal Docker image optimized for cloud deployment.

### Local Docker Testing

**Build:**
```bash
docker build -t mood-app-api:latest .
```

**Run:**
```bash
docker run --rm \
  -e HF_TOKEN=$HF_TOKEN \
  -p 7860:7860 \
  --name mood-app-api \
  mood-app-api:latest
```

**Access:** `http://localhost:7860`

### Cloud Platform Deployment

#### GCP Cloud Run

**Prerequisites:**
- GCP account with billing enabled (Free Tier is fine)
- `gcloud` CLI installed and initialized
- Project ID ready

**Step 1: Set up GCP Environment**

```bash
# Initialize gcloud (if not done already)
gcloud init

# Enable required APIs
gcloud services enable artifactregistry.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

**Step 2: Create Artifact Registry Repository**

```bash
# Replace [REGION] with your preferred region (e.g., us-central1)
# Replace [REPOSITORY_NAME] with your repository name (e.g., mood-app-repo)
gcloud artifacts repositories create [REPOSITORY_NAME] \
  --repository-format=docker \
  --location=[REGION] \
  --description="Docker repository for mood app API"

# Configure Docker authentication
gcloud auth configure-docker [REGION]-docker.pkg.dev
```

**Step 3: Build and Push Docker Image**

```bash
# Get your PROJECT_ID
PROJECT_ID=$(gcloud config get-value project)

# Build and push in one step (recommended)
gcloud builds submit --tag [REGION]-docker.pkg.dev/$PROJECT_ID/[REPOSITORY_NAME]/mood-app-api:latest

# OR build locally, tag, and push:
# docker build -t mood-app-api:latest .
# docker tag mood-app-api:latest [REGION]-docker.pkg.dev/$PROJECT_ID/[REPOSITORY_NAME]/mood-app-api:latest
# docker push [REGION]-docker.pkg.dev/$PROJECT_ID/[REPOSITORY_NAME]/mood-app-api:latest
```

**Step 4: Deploy to Cloud Run**

```bash
gcloud run deploy mood-app-api \
  --image [REGION]-docker.pkg.dev/$PROJECT_ID/[REPOSITORY_NAME]/mood-app-api:latest \
  --platform managed \
  --region [REGION] \
  --allow-unauthenticated \
  --set-env-vars HF_TOKEN=your_huggingface_token_here \
  --port 8080
```

**Note:** Cloud Run automatically sets `PORT=8080` environment variable, which our app reads.

**Step 5: Get Your Service URL**

After deployment, Cloud Run will display your service URL. You can also get it with:

```bash
gcloud run services describe mood-app-api --region [REGION] --format 'value(status.url)'
```

**Step 6: Set up Cost Monitoring**

1. Go to [GCP Console → Billing → Budgets & Alerts](https://console.cloud.google.com/billing/budgets)
2. Click **CREATE BUDGET**
3. **Scope:** Select your project
4. **Budget amount:** Set to `$1.00 USD` (to get alerts immediately if charges occur)
5. **Thresholds:** Set alerts at 10%, 50%, 90%, 100% of budget
6. **Recipients:** Add your email address
7. Click **CREATE**

This will alert you if you exceed Free Tier limits (2 million requests/month for Cloud Run).

#### Azure Container Apps

1. **Build and push to Azure Container Registry:**
   ```bash
   az acr build --registry REGISTRY_NAME --image mood-app-api:latest .
   ```

2. **Deploy to Container Apps:**
   ```bash
   az containerapp create \
     --name mood-app-api \
     --resource-group RESOURCE_GROUP \
     --image REGISTRY_NAME.azurecr.io/mood-app-api:latest \
     --target-port 80 \
     --ingress external \
     --env-vars HF_TOKEN=your_token_here
   ```
   Note: Azure Container Apps typically use port 80.

#### AWS ECS (Fargate)

1. **Build and push to Amazon ECR:**
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
   docker build -t mood-app-api .
   docker tag mood-app-api:latest ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/mood-app-api:latest
   docker push ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/mood-app-api:latest
   ```

2. **Create ECS Task Definition** (via AWS Console or CLI) with:
   - Container port: 7860 (or set PORT env var)
   - Environment variable: `HF_TOKEN`

3. **Deploy to ECS Fargate service** using the task definition.

### Environment Variables

- `HF_TOKEN` (required): Your Hugging Face API token
- `PORT` (optional): Port to bind the application (defaults to 7860)

### Notes

- The application automatically reads the `PORT` environment variable set by cloud platforms.
- All cloud platforms will provide a public URL after deployment.
- Make sure to set up cost monitoring/budgets on each platform to stay within free tier limits.