# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt /app/

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . /app/

# Expose the port that the Flask app will run on
EXPOSE 8000

# Set the environment variable for Flask to run in production mode
ENV FLASK_ENV=production

# Command to run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
