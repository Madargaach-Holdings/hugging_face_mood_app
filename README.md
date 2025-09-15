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

A Gradio-based web application demonstrating key MLOps concepts by comparing local vs. remote AI model deployment strategies. Built for DS/CS553 – Machine Learning Development and Operations (MLOps) Case Study 1.

**Live Demo on Hugging Face Spaces:**  
👉 [https://huggingface.co/spaces/upandit/mood-app-api-version](https://huggingface.co/spaces/upandit/mood-app-api-version) 👈

## 🚀 Features

- **Dual-Tab Interface:** Compare two deployment paradigms in a single application.
- **🔍 Analyze Sentiment (Local Model):** Runs a lightweight DistilBERT model **locally** on the CPU for fast, private sentiment analysis.
- **💡 Generate Positive Thought (API Model):** Leverages a powerful remote model via Hugging Face's **Inference API** for generative tasks.
- **Built-in Performance Metrics:** Response times are displayed, providing immediate data for comparing local vs. API latency.
- **Automated MLOps Pipeline:** GitHub Actions automatically syncs code to Hugging Face Spaces on every commit.

## 🛠️ Technical Architecture

### Models Used
| Task | Model | Framework | Deployment |
| :--- | :--- | :--- | :--- |
| Sentiment Analysis | [`distilbert-base-uncased-finetuned-sst-2-english`](https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english) | Transformers | Local CPU |
| Text Generation | [`HuggingFaceTB/SmolLM3-3B`](https://huggingface.co/HuggingFaceTB/SmolLM3-3B) | Hugging Face Inference API | Remote API |

### Tech Stack
- **Frontend:** [Gradio](https://www.gradio.app/)
- **ML Framework:** [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- **API Client:** [Hugging Face Hub](https://huggingface.co/docs/huggingface_hub)
- **CI/CD & Sync:** [GitHub Actions](https://github.com/features/actions)
- **Hosting:** [Hugging Face Spaces](https://huggingface.co/spaces)

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

4.  **Run the application:**
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