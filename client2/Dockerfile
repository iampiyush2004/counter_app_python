# Use official Python base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir websocket-client

# Copy client code
COPY client2.py .

# Environment variable for server URL
ENV SERVER_URL="http://server:5000"

# Start client
CMD ["python", "client2.py"]
