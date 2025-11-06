#!/usr/bin/env python3
"""
Script to run the NLP Chatbot application.
This script handles dependency checking and provides helpful error messages.
"""

import sys
import subprocess
import os

def check_and_install_dependencies():
    """Check if required dependencies are installed, install if missing."""
    required_packages = [
        "streamlit",
        "openai<1.0.0",
        "python-dotenv"
    ]
    
    for package in required_packages:
        try:
            __import__(package.split('<')[0])  # Handle version specifiers
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():
    """Main function to run the chatbot application."""
    try:
        # Check and install dependencies
        check_and_install_dependencies()
        
        # Import required modules after ensuring they're installed
        import streamlit as st
        
        # Run the Streamlit app
        os.system("streamlit run app.py")
        
    except Exception as e:
        print(f"Error running the chatbot: {e}")
        print("Please make sure you have Python 3.8+ installed and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()