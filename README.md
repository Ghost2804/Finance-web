# Finance Hub - Advanced Financial Health & Smart Savings Platform

A comprehensive financial platform that addresses critical issues in the Indian banking sector and personal finance management. This project provides advanced banking sector analysis, AI-powered budget planning, and personalized financial recommendations.

## 🎯 **Unique Value Proposition**

### **Topic 1: Banking Sector Health Analysis**
- **Bank Performance Monitoring**: Real-time analysis of Indian banking sector health
- **Early Warning Indicators**: Detect potential banking stress and financial instability
- **NPL & Capital Adequacy Tracking**: Monitor non-performing loans and capital adequacy ratios
- **Individual Bank Health Scores**: Comprehensive health assessment for major Indian banks

### **Topic 2: AI-Powered Smart Budget Planning**
- **Personalized Budget Structuring**: AI creates optimal budget plans based on income, expenses, and goals
- **Financial Health Scoring**: Get your personal financial health score with actionable recommendations
- **Savings Challenge System**: Gamified savings challenges (52-week, no-spend, round-up)
- **Smart Recommendations**: AI-powered financial advice and goal tracking

## 🚀 **Advanced Features**

- 🏦 **Bank Health Analysis**: Comprehensive banking sector performance monitoring
- 🤖 **AI Budget Planner**: Intelligent budget structuring with personalized recommendations
- 📊 **Real-time Stock Data**: Live stock prices for US and Indian markets
- 💬 **AI Financial Advisor**: Powered by Google Gemini for expert financial guidance
- 📈 **Financial Health Scoring**: Personal financial wellness assessment
- 🏆 **Savings Challenges**: Gamified approach to building savings habits
- ⚠️ **Early Warning System**: Banking sector stress indicators
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **AI**: Google Gemini API
- **Data**: Yahoo Finance API (yfinance)
- **Styling**: Custom CSS with modern design

## Project Structure

```
Finance_pro/
├── main.py                    # Main Flask application
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
├── env.example               # Environment variables template
├── services/                 # Business logic services
│   ├── __init__.py
│   ├── stock_service.py      # Stock market data service
│   ├── chatbot_service.py    # AI chatbot service
│   ├── bank_analysis.py      # Banking sector analysis
│   └── budget_planner.py     # AI budget planning service
├── templates/                # HTML templates
│   ├── home.html
│   ├── chat.html
│   ├── bank_analysis.html    # Banking sector analysis page
│   ├── smart_budget.html     # AI budget planner page
│   ├── finance.html
│   ├── budget.html
│   ├── stocknews.html
│   ├── 404.html
│   └── 500.html
└── static/                   # Static assets
    ├── css/                 # Stylesheets
    └── js/                  # JavaScript files
        └── chat.js          # Chat functionality
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Google Gemini API key

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Finance_pro
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp env.example .env
   
   # Edit .env with your actual values
   # SECRET_KEY=your_super_secret_key_here
   # Google_API=your_google_gemini_api_key_here
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

6. **Access the application**
   Open your browser and go to `http://localhost:5000`

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
SECRET_KEY=your_super_secret_key_here
FLASK_ENV=development
Google_API=your_google_gemini_api_key_here
```

## API Endpoints

### Core Pages
- `GET /` - Home page
- `GET /chatbot` - AI Financial Advisor interface
- `GET /finance` - Finance education page
- `GET /budget` - Basic budgeting tools page

### Advanced Features
- `GET /bank-analysis` - Banking sector health analysis
- `GET /smart-budget` - AI-powered budget planning interface
- `GET /stocknews` - Real-time stock data dashboard

### API Endpoints
- `POST /chat` - AI chatbot API endpoint
- `GET /chat-history` - Get chat history
- `GET /api/bank/<bank_name>` - Get specific bank analysis data
- `POST /api/create-budget` - Create personalized budget plan
- `GET /api/savings-tips/<profile>` - Get personalized savings tips

## Code Quality Improvements

This project has been refactored to follow best practices:

### ✅ **Security Improvements**
- Centralized configuration management
- Proper environment variable handling
- Input validation and sanitization
- Error handling for API calls

### ✅ **Code Organization**
- Separation of concerns (services, config, main app)
- Type hints for better code documentation
- Proper logging implementation
- Modular JavaScript with ES6 classes

### ✅ **Error Handling**
- Comprehensive exception handling
- User-friendly error pages (404, 500)
- Graceful degradation for API failures
- Proper HTTP status codes

### ✅ **Code Style**
- PEP 8 compliance
- Consistent naming conventions
- Docstrings for all functions
- Clean code principles

## Development

### Running in Development Mode
```bash
export FLASK_ENV=development
python main.py
```

### Code Formatting
```bash
# Format Python code
black .

# Check for style issues
flake8 .

# Type checking
mypy .
```

### Testing
```bash
pytest
```

## Deployment

### Using setup.sh (Linux/macOS)
```bash
chmod +x setup.sh
./setup.sh
```

### Manual Deployment
1. Set `FLASK_ENV=production` in your environment
2. Use a production WSGI server like Gunicorn
3. Set up proper logging and monitoring
4. Configure your web server (nginx/Apache)



