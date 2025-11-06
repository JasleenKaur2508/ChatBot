@echo off
REM NLP Chatbot Runner Script for Windows

echo 🤖 Setting up NLP Chatbot...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo ✅ Python found

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 🔧 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Upgrade pip
echo ⬆️  Upgrading pip...
pip install --upgrade pip

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Check if .env file exists and has API key
findstr "your-api-key-here" .env >nul 2>&1
if %errorlevel% equ 0 (
    echo ⚠️  Please update your OpenAI API key in the .env file
    echo    Get your API key from: https://platform.openai.com/api-keys
    echo    Then add it to .env like: OPENAI_API_KEY=sk-...
    pause
)

REM Run the chatbot
echo 🚀 Starting the chatbot...
streamlit run app.py

pause