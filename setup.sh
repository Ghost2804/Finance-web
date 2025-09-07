

#!/bin/bash

echo "Starting Finance Hub Project Deployment..."

# Exit on any error
set -e

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "Please do not run this script as root"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Error: .env file not found!"
    echo "Please copy env.example to .env and configure your environment variables"
    exit 1
fi

echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

echo "Installing necessary system dependencies..."
sudo apt install -y python3 python3-pip python3-venv

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Checking for environment variables..."
if [ -z "$SECRET_KEY" ]; then
    echo "Warning: SECRET_KEY not set in environment"
fi

if [ -z "$Google_API" ]; then
    echo "Warning: Google_API not set in environment"
fi

echo "Starting Finance Hub project..."
echo "Application will be available at http://localhost:5000"

# Use the new main.py instead of app.py
export FLASK_APP=main.py
export FLASK_ENV=production

# Start the application in the background
nohup python main.py > app.log 2>&1 &

echo "Deployment completed successfully!"
echo "Check app.log for application logs"
