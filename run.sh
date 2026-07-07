#!/bin/bash

# --- 1. CLEANUP TRAP ---
# This ensures that when you press Ctrl+C, all child processes are killed
cleanup() {
    echo -e "\n\nStopping all processes (Backend & Frontend)..."
    fuser -k 5000/tcp 2>/dev/null
    pkill -f vite
    exit
}

# Trap SIGINT (Ctrl+C) and SIGTERM
trap cleanup SIGINT SIGTERM

# --- 2. BACKEND SETUP ---
echo "--- Setting up Backend ---"
cd backend || { echo "Error: 'backend' directory not found."; exit 1; }

# Virtual Env check
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate and Install
source venv/bin/activate
#download dependencies
# if [ -f "requirements.txt" ]; then
#     echo "Installing backend dependencies..."
#     pip install -r requirements.txt
# fi

# Start Flask in the background
echo "Starting Flask on port 5000..."
flask run --port=5000 &
BACKEND_PID=$!
cd ..

# --- 3. FRONTEND SETUP ---
echo "--- Setting up Frontend ---"
cd frontend || { echo "Error: 'frontend' directory not found."; exit 1; }

# Install modules if not present
# if [ ! -d "node_modules" ]; then
#     echo "Installing frontend dependencies..."
#     npm install
# fi

# Start Frontend
echo "Starting Frontend..."
npm run dev

# --- 4. WAIT FOR EXIT ---
# This keeps the script running until you press Ctrl+C
wait