"""
Chatbot Service for AI-powered financial advice.
"""
import logging
from typing import Dict
import google.generativeai as genai
from config import Config

logger = logging.getLogger(__name__)

# Configure Gemini API
genai.configure(api_key=Config.GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-pro")

class ChatbotService:
    """Service class for handling chatbot operations."""
    
    @staticmethod
    def is_finance_related(question: str) -> bool:
        """
        Check if a question is finance-related.
        
        Args:
            question: The user's question
            
        Returns:
            True if the question is finance-related, False otherwise
        """
        question_lower = question.lower()
        return any(keyword in question_lower for keyword in Config.FINANCE_KEY_WORDS)
    
    @staticmethod
    def get_response(question: str) -> str:
        """
        Generate a response for the user's question using Gemini AI.
        
        Args:
            question: The user's question
            
        Returns:
            Formatted response from the AI model
        """
        if not ChatbotService.is_finance_related(question):
            return "This chatbot only answers finance-related questions. Please ask about stocks, investments, budgeting, or other financial topics."
        
        try:
            finance_prompt = f"""You are a helpful financial advisor. Provide a clear, informative, and practical answer to this finance-related question:

Question: {question}

Please format your response with:
- Clear explanations
- Practical tips when applicable
- Bullet points for easy reading
- Professional but friendly tone"""

            response = model.generate_content(finance_prompt)
            
            # Format response for better readability
            formatted_response = response.text.replace("**", "").replace("*", "• ")
            return formatted_response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I apologize, but I'm having trouble processing your request right now. Please try again later." 