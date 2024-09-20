#!/bin/bash
# Test script for Dockerfile

# Step 1: Build the Docker image

docker build -t test-sandbox .

# Step 2: Run the Docker container

docker run -d -p 8080:80 --name test-container test-sandbox

# Step 3: Verify the container is running

if [ $(docker ps -q -f name=test-container) ]; then
    echo "Container is running"
else
    echo "Container failed to start"
    exit 1
fi

# Step 4: Test the application

response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080)
if [ $response -eq 200 ]; then
    echo "Application is running successfully"
else
    echo "Application test failed with status code $response"
    exit 1
fi

# Clean up

docker stop test-container

docker rm test-container

docker rmi test-sandbox

exit 0
