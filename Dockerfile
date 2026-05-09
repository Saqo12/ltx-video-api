FROM nvidia/cuda:12.1.0-cudnn8-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install Python, git, and dependencies
RUN apt-get update && apt-get install -y \
    python3.11 python3-pip git curl libgl1 libglib2.0-0 wget \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 \
    && pip install diffusers transformers accelerate scipy flask \
    && pip install httpx python-dotenv

# Clone LTX-Video
RUN git clone https://github.com/Lightricks/LTX-Video.git . 2>/dev/null || true

# Copy app
COPY app.py .
COPY requirements.txt .

EXPOSE 7860

ENV HOST=0.0.0.0
ENV PORT=7860

CMD ["python3", "-u", "app.py"]