#!/bin/bash

# Navigate to backend folder
cd backend

# Initialize DB if not exists
python db_init.py

# Start the Flask app
python app.py
