# Use Debian Bullseye (stable) - known to work
FROM python:3.11-slim-bullseye

# Install ALL OpenCV/YOLO dependencies
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

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app
COPY . .

# Run Streamlit
CMD ["streamlit", "run", "app.py"]