# Use the official Python image as the base image
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install terrasect
RUN apt-get update && apt-get install -y tesseract-ocr poppler-utils

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the entire application directory into the container
COPY . .

# Expose the port the application will run on
EXPOSE 8000

# Define the command to run your Flask app
CMD ["python", "app.py"]