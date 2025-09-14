# 🧠 Mental Health ChatBot

A comprehensive AI-powered mental health support chatbot with mood tracking, personalized recommendations, and crisis detection.

## 🚀 Quick Start

### For Windows Users:

1. **Run the setup script:**
   ```cmd
   python setup.py
   ```

2. **Start the application:**
   - Double-click `run.bat`, or
   - Run: `python run.py`, or
   - Run: `powershell -ExecutionPolicy Bypass -File run.ps1`

### For Linux/Mac Users:

1. **Run the setup script:**
   ```bash
   python3 setup.py
   ```

2. **Start the application:**
   ```bash
   python3 run.py
   ```

## 🔧 Troubleshooting

### Problem 1: `/usr/bin/env` not recognized (Windows)
**Solution:** Use the provided Windows-compatible files:
- `run.bat` - Double-click to run
- `run.ps1` - PowerShell script
- `run.py` - Updated Python script

### Problem 2: Import Errors
**Solution:** Run the test script to identify issues:
```cmd
python test_imports.py
```

If imports fail, install missing dependencies:
```cmd
pip install -r requirements.txt
```

### Problem 3: Missing spaCy Model
**Solution:** Download the English model:
```cmd
python -m spacy download en_core_web_sm
```

### Problem 4: Database Issues
**Solution:** The app will create the database automatically on first run. If you encounter issues:
1. Delete `mental_health_chatbot.db` (if it exists)
2. Restart the application

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🛠️ Manual Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd mental-health-chatbot
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy model:**
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Configure environment:**
   - Copy `.env.example` to `.env`
   - Update API keys in `.env` file

6. **Run the application:**
   ```bash
   python run.py
   ```

## 🌐 Access the Application

Once running, open your browser and go to:
- **Main Application:** http://localhost:5000
- **Chat Interface:** http://localhost:5000/chat
- **Mood Tracking:** http://localhost:5000/mood-tracking
- **Dashboard:** http://localhost:5000/dashboard

## 🔑 Environment Variables

Create a `.env` file with the following variables:

```env
# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-this-in-production

# Database Configuration
DATABASE_URL=sqlite:///mental_health_chatbot.db
SQLALCHEMY_DATABASE_URI=sqlite:///mental_health_chatbot.db

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production
JWT_ACCESS_TOKEN_EXPIRES=3600

# Email Configuration (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Pinecone Configuration (Optional)
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_ENVIRONMENT=your-pinecone-environment
```

## 🎯 Features

- **AI-Powered Chat:** Intelligent conversations with empathy and context awareness
- **Mood Tracking:** Comprehensive mood monitoring with analytics and insights
- **Mental Health Assessments:** PHQ-9, GAD-7, and custom assessment tools
- **Personalized Recommendations:** AI-driven suggestions based on user data
- **Crisis Detection:** Immediate crisis detection and appropriate resources
- **Data Privacy:** Secure, anonymous chat options and data protection
- **Mobile Responsive:** Works perfectly on all devices

## 🏗️ Project Structure

```
mental-health-chatbot/
├── src/
│   ├── web/                 # Flask web application
│   │   ├── routes/         # API routes and blueprints
│   │   ├── templates/      # HTML templates
│   │   ├── static/         # CSS, JS, and static files
│   │   └── config.py       # Configuration settings
│   ├── db/                 # Database models and configuration
│   ├── nlp/                # Natural Language Processing
│   └── ml/                 # Machine Learning models
├── run.py                  # Main application entry point
├── run.bat                 # Windows batch file
├── run.ps1                 # PowerShell script
├── setup.py                # Setup and installation script
├── test_imports.py         # Import testing script
└── requirements.txt        # Python dependencies
```

## 🐛 Common Issues

### Issue: "Module not found" errors
**Solution:** Ensure you're in the correct directory and have activated your virtual environment.

### Issue: "Permission denied" on Windows
**Solution:** Run PowerShell as Administrator or use Command Prompt.

### Issue: Database connection errors
**Solution:** Check your database configuration in the `.env` file.

### Issue: OpenAI API errors
**Solution:** Ensure you have a valid OpenAI API key in your `.env` file.

## 📞 Support

If you encounter any issues:

1. Run `python test_imports.py` to check for import problems
2. Check the console output for specific error messages
3. Ensure all dependencies are installed: `pip install -r requirements.txt`
4. Verify your `.env` file configuration

## 🎉 Success!

Once everything is working, you should see:
```
🚀 Starting Mental Health ChatBot on port 5000
🌐 Environment: Development
🔗 Access the application at: http://localhost:5000
```

Open your browser and enjoy your new mental health chatbot! 🧠💙