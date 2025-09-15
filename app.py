import gradio as gr
from transformers import pipeline
from huggingface_hub import InferenceClient
import time
import os

# --- Configuration --- #
# Model for the LOCAL tab (must be small enough to run on CPU)
LOCAL_MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"
# Model for the API tab (Using a powerful, supported chat model)
API_MODEL_NAME = "HuggingFaceH4/zephyr-7b-beta"

# --- Function for the LOCAL model (Tab 1) --- #
print("🔄 Loading the local sentiment model... This might take a minute.")
try:
    # This pipeline will run locally on the Space's CPU
    local_sentiment_pipeline = pipeline("sentiment-analysis", 
                                       model=LOCAL_MODEL_NAME)
    print("✅ Local model loaded successfully!")
except Exception as e:
    print(f"❌ Failed to load local model: {e}")
    # If loading fails, create a dummy function that returns an error message
    local_sentiment_pipeline = None

def analyze_sentiment(text):
    """Runs the sentiment analysis model locally on the CPU."""
    if not text.strip():
        return "Please enter some text to analyze."
    
    if local_sentiment_pipeline is None:
        return "Error: Local model failed to load. Check the logs."
    
    try:
        start_time = time.time()
        # Get the prediction from the local model
        result = local_sentiment_pipeline(text)[0]
        end_time = time.time()
        
        response_time = round(end_time - start_time, 2)
        
        # Format the result nicely
        return f"Label: {result['label']}\nConfidence: {round(result['score'] * 100, 2)}%\n(Processed locally in {response_time}s)"
    except Exception as e:
        return f"An error occurred during analysis: {str(e)}"

# --- Function for the API model (Tab 2) --- #
# Initialize the client for the API-based model.
# We are not loading the model here, just setting up a client to call Hugging Face's API.
api_client = InferenceClient(model=API_MODEL_NAME)

def generate_positive_thought():
    """Uses the Hugging Face Inference API to generate a positive message."""
    
    # Create a prompt that will guide the model to generate a positive message
    prompt = """<|system|>
You are a helpful AI assistant that generates short, positive, and motivational messages.
Your responses should be one or two sentences maximum, and designed to make someone's day better.
</s>
<|user|>
Please generate a short positive and motivational message.
</s>
<|assistant|>
"""
    
    try:
        start_time = time.time()
        
        # Call the hosted model via API with the specific prompt format for this model
        response = api_client.text_generation(
            prompt=prompt,
            max_new_tokens=75,  # Increased slightly for better responses
            do_sample=True,
            temperature=0.8,    # Slightly lower temperature for more focused responses
            stop_sequences=["</s>"]  # Stop generating when this token appears
        )
        
        end_time = time.time()
        response_time = round(end_time - start_time, 2)
        
        # Clean up the response by removing the stop sequence if it appears at the end
        cleaned_response = response.replace('</s>', '').strip()
        
        return f"{cleaned_response}\n\n(Generated via API in {response_time}s)"
    
    except Exception as e:
        return f"An error occurred calling the API: {str(e)}. The API might be busy or require authentication."

# --- Gradio Interface --- #
with gr.Blocks(title="Dual-Mode Mood App", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🌟 Dual-Mode Mood App
    **Compare local vs. remote AI model execution.**
    """)
    
    with gr.Tab("🔍 Analyze Sentiment (Local Model)"):
        gr.Markdown("This tab uses a small model (**DistilBERT**) running **locally** on this server's CPU.")
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
        gr.Markdown("This tab uses a powerful 7B parameter model (**Zephyr-7B-Beta**) called **remotely** via Hugging Face's Inference API.")
        with gr.Row():
            with gr.Column():
                gr.Markdown("Click the button to generate an uplifting message using a state-of-the-art cloud model.")
                gen_btn = gr.Button("Generate Positivity!", variant="primary")
            with gr.Column():
                output_text = gr.Textbox(label="Generated Message", interactive=False, lines=5)
        gen_btn.click(fn=generate_positive_thought, inputs=None, outputs=output_text)

    gr.Markdown("---")
    gr.Markdown("""
    **MLOps Case Study Demo** | 
    **Local Model:** {LOCAL_MODEL_NAME} | 
    **API Model:** {API_MODEL_NAME}
    """.format(LOCAL_MODEL_NAME=LOCAL_MODEL_NAME, API_MODEL_NAME=API_MODEL_NAME))

# Launch the app
if __name__ == "__main__":
    demo.launch(share=False)