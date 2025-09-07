"""
AI Budget Planner Service
Provides intelligent budget structuring and financial planning recommendations.
"""
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import json
import random

logger = logging.getLogger(__name__)

class AIBudgetPlanner:
    """AI-powered budget planning and financial recommendation service."""
    
    # Budget Categories with recommended percentages
    BUDGET_CATEGORIES = {
        "essential_expenses": {
            "name": "Essential Expenses",
            "max_percentage": 50,
            "subcategories": {
                "housing": {"name": "Housing/Rent", "max_percentage": 30},
                "utilities": {"name": "Utilities", "max_percentage": 10},
                "groceries": {"name": "Groceries", "max_percentage": 15},
                "transportation": {"name": "Transportation", "max_percentage": 10},
                "healthcare": {"name": "Healthcare", "max_percentage": 5}
            }
        },
        "financial_goals": {
            "name": "Financial Goals",
            "max_percentage": 20,
            "subcategories": {
                "emergency_fund": {"name": "Emergency Fund", "max_percentage": 10},
                "savings": {"name": "Savings", "max_percentage": 10},
                "investments": {"name": "Investments", "max_percentage": 10}
            }
        },
        "discretionary": {
            "name": "Discretionary Spending",
            "max_percentage": 30,
            "subcategories": {
                "entertainment": {"name": "Entertainment", "max_percentage": 10},
                "dining_out": {"name": "Dining Out", "max_percentage": 8},
                "shopping": {"name": "Shopping", "max_percentage": 7},
                "hobbies": {"name": "Hobbies", "max_percentage": 5}
            }
        }
    }
    
    # Savings Challenges
    SAVINGS_CHALLENGES = {
        "52_week": {
            "name": "52-Week Savings Challenge",
            "description": "Save increasing amounts each week",
            "total_savings": 1378,
            "duration": "52 weeks"
        },
        "no_spend": {
            "name": "No-Spend Challenge",
            "description": "Avoid non-essential spending for a month",
            "potential_savings": "20-30% of discretionary budget",
            "duration": "30 days"
        },
        "envelope": {
            "name": "Envelope Budgeting Challenge",
            "description": "Use cash envelopes for better spending control",
            "potential_savings": "15-25% of total budget",
            "duration": "Ongoing"
        },
        "round_up": {
            "name": "Round-Up Challenge",
            "description": "Round up all purchases to nearest 10 and save the difference",
            "potential_savings": "5-10% of spending",
            "duration": "Ongoing"
        }
    }
    
    def __init__(self):
        self.user_profiles = {}
        self.budget_plans = {}
    
    def create_personalized_budget(self, user_data: Dict) -> Dict:
        """
        Create a personalized budget plan based on user input.
        
        Args:
            user_data: Dictionary containing user financial information
            
        Returns:
            Dictionary containing personalized budget plan
        """
        try:
            monthly_income = user_data.get("monthly_income", 0)
            current_expenses = user_data.get("current_expenses", {})
            financial_goals = user_data.get("financial_goals", [])
            risk_tolerance = user_data.get("risk_tolerance", "moderate")
            age = user_data.get("age", 30)
            
            if monthly_income <= 0:
                return {"error": "Invalid monthly income"}
            
            # Calculate recommended budget allocation
            budget_plan = self._calculate_budget_allocation(
                monthly_income, current_expenses, financial_goals, risk_tolerance, age
            )
            
            # Generate personalized recommendations
            recommendations = self._generate_recommendations(
                monthly_income, current_expenses, financial_goals, risk_tolerance, age
            )
            
            # Create savings challenges
            savings_challenges = self._create_savings_challenges(monthly_income, financial_goals)
            
            return {
                "budget_plan": budget_plan,
                "recommendations": recommendations,
                "savings_challenges": savings_challenges,
                "financial_health_score": self._calculate_financial_health_score(user_data),
                "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            logger.error(f"Error creating budget plan: {e}")
            return {"error": "Failed to create budget plan"}
    
    def _calculate_budget_allocation(self, income: float, expenses: Dict, 
                                   goals: List, risk_tolerance: str, age: int) -> Dict:
        """Calculate optimal budget allocation based on user profile."""
        
        budget_allocation = {}
        total_allocated = 0
        
        # Essential Expenses (50-60% of income)
        essential_percentage = 55 if risk_tolerance == "conservative" else 50
        essential_amount = (income * essential_percentage) / 100
        
        budget_allocation["essential_expenses"] = {
            "amount": round(essential_amount, 2),
            "percentage": essential_percentage,
            "breakdown": {
                "housing": round(essential_amount * 0.55, 2),  # 55% of essential
                "utilities": round(essential_amount * 0.18, 2),  # 18% of essential
                "groceries": round(essential_amount * 0.27, 2),  # 27% of essential
            }
        }
        total_allocated += essential_amount
        
        # Financial Goals (20-30% of income)
        goals_percentage = 25 if age < 30 else 20
        goals_amount = (income * goals_percentage) / 100
        
        budget_allocation["financial_goals"] = {
            "amount": round(goals_amount, 2),
            "percentage": goals_percentage,
            "breakdown": {
                "emergency_fund": round(goals_amount * 0.4, 2),  # 40% of goals
                "savings": round(goals_amount * 0.3, 2),  # 30% of goals
                "investments": round(goals_amount * 0.3, 2),  # 30% of goals
            }
        }
        total_allocated += goals_amount
        
        # Discretionary Spending (remaining amount)
        discretionary_amount = income - total_allocated
        discretionary_percentage = (discretionary_amount / income) * 100
        
        budget_allocation["discretionary"] = {
            "amount": round(discretionary_amount, 2),
            "percentage": round(discretionary_percentage, 2),
            "breakdown": {
                "entertainment": round(discretionary_amount * 0.33, 2),
                "dining_out": round(discretionary_amount * 0.27, 2),
                "shopping": round(discretionary_amount * 0.23, 2),
                "hobbies": round(discretionary_amount * 0.17, 2),
            }
        }
        
        return budget_allocation
    
    def _generate_recommendations(self, income: float, expenses: Dict, 
                                goals: List, risk_tolerance: str, age: int) -> List[Dict]:
        """Generate personalized financial recommendations."""
        
        recommendations = []
        
        # Emergency Fund Recommendation
        emergency_fund_target = income * 6  # 6 months of income
        recommendations.append({
            "category": "Emergency Fund",
            "priority": "High",
            "recommendation": f"Build an emergency fund of ₹{emergency_fund_target:,.0f} (6 months of income)",
            "action_items": [
                "Set up automatic monthly transfers",
                "Keep in high-yield savings account",
                "Only use for true emergencies"
            ]
        })
        
        # Debt Management
        if expenses.get("debt_payments", 0) > income * 0.2:
            recommendations.append({
                "category": "Debt Management",
                "priority": "High",
                "recommendation": "Focus on paying off high-interest debt first",
                "action_items": [
                    "List all debts by interest rate",
                    "Pay minimum on all, extra on highest rate",
                    "Consider debt consolidation if beneficial"
                ]
            })
        
        # Investment Recommendations
        if age < 40:
            recommendations.append({
                "category": "Investments",
                "priority": "Medium",
                "recommendation": "Start investing early for compound growth",
                "action_items": [
                    "Consider SIP in mutual funds",
                    "Diversify across asset classes",
                    "Start with index funds for beginners"
                ]
            })
        
        # Savings Rate Optimization
        current_savings_rate = (expenses.get("savings", 0) / income) * 100
        if current_savings_rate < 20:
            recommendations.append({
                "category": "Savings",
                "priority": "Medium",
                "recommendation": f"Increase savings rate from {current_savings_rate:.1f}% to 20%",
                "action_items": [
                    "Review discretionary spending",
                    "Look for ways to reduce fixed expenses",
                    "Automate savings transfers"
                ]
            })
        
        # Insurance Recommendations
        recommendations.append({
            "category": "Insurance",
            "priority": "Medium",
            "recommendation": "Ensure adequate insurance coverage",
            "action_items": [
                "Health insurance: ₹5-10 lakhs coverage",
                "Term life insurance: 10x annual income",
                "Consider disability insurance"
            ]
        })
        
        return recommendations
    
    def _create_savings_challenges(self, income: float, goals: List) -> List[Dict]:
        """Create personalized savings challenges."""
        
        challenges = []
        
        # 52-Week Challenge
        challenges.append({
            "challenge_id": "52_week",
            "name": "52-Week Savings Challenge",
            "description": "Save ₹1 in week 1, ₹2 in week 2, and so on",
            "total_savings": 1378,
            "duration": "52 weeks",
            "weekly_breakdown": self._generate_52_week_breakdown(),
            "difficulty": "Easy",
            "suitable_for": "Beginners"
        })
        
        # No-Spend Challenge
        challenges.append({
            "challenge_id": "no_spend",
            "name": "30-Day No-Spend Challenge",
            "description": "Avoid non-essential spending for 30 days",
            "potential_savings": round(income * 0.25, 2),
            "duration": "30 days",
            "rules": [
                "Only spend on essential items",
                "No dining out or entertainment",
                "No impulse purchases",
                "Track all spending"
            ],
            "difficulty": "Hard",
            "suitable_for": "Advanced"
        })
        
        # Round-Up Challenge
        challenges.append({
            "challenge_id": "round_up",
            "name": "Round-Up Challenge",
            "description": "Round up all purchases to nearest ₹10 and save the difference",
            "potential_savings": round(income * 0.05, 2),
            "duration": "Ongoing",
            "how_it_works": [
                "Purchase: ₹247 → Save ₹3",
                "Purchase: ₹1,156 → Save ₹4",
                "Automate with banking apps"
            ],
            "difficulty": "Easy",
            "suitable_for": "Everyone"
        })
        
        return challenges
    
    def _generate_52_week_breakdown(self) -> List[Dict]:
        """Generate 52-week savings challenge breakdown."""
        breakdown = []
        for week in range(1, 53):
            amount = week
            breakdown.append({
                "week": week,
                "amount": amount,
                "cumulative": sum(range(1, week + 1))
            })
        return breakdown
    
    def _calculate_financial_health_score(self, user_data: Dict) -> Dict:
        """Calculate overall financial health score."""
        
        score = 0
        max_score = 100
        factors = []
        
        income = user_data.get("monthly_income", 0)
        expenses = user_data.get("current_expenses", {})
        goals = user_data.get("financial_goals", [])
        
        # Income Factor (20 points)
        if income > 50000:
            score += 20
            factors.append("✅ High income level")
        elif income > 30000:
            score += 15
            factors.append("✅ Good income level")
        elif income > 15000:
            score += 10
            factors.append("⚠️ Moderate income level")
        else:
            factors.append("❌ Low income level")
        
        # Savings Rate (25 points)
        savings = expenses.get("savings", 0)
        savings_rate = (savings / income) * 100 if income > 0 else 0
        
        if savings_rate >= 20:
            score += 25
            factors.append(f"✅ Excellent savings rate: {savings_rate:.1f}%")
        elif savings_rate >= 15:
            score += 20
            factors.append(f"✅ Good savings rate: {savings_rate:.1f}%")
        elif savings_rate >= 10:
            score += 15
            factors.append(f"⚠️ Moderate savings rate: {savings_rate:.1f}%")
        else:
            factors.append(f"❌ Low savings rate: {savings_rate:.1f}%")
        
        # Debt Management (20 points)
        debt_payments = expenses.get("debt_payments", 0)
        debt_ratio = (debt_payments / income) * 100 if income > 0 else 0
        
        if debt_ratio <= 10:
            score += 20
            factors.append(f"✅ Excellent debt management: {debt_ratio:.1f}%")
        elif debt_ratio <= 20:
            score += 15
            factors.append(f"✅ Good debt management: {debt_ratio:.1f}%")
        elif debt_ratio <= 30:
            score += 10
            factors.append(f"⚠️ Moderate debt load: {debt_ratio:.1f}%")
        else:
            factors.append(f"❌ High debt load: {debt_ratio:.1f}%")
        
        # Financial Goals (20 points)
        if len(goals) >= 3:
            score += 20
            factors.append("✅ Multiple financial goals set")
        elif len(goals) >= 1:
            score += 15
            factors.append("✅ Some financial goals set")
        else:
            factors.append("❌ No financial goals identified")
        
        # Emergency Fund (15 points)
        emergency_fund = expenses.get("emergency_fund", 0)
        emergency_months = emergency_fund / income if income > 0 else 0
        
        if emergency_months >= 6:
            score += 15
            factors.append(f"✅ Strong emergency fund: {emergency_months:.1f} months")
        elif emergency_months >= 3:
            score += 10
            factors.append(f"✅ Adequate emergency fund: {emergency_months:.1f} months")
        else:
            factors.append(f"❌ Insufficient emergency fund: {emergency_months:.1f} months")
        
        # Determine overall status
        if score >= 80:
            status = "Excellent"
            status_color = "green"
        elif score >= 60:
            status = "Good"
            status_color = "blue"
        elif score >= 40:
            status = "Fair"
            status_color = "orange"
        else:
            status = "Poor"
            status_color = "red"
        
        return {
            "score": score,
            "max_score": max_score,
            "status": status,
            "status_color": status_color,
            "factors": factors,
            "recommendation": self._get_health_recommendation(score)
        }
    
    def _get_health_recommendation(self, score: int) -> str:
        """Get recommendation based on financial health score."""
        if score >= 80:
            return "Excellent financial health! Focus on wealth building and advanced strategies."
        elif score >= 60:
            return "Good financial health. Continue building emergency fund and increasing savings."
        elif score >= 40:
            return "Fair financial health. Prioritize debt reduction and emergency fund building."
        else:
            return "Poor financial health. Focus on basic budgeting and debt management first."
    
    def get_savings_tips(self, user_profile: str = "general") -> List[Dict]:
        """Get personalized savings tips based on user profile."""
        
        tips = {
            "beginner": [
                {
                    "title": "Start Small",
                    "tip": "Begin with saving just ₹100 per day. It adds up to ₹36,500 per year!",
                    "difficulty": "Easy",
                    "impact": "High"
                },
                {
                    "title": "Use the 50/30/20 Rule",
                    "tip": "50% for needs, 30% for wants, 20% for savings",
                    "difficulty": "Easy",
                    "impact": "High"
                },
                {
                    "title": "Track Every Rupee",
                    "tip": "Use apps to track all expenses. Awareness leads to better decisions.",
                    "difficulty": "Easy",
                    "impact": "Medium"
                }
            ],
            "intermediate": [
                {
                    "title": "Automate Savings",
                    "tip": "Set up automatic transfers to savings account on payday",
                    "difficulty": "Easy",
                    "impact": "High"
                },
                {
                    "title": "Cut Subscriptions",
                    "tip": "Review and cancel unused subscriptions. Save ₹500-2000 monthly.",
                    "difficulty": "Medium",
                    "impact": "Medium"
                },
                {
                    "title": "Meal Planning",
                    "tip": "Plan meals weekly to reduce food waste and dining out costs",
                    "difficulty": "Medium",
                    "impact": "High"
                }
            ],
            "advanced": [
                {
                    "title": "Side Hustle",
                    "tip": "Start a side business or freelance work for extra income",
                    "difficulty": "Hard",
                    "impact": "Very High"
                },
                {
                    "title": "Invest Wisely",
                    "tip": "Start SIP in mutual funds for long-term wealth building",
                    "difficulty": "Medium",
                    "impact": "Very High"
                },
                {
                    "title": "Negotiate Bills",
                    "tip": "Negotiate with service providers for better rates",
                    "difficulty": "Hard",
                    "impact": "Medium"
                }
            ]
        }
        
        return tips.get(user_profile, tips["general"]) 