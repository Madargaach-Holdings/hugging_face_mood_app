FROM python:3.10-slim

WORKDIR /opt/app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose port (will be overridden by cloud platforms via PORT env var)
EXPOSE 7860

# Set the Gradio server name to 0.0.0.0 for container accessibility
ENV GRADIO_SERVER_NAME=0.0.0.0

# Run the application
CMD ["python", "app.py"]
