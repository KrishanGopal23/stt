# Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install ffmpeg, which is a system dependency for Whisper
RUN apt-get update && apt-get install -y ffmpeg

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 10000

# Define the command to run your app using uvicorn
# This will be executed when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
