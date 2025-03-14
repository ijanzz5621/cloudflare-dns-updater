# Use a lightweight Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the Python script into the container
COPY update_dns.py .

# Install required dependencies
RUN pip install requests

# Set default environment variables (can be overridden)
ENV UPDATE_INTERVAL=300
ENV API_TOKEN=""
ENV ZONE_ID=""
ENV RECORD_NAME=""

# Run the script
CMD ["python", "update_dns.py"]
