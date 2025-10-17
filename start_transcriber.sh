#!/bin/bash

echo "Starting Gemini Video Transcriber..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check if dependencies are installed
if ! python3 -c "import google.generativeai" &> /dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements-transcriber.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
fi

# Start the application
python3 video_transcriber.py

if [ $? -ne 0 ]; then
    echo ""
    echo "Application exited with an error"
    read -p "Press Enter to continue..."
fi
