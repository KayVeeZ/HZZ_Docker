# Base on the latest Python image
FROM python:latest

# Set the working directory in the container
WORKDIR /app

# Copy the Python program and requirements file into the container
COPY get_d.py requirements.txt /app/

# Install dependent libraries
RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run our program
CMD ["python", "get_d.py"]
