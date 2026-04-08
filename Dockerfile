FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only requirements first (better caching)
COPY requirements.txt .

# Create virtual environment
RUN python -m venv /opt/venv

# Activate venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip and install deps
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy rest of the code
COPY . .

# Expose port
EXPOSE 7860

# Run app
CMD ["python", "inference.py"]
