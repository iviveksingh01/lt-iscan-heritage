FROM python:3.11-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive

# Install ALL OpenCV dependencies - DO NOT COMMENT THESE!
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    libegl1-mesa \
    libxcb-xinerama0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py"]