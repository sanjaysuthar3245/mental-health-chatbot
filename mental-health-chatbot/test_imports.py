"""
Test script to check for import issues
"""

def test_imports():
    """Test all critical imports"""
    print("🧪 Testing imports...")
    
    try:
        print("  ✓ Testing Flask imports...")
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        from flask_login import LoginManager
        from flask_jwt_extended import JWTManager
        from flask_migrate import Migrate
        from flask_cors import CORS
        from flask_mail import Mail
        print("  ✅ Flask imports successful")
    except ImportError as e:
        print(f"  ❌ Flask import error: {e}")
        return False
    
    try:
        print("  ✓ Testing database imports...")
        from src.db.database import db
        from src.db.models import User, ChatSession, Message, MoodEntry
        print("  ✅ Database imports successful")
    except ImportError as e:
        print(f"  ❌ Database import error: {e}")
        return False
    
    try:
        print("  ✓ Testing web app imports...")
        from src.web.app import create_app
        from src.web.config import config
        print("  ✅ Web app imports successful")
    except ImportError as e:
        print(f"  ❌ Web app import error: {e}")
        return False
    
    try:
        print("  ✓ Testing NLP imports...")
        from src.nlp.gpt_handler import GPTHandler
        from src.nlp.sentiment_analysis import SentimentAnalyzer
        print("  ✅ NLP imports successful")
    except ImportError as e:
        print(f"  ❌ NLP import error: {e}")
        return False
    
    try:
        print("  ✓ Testing ML imports...")
        from src.ml.models.recommendation_engine import RecommendationEngine
        from src.ml.models.mental_health_classifier import MentalHealthClassifier
        print("  ✅ ML imports successful")
    except ImportError as e:
        print(f"  ❌ ML import error: {e}")
        return False
    
    print("🎉 All imports successful!")
    return True

if __name__ == "__main__":
    success = test_imports()
    if not success:
        print("\n❌ Some imports failed. Please check the error messages above.")
        print("💡 Try running: python setup.py")
    else:
        print("\n✅ All imports are working correctly!")
        print("🚀 You can now run the application with: python run.py")

