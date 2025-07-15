# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# No need to run the development server, Gunicorn is used in the Docker Compose file
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]  # Remove this line
