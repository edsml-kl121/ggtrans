# Use an official Python base image from the Docker Hub
FROM python:3.11-slim

# Install browsers
RUN apt-get update && apt-get install build-essential -y
# Install utilities
RUN apt-get install -y curl wget git

# Declare working directory
WORKDIR /Users

COPY . .

# Install any necessary packages specified in requirements.txt.
RUN pip install -r requirement.txt

EXPOSE 8071

ENTRYPOINT ["python", "main.py", "--server.port=8071", "--server.address=0.0.0.0"]