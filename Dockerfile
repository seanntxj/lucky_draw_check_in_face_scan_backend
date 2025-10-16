# Use official Python base image
FROM python:3.11

# Install system dependencies
RUN apt-get update && apt-get install -y libgl1-mesa-dev

# Set working directory and environment variables
ENV HOME=/app
WORKDIR /app
# Copy and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories with proper permissions
RUN mkdir -p /app/.deepface/weights && \
    chmod -R 777 /app/.deepface
# Optional: Create a non-root user for better security
# RUN useradd -m appuser && chown -R appuser /app
# USER appuser

# Expose the application port
EXPOSE 9001

# Start the application using Uvicorn
CMD ["uvicorn", "app.src.face_api:app", "--host", "0.0.0.0", "--port", "9001"]