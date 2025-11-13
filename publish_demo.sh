#!/bin/bash

# Streamlit Demo App Publisher
# This script builds and runs the Streamlit demo application

set -e  # Exit on error

echo "🚀 Building and starting Streamlit demo app..."

# Build and start the containers
docker-compose -f docker-compose.demo.yml up --build

# Note: To run in detached mode, use:
# docker-compose -f docker-compose.demo.yml up --build -d
