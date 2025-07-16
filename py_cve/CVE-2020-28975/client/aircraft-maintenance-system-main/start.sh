#!/bin/bash
echo "Setting up the environment..."

# Install dependencies
pip install -r requirements.txt

# Start the backend server
uvicorn backend.backend:app --reload