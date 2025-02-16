# Use official Python base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the server code
COPY . .

# Expose Flask port
EXPOSE 5000

# Start Flask server
CMD ["python", "server.py"]
