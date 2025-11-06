"""
Test script to verify the chatbot environment setup.
"""

import sys
import os

def test_imports():
    """Test if all required packages can be imported."""
    try:
        import streamlit
        print("✅ Streamlit import successful")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import google.generativeai
        print("✅ Google Generative AI import successful")
    except ImportError as e:
        print(f"❌ Google Generative AI import failed: {e}")
        return False
        
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv import successful")
    except ImportError as e:
        print(f"❌ python-dotenv import failed: {e}")
        return False
    
    return True

def test_env_file():
    """Test if .env file exists and has API key."""
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            content = f.read()
            if "your-api-key-here" in content:
                print("⚠️  .env file exists but still has placeholder API key")
                return False
            elif "GEMINI_API_KEY=" in content:
                print("✅ .env file has API key")
                return True
            else:
                print("⚠️  .env file exists but doesn't contain API key")
                return False
    else:
        print("❌ .env file not found")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing chatbot environment setup...\n")
    
    imports_ok = test_imports()
    print()
    
    env_ok = test_env_file()
    print()
    
    if imports_ok and env_ok:
        print("🎉 All tests passed! Your chatbot is ready to run.")
        print("   Use 'streamlit run app.py' to start the application.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)