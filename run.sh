#!/bin/bash

# NLP Chatbot Runner Script

echo "🤖 Setting up NLP Chatbot..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists and has API key
if [ -f ".env" ]; then
    if grep -q "your-api-key-here" .env; then
        echo "⚠️  Please update your OpenAI API key in the .env file"
        echo "   Get your API key from: https://platform.openai.com/api-keys"
        echo "   Then add it to .env like: OPENAI_API_KEY=sk-..."
        read -p "Press enter to continue (you can edit .env in another terminal)..."
    fi
else
    echo "⚠️  .env file not found. Creating one..."
    echo "OPENAI_API_KEY=your-api-key-here" > .env
    echo "Please update your OpenAI API key in the .env file"
fi

# Run the chatbot
echo "🚀 Starting the chatbot..."
streamlit run app.py