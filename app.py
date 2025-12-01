import gradio as gr
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
API_MODEL_NAME = "HuggingFaceTB/SmolLM3-3B"

# Get port from environment variable (for cloud platforms) or default to 7860
PORT = int(os.getenv("PORT", 7860))

# --- API Client Setup --- #
api_client = InferenceClient(
    provider="hf-inference",
    api_key=HF_TOKEN
)

def generate_positive_thought():
    """Generate a positive motivational message using Hugging Face Inference API."""
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
with gr.Blocks(title="API-Based Mood App") as demo:
    gr.Markdown("""
    # 💡 API-Based Mood App
    **Generate positive motivational messages using cloud-based AI models.**
    
    This application uses **Hugging Face Inference API** to generate uplifting messages.
    """)
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Generate Positive Thought")
            gr.Markdown("Click the button below to generate an uplifting message using a cloud-based model.")
            gen_btn = gr.Button("Generate Positivity! ✨", variant="primary", size="lg")
        with gr.Column():
            output_text = gr.Textbox(
                label="Generated Message", 
                interactive=False, 
                lines=8,
                placeholder="Your positive message will appear here..."
            )
    
    gen_btn.click(fn=generate_positive_thought, inputs=None, outputs=output_text)

    gr.Markdown("---")
    gr.Markdown(f"""
    **MLOps Case Study 4 - Cloud Deployment** |  
    **Model:** {API_MODEL_NAME} |  
    **Deployment:** API-based via Hugging Face Inference API
    """)

# Launch the app
if __name__ == "__main__":
    # Bind to 0.0.0.0 to be accessible from outside container
    # Use PORT environment variable for cloud platforms (GCP, Azure, AWS)
    demo.launch(server_name="0.0.0.0", server_port=PORT, share=False)
