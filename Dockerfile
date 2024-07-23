# Use Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Flask and other required Python packages
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose the port that Flask runs on
EXPOSE 5000

# Command to run the Flask application
CMD ["python3", "app.py"]
