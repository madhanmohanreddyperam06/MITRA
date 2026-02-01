#!/bin/bash

# Smart College Helpdesk Bot Startup Script

echo "Starting Smart College Helpdesk Bot..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Download spaCy model
echo "Downloading spaCy model..."
python -m spacy download en_core_web_sm

# Start backend API in background
echo "Starting backend API..."
cd backend
python main.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 5

# Start Streamlit frontend
echo "Starting Streamlit frontend..."
cd streamlit_app
streamlit run main.py

# Cleanup: Kill backend when Streamlit stops
kill $BACKEND_PID
