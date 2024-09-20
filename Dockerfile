# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy only the necessary files
COPY requirements.txt .
COPY app.py .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Add a non-root user
RUN useradd -m myuser
USER myuser

# Copy the rest of the application files
COPY . .

# Make port 80 available to the world outside this container
EXPOSE 80

# Add a health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:80/ || exit 1

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]