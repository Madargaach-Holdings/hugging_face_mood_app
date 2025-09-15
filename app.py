import gradio as gr
from transformers import pipeline
from huggingface_hub import InferenceClient
import time
import os
import traceback

# --- Token Check --- #
HF_TOKEN = os.getenv("HF_TOKEN")
print("🔑 HF_TOKEN available?", "Yes ✅" if HF_TOKEN else "No ❌")
if not HF_TOKEN:
    raise ValueError("HF_TOKEN not set. Please set it in your environment.")

# --- Configuration --- #
LOCAL_MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"
API_MODEL_NAME = "HuggingFaceTB/SmolLM3-3B"

# --- Local Model Setup --- #
print("🔄 Loading the local sentiment model... This might take a minute.")
try:
    local_sentiment_pipeline = pipeline("sentiment-analysis", model=LOCAL_MODEL_NAME)
    print("✅ Local model loaded successfully!")
except Exception as e:
    print(f"❌ Failed to load local model: {e}")
    local_sentiment_pipeline = None

def analyze_sentiment(text):
    if not text.strip():
        return "Please enter some text to analyze."
    if local_sentiment_pipeline is None:
        return "Error: Local model failed to load. Check the logs."
    try:
        start_time = time.time()
        result = local_sentiment_pipeline(text)[0]
        end_time = time.time()
        response_time = round(end_time - start_time, 2)
        return f"Label: {result['label']}\nConfidence: {round(result['score']*100, 2)}%\n(Processed locally in {response_time}s)"
    except Exception as e:
        traceback.print_exc()
        return f"❌ An error occurred during analysis:\n{str(e)}"

# --- API Client Setup --- #
api_client = InferenceClient(
    provider="hf-inference",
    api_key=HF_TOKEN
)

def generate_positive_thought():
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
        response_time = round(end_time - start_time, 2)

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
    demo.launch(share=False)
