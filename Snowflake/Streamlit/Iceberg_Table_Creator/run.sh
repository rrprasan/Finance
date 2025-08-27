#!/bin/bash

# 🧊 Iceberg Table Creator - Run Script
# Quick launcher for the Streamlit app

echo "🧊 Starting Iceberg Table Creator..."
echo "=================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run ./install.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if main file exists
if [ ! -f "Iceberg_Table_Creator.py" ]; then
    echo "❌ Iceberg_Table_Creator.py not found!"
    echo "Make sure you're in the correct directory"
    exit 1
fi

# Start the app
echo "🚀 Launching app at http://localhost:8501"
echo "Press Ctrl+C to stop the app"
echo ""

streamlit run Iceberg_Table_Creator.py
