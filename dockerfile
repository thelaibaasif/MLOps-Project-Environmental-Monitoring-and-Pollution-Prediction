# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Run the Flask app
CMD ["python", "api.py"]
