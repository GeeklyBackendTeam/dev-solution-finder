# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
  build-essential \
  libpq-dev \
  && apt-get clean

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file
COPY requirements.txt /code/

# Install Python dependencies
RUN pip install --upgrade pip \
  && pip install -r requirements.txt

# Copy the application code into the container
COPY . /code/

# Expose the port FastAPI is running on
EXPOSE 8000

# Command to run the FastAPI app using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
