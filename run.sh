#!/usr/bin/bash

# Exit on error
set -e

# check python version is 3.10 or higher
if [[ $(python -V | cut -d " " -f 2 | cut -d "." -f 1) -lt 3 ]] || [[ $(python -V | cut -d " " -f 2 | cut -d "." -f 2) -lt 10 ]]; then
    echo "Python version must be 3.10 or higher"
    exit 1
fi

# check node version is 16 or higher
if [[ $(node -v | cut -d "v" -f 2 | cut -d "." -f 1) -lt 16 ]]; then
    echo "Node version must be 16 or higher"
    exit 1
fi

# create virtual environment
# cd src
# python -m venv venv
# source venv/bin/activate
# pip install rich fastapi pydantic watchfiles

cd socket-server
npm install

cd ../ui
npm install

# Run the server
cd ../src
uvicorn app:app --reload &

# Run the socket server in a new terminal
gnome-terminal -- bash -c "cd ../socket-server; node server.js; exec bash" &

# Run the UI on a separate terminal
gnome-terminal -- bash -c "cd ../ui; npm start; exec bash"

