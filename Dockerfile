FROM python:3.10-slim

# Prevents Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Install only minimal OS dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy only requirements first to reduce layer size if code changes
COPY requirements.txt .

# Upgrade pip and install Python dependencies with cache off to reduce space
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose Flask or Streamlit port if needed (adjust as necessary)
EXPOSE 5000

# Default command
CMD ["python", "app.py"]
