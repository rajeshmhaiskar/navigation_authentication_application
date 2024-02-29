# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Clone the repository from GitHub
RUN apt-get update && apt-get install -y git \
    && git clone https://github.com/rajeshmhaiskar/navigation_authentication_application.git

# Change the working directory to the cloned repository
WORKDIR /app/navigation_authentication_application

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /home/Genesys/navigation_authentication_application/requirments/requirments.txt

# Expose port 5000 to the outside world
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
