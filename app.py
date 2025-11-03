import gradio as gr
from transformers import pipeline
from huggingface_hub import InferenceClient
import time
import os
import traceback
from prometheus_client import start_http_server, Counter, Summary, Gauge

# --- Token Check --- #
HF_TOKEN = os.getenv("HF_TOKEN")
print("🔑 HF_TOKEN available?", "Yes ✅" if HF_TOKEN else "No ❌")
if not HF_TOKEN:
    raise ValueError("HF_TOKEN not set. Please set it in your environment.")

# --- Configuration --- #
LOCAL_MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"
API_MODEL_NAME = "HuggingFaceTB/SmolLM3-3B"

# --- Prometheus Metrics --- #
REQUESTS_LOCAL_TOTAL = Counter(
    "requests_local_total", "Total local sentiment requests received"
)
REQUESTS_API_TOTAL = Counter(
    "requests_api_total", "Total API generation requests received"
)
ERRORS_LOCAL_TOTAL = Counter(
    "errors_local_total", "Total errors during local sentiment analysis"
)
ERRORS_API_TOTAL = Counter(
    "errors_api_total", "Total errors during API generation"
)
LOCAL_LATENCY_SECONDS = Summary(
    "local_inference_latency_seconds", "Local model inference latency in seconds"
)
API_LATENCY_SECONDS = Summary(
    "api_generation_latency_seconds", "API generation latency in seconds"
)
MODEL_LOADED_GAUGE = Gauge(
    "local_model_loaded", "Whether the local model is loaded successfully (1 yes, 0 no)"
)

# --- Local Model Setup --- #
print("🔄 Loading the local sentiment model... This might take a minute.")
try:
    local_sentiment_pipeline = pipeline("sentiment-analysis", model=LOCAL_MODEL_NAME)
    print("✅ Local model loaded successfully!")
    MODEL_LOADED_GAUGE.set(1)
except Exception as e:
    print(f"❌ Failed to load local model: {e}")
    local_sentiment_pipeline = None
    MODEL_LOADED_GAUGE.set(0)

def analyze_sentiment(text):
    REQUESTS_LOCAL_TOTAL.inc()
    if not text.strip():
        return "Please enter some text to analyze."
    if local_sentiment_pipeline is None:
        return "Error: Local model failed to load. Check the logs."
    try:
        start_time = time.time()
        result = local_sentiment_pipeline(text)[0]
        end_time = time.time()
        latency = end_time - start_time
        LOCAL_LATENCY_SECONDS.observe(latency)
        response_time = round(latency, 2)
        return f"Label: {result['label']}\nConfidence: {round(result['score']*100, 2)}%\n(Processed locally in {response_time}s)"
    except Exception as e:
        traceback.print_exc()
        ERRORS_LOCAL_TOTAL.inc()
        return f"❌ An error occurred during analysis:\n{str(e)}"

# --- API Client Setup --- #
api_client = InferenceClient(
    provider="hf-inference",
    api_key=HF_TOKEN
)

def generate_positive_thought():
    REQUESTS_API_TOTAL.inc()
    user_prompt = "Generate a short positive and motivational message."
    try:
        start_time = time.time()

        completion = api_client.chat.completions.create(
            model=API_MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a friendly assistant that ONLY returns a short, positive, "
                        "motivational message. You may think internally, but always wrap your "
                        "internal reasoning in <think>...</think> tags. The user only sees the message "
                        "outside these tags."
                    )
                },
                {"role": "user", "content": user_prompt}
            ]
        )
        end_time = time.time()
        latency = end_time - start_time
        API_LATENCY_SECONDS.observe(latency)
        response_time = round(latency, 2)

        full_text = completion.choices[0].message["content"].strip()

        # Extract only text after </think> and clean up formatting
        if "</think>" in full_text:
            final_message = full_text.split("</think>")[-1].strip()
        else:
            final_message = full_text

        # Clean up any remaining formatting artifacts
        final_message = final_message.replace("</code>", "").strip()
        
        # Remove surrounding quotes if present
        if final_message.startswith('"') and final_message.endswith('"'):
            final_message = final_message[1:-1].strip()

        return f"{final_message}\n\n(Generated via {API_MODEL_NAME} in {response_time}s)"

    except Exception as e:
        traceback.print_exc()
        ERRORS_API_TOTAL.inc()
        return f"❌ API Call Failed:\n{type(e).__name__}: {str(e)}"

# --- Gradio Interface --- #
with gr.Blocks(title="Dual-Mode Mood App", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🌟 Dual-Mode Mood App
    **Compare local vs. remote AI model execution.**
    """)
    
    with gr.Tab("🔍 Analyze Sentiment (Local Model)"):
        gr.Markdown("This tab uses a small model (**DistilBERT - 66M parameters**) running **locally** on CPU.")
        with gr.Row():
            with gr.Column():
                input_text = gr.Textbox(label="How are you feeling?", placeholder="Type a sentence here...", lines=3)
                analyze_btn = gr.Button("Analyze Sentiment", variant="primary")
            with gr.Column():
                output_sentiment = gr.Textbox(label="Analysis Result", interactive=False, lines=5)
        examples = gr.Examples(
            examples=["I am so happy today!", "This is the worst day ever.", "I feel okay, I guess."],
            inputs=input_text
        )
        analyze_btn.click(fn=analyze_sentiment, inputs=input_text, outputs=output_sentiment)

    with gr.Tab("💡 Generate Positive Thought (API Model)"):
        gr.Markdown(f"This tab uses **{API_MODEL_NAME}**, called **remotely** via Hugging Face's free Inference API.")
        with gr.Row():
            with gr.Column():
                gr.Markdown("Click the button to generate an uplifting message using a cloud-based model.")
                gen_btn = gr.Button("Generate Positivity!", variant="primary")
            with gr.Column():
                output_text = gr.Textbox(label="Generated Message", interactive=False, lines=5)
        gen_btn.click(fn=generate_positive_thought, inputs=None, outputs=output_text)

    gr.Markdown("---")
    gr.Markdown(f"""
    **MLOps Case Study Demo** |  
    **Local Model:** {LOCAL_MODEL_NAME} |  
    **API Model:** {API_MODEL_NAME}
    """)

# Launch the app
if __name__ == "__main__":
    # Start Prometheus Python client metrics on port 8000
    start_http_server(8000)
    # Bind Gradio to 0.0.0.0 so it is reachable from outside the container
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
