"""
Setup script for Mental Health ChatBot
"""

import os
import sys
import subprocess
import platform

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def download_spacy_model():
    """Download required spaCy model"""
    print("🧠 Downloading spaCy English model...")
    try:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        print("✅ spaCy model downloaded successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error downloading spaCy model: {e}")
        print("You may need to install it manually: python -m spacy download en_core_web_sm")
        return False

def create_env_file():
    """Create .env file with default configuration"""
    env_content = """# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-this-in-production

# Database Configuration
DATABASE_URL=sqlite:///mental_health_chatbot.db
SQLALCHEMY_DATABASE_URI=sqlite:///mental_health_chatbot.db

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Email Configuration (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production
JWT_ACCESS_TOKEN_EXPIRES=3600

# Pinecone Configuration (Optional)
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_ENVIRONMENT=your-pinecone-environment
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Created .env file with default configuration")
        print("⚠️  Please update the .env file with your actual API keys!")
    else:
        print("ℹ️  .env file already exists")

def main():
    """Main setup function"""
    print("🚀 Setting up Mental Health ChatBot...")
    print(f"🖥️  Platform: {platform.system()} {platform.release()}")
    print(f"🐍 Python: {sys.version}")
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed during requirements installation")
        return False
    
    # Download spaCy model
    download_spacy_model()
    
    # Create .env file
    create_env_file()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update the .env file with your API keys")
    print("2. Run the application:")
    if platform.system() == "Windows":
        print("   - Double-click run.bat, or")
        print("   - Run: python run.py")
    else:
        print("   - Run: python run.py")
    print("3. Open your browser and go to http://localhost:5000")
    
    return True

if __name__ == "__main__":
    main()