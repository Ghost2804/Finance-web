"""
Main Flask application for the Finance Hub.
"""
import logging
from flask import Flask, render_template, request, jsonify, session
from config import Config
from services import StockService, ChatbotService
from services.bank_analysis import BankHealthAnalyzer
from services.budget_planner import AIBudgetPlanner

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Application factory pattern for creating Flask app."""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Register routes
    register_routes(app)
    
    return app


def register_routes(app):
    """Register all application routes."""
    
    # Initialize services
    bank_analyzer = BankHealthAnalyzer()
    budget_planner = AIBudgetPlanner()
    
    @app.route("/")
    def home():
        """Home page route."""
        return render_template("home.html")
    
    @app.route("/finance")
    def finance():
        """Finance page route."""
        return render_template('finance.html')
    
    @app.route("/budget")
    def budget():
        """Budget page route."""
        return render_template('budget.html')
    
    @app.route("/stocknews")
    def stocknews():
        """Stock news page with real-time stock data."""
        try:
            stock_data = StockService.get_stock_data()
            return render_template("stocknews.html", stock_data=stock_data)
        except Exception as e:
            logger.error(f"Error fetching stock data: {e}")
            return render_template("stocknews.html", stock_data={}, error="Unable to fetch stock data")
    
    @app.route("/bank-analysis")
    def bank_analysis():
        """Bank health analysis page."""
        try:
            sector_overview = bank_analyzer.get_banking_sector_overview()
            warning_indicators = bank_analyzer.get_early_warning_indicators()
            return render_template("bank_analysis.html", 
                                 sector_overview=sector_overview,
                                 warning_indicators=warning_indicators)
        except Exception as e:
            logger.error(f"Error in bank analysis: {e}")
            return render_template("bank_analysis.html", 
                                 sector_overview={"error": "Unable to fetch data"},
                                 warning_indicators={"error": "Unable to fetch data"})
    
    @app.route("/api/bank/<bank_name>")
    def get_bank_data(bank_name):
        """API endpoint to get specific bank data."""
        try:
            bank_data = bank_analyzer.get_bank_stock_data(bank_name)
            health_analysis = bank_analyzer.calculate_bank_health_score(bank_data)
            return jsonify({
                "bank_data": bank_data,
                "health_analysis": health_analysis
            })
        except Exception as e:
            logger.error(f"Error fetching bank data for {bank_name}: {e}")
            return jsonify({"error": "Failed to fetch bank data"}), 500
    
    @app.route("/smart-budget")
    def smart_budget():
        """AI-powered budget planning page."""
        return render_template("smart_budget.html")
    
    @app.route("/api/create-budget", methods=["POST"])
    def create_budget():
        """API endpoint to create personalized budget plan."""
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            
            budget_plan = budget_planner.create_personalized_budget(data)
            return jsonify(budget_plan)
        except Exception as e:
            logger.error(f"Error creating budget plan: {e}")
            return jsonify({"error": "Failed to create budget plan"}), 500
    
    @app.route("/api/savings-tips/<profile>")
    def get_savings_tips(profile):
        """API endpoint to get personalized savings tips."""
        try:
            tips = budget_planner.get_savings_tips(profile)
            return jsonify({"tips": tips})
        except Exception as e:
            logger.error(f"Error fetching savings tips: {e}")
            return jsonify({"error": "Failed to fetch tips"}), 500
    
    @app.route("/chatbot")
    def chatbot():
        """Chatbot page route."""
        if 'chat_history' not in session:
            session['chat_history'] = []
        return render_template("chat.html")
    
    @app.route("/chat-history")
    def chat_history():
        """Get chat history from session."""
        return jsonify({"history": session.get("chat_history", [])})
    
    @app.route("/chat", methods=["POST"])
    def chat_response():
        """Handle chat requests and generate responses."""
        try:
            data = request.get_json()
            
            if not data or "message" not in data:
                return jsonify({"error": "Invalid request format"}), 400
            
            user_message = data["message"].strip()
            
            if not user_message:
                return jsonify({"error": "Message cannot be empty"}), 400
            
            # Generate bot response
            bot_reply = ChatbotService.get_response(user_message)
            
            # Store in session
            if 'chat_history' not in session:
                session['chat_history'] = []
            
            session['chat_history'].append({
                "user": user_message, 
                "bot": bot_reply
            })
            session.modified = True
            
            return jsonify({
                "response": bot_reply, 
                "history": session['chat_history']
            })
            
        except Exception as e:
            logger.error(f"Error in chat response: {e}")
            return jsonify({"error": "Internal server error"}), 500
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return render_template("404.html"), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        logger.error(f"Internal server error: {error}")
        return render_template("500.html"), 500


if __name__ == "__main__":
    app = create_app()
    app.run(debug=Config.DEBUG, host="0.0.0.0", port=5000) 