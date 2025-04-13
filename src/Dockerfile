# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable
ENV FLASK_APP=main.py

# Start both the Flask server and the HTTP server
CMD flask run --host=0.0.0.0 --port=5000
