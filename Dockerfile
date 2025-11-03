FROM python:3.10-slim

WORKDIR /opt/app
COPY . .
RUN pip install --no-cache-dir -r /opt/app/requirements.txt

# Install packages for Node Exporter (Deliverable 2a)
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get upgrade -yq ca-certificates \
    && apt-get install -yq --no-install-recommends prometheus-node-exporter \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 7860
EXPOSE 8000
EXPOSE 9100

# Set the Gradio server name to 0.0.0.0 for container accessibility
ENV GRADIO_SERVER_NAME=0.0.0.0

# Start Node Exporter in background and your Python app
CMD bash -c "prometheus-node-exporter --web.listen-address=':9100' & python /opt/app/app.py"


