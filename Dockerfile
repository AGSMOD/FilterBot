# Use the official Python image as the base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip3 install -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /app/

# Define environment variable for Python to run in unbuffered mode
ENV PYTHONUNBUFFERED 1

# Command to run on container start
CMD ["python3", "bot.py"]
