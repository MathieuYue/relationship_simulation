#!/usr/bin/env python3
"""
Simple startup script for the Agent Chat Simulator web app
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if LAMBDA_API_KEY is set
if not os.getenv("LAMBDA_API_KEY"):
    print("❌ Error: LAMBDA_API_KEY not found in environment variables!")
    print("Please create a .env file with your Lambda AI API key:")
    print("LAMBDA_API_KEY=your_api_key_here")
    sys.exit(1)

# Check if required files exist
required_files = [
    "relationship_agent.py",
    "environment.py", 
    "parser_utils.py",
    "prompt_utils.py",
    "json_utils.py",
    "scenarios/vacation.json"
]

for file_path in required_files:
    if not os.path.exists(file_path):
        print(f"❌ Error: Required file '{file_path}' not found!")
        sys.exit(1)

print("🚀 Starting Agent Chat Simulator...")
print("✅ Environment check passed")
print("🌐 Web app will be available at: http://localhost:5000")
print("📝 Make sure you have installed dependencies: pip install -r requirements.txt")
print()

# Import and run the Flask app
try:
    from app import app
    app.run(debug=True, port=5000, host='0.0.0.0')
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install dependencies: pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error starting app: {e}")
    sys.exit(1)