#!/bin/bash

# Check if we are on Linux or Windows
if [[ "$OSTYPE" == "linux-gnu" ]]; then
    # Linux
    echo "Installing packages on Linux..."
    sudo apt-get update
    sudo apt-get install -y python3-pip
    pip3 install tkinter  requests 
elif [[ "$OSTYPE" == "msys" ]]; then
    # Windows (using MinGW)
    echo "Installing packages on Windows..."
    python -m pip install --upgrade pip
    pip install tk requests 
else
    echo "Unsupported operating system"
    exit 1
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install it before proceeding."
    exit 1
fi


# Install requests using pip
pip install requests 

# Check if installation was successful
echo "Installation complete."
