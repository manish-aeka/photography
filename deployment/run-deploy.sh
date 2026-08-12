#!/bin/bash
# Quick run script for deployment app

if [ ! -d ".venv" ]; then
    echo "Virtual environment not found!"
    echo "Please run ./setup.sh first"
    exit 1
fi

source .venv/bin/activate
python deploy-app.py
