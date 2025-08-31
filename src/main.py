from flask import Flask, render_template, request, url_for, jsonify
import pandas as pd
from flask_cors import CORS
import json
from datetime import datetime, timedelta
import math

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

class ComprehensiveFinancialPlanner:
    def __init__(self):
        self.expense_categories = {
            'housing': {
                'name': 'Housing',
                'icon': '🏠',
                'description': 'Rent, mortgage, utilities, insurance',
                'flexible': True,
                'priority': 'high'
            },
            'transportation': {
                'name': 'Transportation',
                'icon': '🚗',
                'description': 'Car payment, gas, insurance, public transit',
                'flexible': True,
                'priority': 'high'
            },
            'food': {
                'name': 'Food',
                'icon': '🍕',
                'description': 'Groceries, eating out, coffee',
                'flexible': True,
                'priority': 'high'
            },
            'debt': {
                'name': 'Debt Payments',
                'icon': '💳',
                'description': 'Credit cards, loans, student debt',
                'flexible': False,
                'priority': 'high'
            },
            'healthcare': {
                'name': 'Healthcare',
                'icon': '🏥',
                'description': 'Insurance, medical, dental, prescriptions',
                'flexible': True,
                'priority': 'high'
            },
            'utilities': {
                'name': 'Utilities',
                'icon': '⚡',
                'description': 'Electric, water, gas, internet, phone',
                'flexible': True,
                'priority': 'medium'
            },
            'entertainment': {
                'name': 'Entertainment',
                'icon': '🎉',
                'description': 'Movies, streaming, hobbies, shopping',
                'flexible': True,
                'priority': 'low'
            },
            'savings': {
                'name': 'Savings',
                'icon': '💰',
                'description': 'Emergency fund, retirement, investments',
                'flexible': True,
                'priority': 'high'
            },
            'business': {
                'name': 'Business Expenses',
                'icon': '💼',
                'description': 'Equipment, software, marketing, taxes',
                'flexible': True,
                'priority': 'medium'
            },
            'education': {
                'name': 'Education',
                'icon': '📚',
                'description': 'Courses, books, certifications',
                'flexible': True,
                'priority': 'medium'
            }
        }
    
    def calculate_comprehensive_plan(self, financial_data):
        """Calculate comprehensive financial plan with variable income and goals"""
        monthly_income = float(financial_data.get('monthly_income', 0))
        current_savings = float(financial_data.get('current_savings', 0))
        debts = financial_data.get('debts', [])
        expenses = financial_data.get('expenses', [])
        income_changes = financial_data.get('income_changes', [])
        goals = financial_data.get('goals', [])
        emergency_fund_target = float(financial_data.get('emergency_fund_target', monthly_income * 6))
        
        # Calculate total debt and minimum payments
        total_debt = sum(float(debt['current_balance']) for debt in debts)
        total_min_payments = sum(float(debt['minimum_payment']) for debt in debts)
        
        # Calculate current monthly expenses
        current_expenses = {}
        for expense in expenses:
            category = expense.get('category', 'other')
            if category not in current_expenses:
                current_expenses[category] = 0
            current_expenses[category] += float(expense.get('amount', 0))
        
        # Calculate total current monthly expenses
        total_current_expenses = sum(current_expenses.values())
        
        # Calculate available funds after minimum payments and current expenses
        available_funds = monthly_income - total_min_payments - total_current_expenses
        
        # Generate 12-month projection
        projection = self.generate_12_month_projection(
            monthly_income, current_savings, debts, expenses, 
            income_changes, goals, emergency_fund_target
        )
        
        # Calculate debt payoff strategies
        debt_strategies = self.calculate_debt_strategies(monthly_income, debts, available_funds)
        
        # Generate recommendations
        recommendations = self.generate_recommendations(
            monthly_income, current_savings, debts, expenses, 
            income_changes, goals, emergency_fund_target, available_funds
        )
        
        # Calculate financial health score
        health_score = self.calculate_financial_health_score(
            monthly_income, current_savings, total_debt, total_current_expenses,
            emergency_fund_target, available_funds
        )
        
        return {
            'summary': {
                'monthly_income': monthly_income,
                'current_savings': current_savings,
                'total_debt': total_debt,
                'total_min_payments': total_min_payments,
                'total_current_expenses': total_current_expenses,
                'available_funds': available_funds,
                'emergency_fund_target': emergency_fund_target,
                'financial_health_score': health_score
            },
            'projection': projection,
            'debt_strategies': debt_strategies,
            'recommendations': recommendations,
            'expense_breakdown': current_expenses
        }
    
    def generate_12_month_projection(self, monthly_income, current_savings, debts, expenses, income_changes, goals, emergency_fund_target):
        """Generate 12-month financial projection"""
        projection = []
        current_debts = [debt.copy() for debt in debts]
        current_balance = current_savings
        
        for month in range(1, 13):
            # Apply income changes
            month_income = monthly_income
            for change in income_changes:
                if change['start_month'] <= month:
                    if change['type'] == 'percentage':
                        month_income *= (1 + change['amount'] / 100)
                    elif change['type'] == 'fixed':
                        month_income += change['amount']
                    elif change['type'] == 'one_time':
                        if change['start_month'] == month:
                            month_income += change['amount']
            
            # Calculate expenses for this month
            month_expenses = sum(float(exp['amount']) for exp in expenses)
            
            # Calculate debt payments (avalanche method)
            debt_payments = self.calculate_monthly_debt_payments(current_debts, month_income, month_expenses)
            
            # Calculate savings
            month_savings = month_income - month_expenses - sum(payment['amount'] for payment in debt_payments)
            current_balance += month_savings
            
            # Update debt balances
            for i, payment in enumerate(debt_payments):
                if i < len(current_debts):
                    current_debts[i]['current_balance'] = max(0, float(current_debts[i]['current_balance']) - payment['principal'])
            
            # Check goal progress
            goal_progress = self.check_goal_progress(goals, current_balance, month, current_debts)
            
            projection.append({
                'month': month,
                'income': month_income,
                'expenses': month_expenses,
                'debt_payments': debt_payments,
                'savings': month_savings,
                'current_balance': current_balance,
                'emergency_fund_ratio': current_balance / emergency_fund_target if emergency_fund_target > 0 else 0,
                'goal_progress': goal_progress,
                'total_debt_remaining': sum(float(debt['current_balance']) for debt in current_debts)
            })
        
        return projection
    
    def calculate_monthly_debt_payments(self, debts, monthly_income, monthly_expenses):
        """Calculate debt payments using avalanche method"""
        available_for_debt = monthly_income - monthly_expenses
        total_min_payments = sum(float(debt['minimum_payment']) for debt in debts)
        extra_payment = available_for_debt - total_min_payments
        
        if extra_payment < 0:
            # Can't even make minimum payments
            return [{'name': debt['name'], 'amount': min(float(debt['minimum_payment']), available_for_debt / len(debts)), 'principal': 0} for debt in debts]
        
        # Sort debts by interest rate (avalanche method)
        sorted_debts = sorted(debts, key=lambda x: float(x['interest_rate']), reverse=True)
        
        payments = []
        remaining_extra = extra_payment
        
        for debt in sorted_debts:
            min_payment = float(debt['minimum_payment'])
            current_balance = float(debt['current_balance'])
            
            # Calculate how much extra we can pay on this debt
            extra_on_this_debt = min(remaining_extra, current_balance - min_payment)
            total_payment = min_payment + extra_on_this_debt
            
            # Calculate principal payment (simplified)
            interest = current_balance * float(debt['interest_rate']) / 100 / 12
            principal = total_payment - interest
            
            payments.append({
                'name': debt['name'],
                'amount': total_payment,
                'principal': principal,
                'interest': interest
            })
            
            remaining_extra -= extra_on_this_debt
        
        return payments
    
    def check_goal_progress(self, goals, current_balance, current_month, current_debts):
        """Check progress towards financial goals"""
        progress = []
        
        for goal in goals:
            goal_type = goal.get('type', 'savings')
            target_amount = float(goal.get('target_amount', 0))
            target_month = goal.get('target_month', 12)
            
            if goal_type == 'savings':
                progress_percentage = min(100, (current_balance / target_amount) * 100) if target_amount > 0 else 0
                on_track = current_balance >= (target_amount * current_month / target_month)
            elif goal_type == 'debt_payoff':
                initial_debt = sum(float(debt.get('initial_balance', debt['current_balance'])) for debt in current_debts)
                current_debt = sum(float(debt['current_balance']) for debt in current_debts)
                progress_percentage = min(100, ((initial_debt - current_debt) / initial_debt) * 100) if initial_debt > 0 else 0
                on_track = current_debt <= (initial_debt * (1 - current_month / target_month))
            else:
                progress_percentage = 0
                on_track = False
            
            progress.append({
                'name': goal.get('name', 'Goal'),
                'type': goal_type,
                'target_amount': target_amount,
                'target_month': target_month,
                'progress_percentage': progress_percentage,
                'on_track': on_track,
                'current_value': current_balance if goal_type == 'savings' else (initial_debt - current_debt) if goal_type == 'debt_payoff' else 0
            })
        
        return progress
    
    def calculate_debt_strategies(self, monthly_income, debts, available_funds):
        """Calculate different debt payoff strategies"""
        strategies = {}
        
        # Avalanche method
        avalanche_result = self.calculate_avalanche_strategy(monthly_income, debts, available_funds)
        strategies['avalanche'] = avalanche_result
        
        # Snowball method
        snowball_result = self.calculate_snowball_strategy(monthly_income, debts, available_funds)
        strategies['snowball'] = snowball_result
        
        # Equal payment method
        equal_result = self.calculate_equal_payment_strategy(monthly_income, debts, available_funds)
        strategies['equal_payment'] = equal_result
        
        return strategies
    
    def calculate_avalanche_strategy(self, monthly_income, debts, available_funds):
        """Calculate avalanche method results"""
        sorted_debts = sorted(debts, key=lambda x: float(x['interest_rate']), reverse=True)
        return self.simulate_debt_payoff(sorted_debts, monthly_income, available_funds, 'avalanche')
    
    def calculate_snowball_strategy(self, monthly_income, debts, available_funds):
        """Calculate snowball method results"""
        sorted_debts = sorted(debts, key=lambda x: float(x['current_balance']))
        return self.simulate_debt_payoff(sorted_debts, monthly_income, available_funds, 'snowball')
    
    def calculate_equal_payment_strategy(self, monthly_income, debts, available_funds):
        """Calculate equal payment method results"""
        return self.simulate_debt_payoff(debts, monthly_income, available_funds, 'equal')
    
    def simulate_debt_payoff(self, debts, monthly_income, available_funds, strategy):
        """Simulate debt payoff for a given strategy"""
        current_debts = [debt.copy() for debt in debts]
        total_interest = 0
        months_to_payoff = 0
        
        while any(float(debt['current_balance']) > 0 for debt in current_debts) and months_to_payoff < 120:
            months_to_payoff += 1
            monthly_interest = 0
            
            # Calculate minimum payments
            total_min_payments = sum(float(debt['minimum_payment']) for debt in current_debts)
            extra_funds = available_funds
            
            for debt in current_debts:
                if float(debt['current_balance']) > 0:
                    # Calculate interest
                    interest = float(debt['current_balance']) * float(debt['interest_rate']) / 100 / 12
                    monthly_interest += interest
                    
                    # Calculate payment
                    min_payment = float(debt['minimum_payment'])
                    if strategy == 'equal' and extra_funds > 0:
                        extra_payment = extra_funds / len([d for d in current_debts if float(d['current_balance']) > 0])
                        payment = min_payment + extra_payment
                    else:
                        payment = min_payment
                    
                    # Update balance
                    new_balance = float(debt['current_balance']) + interest - payment
                    debt['current_balance'] = max(0, new_balance)
            
            total_interest += monthly_interest
        
        return {
            'months_to_payoff': months_to_payoff,
            'total_interest': round(total_interest, 2),
            'strategy': strategy
        }
    
    def generate_recommendations(self, monthly_income, current_savings, debts, expenses, income_changes, goals, emergency_fund_target, available_funds):
        """Generate personalized financial recommendations"""
        recommendations = []
        
        # Emergency fund recommendations
        emergency_fund_ratio = current_savings / emergency_fund_target if emergency_fund_target > 0 else 0
        if emergency_fund_ratio < 0.5:
            recommendations.append({
                'type': 'emergency_fund',
                'priority': 'high',
                'title': 'Build Emergency Fund',
                'description': 'Your emergency fund is only {:.1%} of your target. Aim to save ${:,.0f} more.'.format(emergency_fund_ratio, emergency_fund_target - current_savings),
                'action': 'Increase monthly savings by 10-20% of income'
            })
        
        # Debt recommendations
        total_debt = sum(float(debt['current_balance']) for debt in debts)
        debt_to_income_ratio = total_debt / monthly_income if monthly_income > 0 else 0
        
        if debt_to_income_ratio > 0.5:
            recommendations.append({
                'type': 'debt',
                'priority': 'high',
                'title': 'High Debt Burden',
                'description': 'Your debt is {:.1%} of your income. Focus on debt reduction.'.format(debt_to_income_ratio),
                'action': 'Use avalanche method to pay off highest interest debt first'
            })
        
        # Income optimization
        if income_changes:
            recommendations.append({
                'type': 'income',
                'priority': 'medium',
                'title': 'Income Changes Planned',
                'description': 'You have {} income changes planned. Adjust your budget accordingly.'.format(len(income_changes)),
                'action': 'Review and update your financial plan monthly'
            })
        
        # Expense optimization
        high_expenses = [exp for exp in expenses if float(exp.get('amount', 0)) > monthly_income * 0.3]
        if high_expenses:
            recommendations.append({
                'type': 'expenses',
                'priority': 'medium',
                'title': 'High Expense Categories',
                'description': 'Consider reducing expenses in: {}'.format(", ".join([exp["category"] for exp in high_expenses])),
                'action': 'Look for ways to reduce these expenses by 10-20%'
            })
        
        # Goal recommendations
        for goal in goals:
            if goal.get('type') == 'savings' and float(goal.get('target_amount', 0)) > current_savings * 2:
                recommendations.append({
                    'type': 'goals',
                    'priority': 'medium',
                    'title': 'Large Savings Goal',
                    'description': 'Your goal "{}" requires significant savings.'.format(goal.get("name")),
                    'action': 'Consider breaking it into smaller, more achievable milestones'
                })
        
        return recommendations
    
    def calculate_financial_health_score(self, monthly_income, current_savings, total_debt, total_expenses, emergency_fund_target, available_funds):
        """Calculate overall financial health score (0-100)"""
        score = 0
        
        # Emergency fund score (25 points)
        emergency_fund_ratio = current_savings / emergency_fund_target if emergency_fund_target > 0 else 0
        if emergency_fund_ratio >= 1:
            score += 25
        elif emergency_fund_ratio >= 0.5:
            score += 15
        elif emergency_fund_ratio >= 0.25:
            score += 10
        else:
            score += 5
        
        # Debt-to-income ratio score (25 points)
        debt_to_income = total_debt / monthly_income if monthly_income > 0 else 1
        if debt_to_income <= 0.2:
            score += 25
        elif debt_to_income <= 0.4:
            score += 20
        elif debt_to_income <= 0.6:
            score += 15
        elif debt_to_income <= 0.8:
            score += 10
        else:
            score += 5
        
        # Expense ratio score (25 points)
        expense_ratio = total_expenses / monthly_income if monthly_income > 0 else 1
        if expense_ratio <= 0.5:
            score += 25
        elif expense_ratio <= 0.7:
            score += 20
        elif expense_ratio <= 0.8:
            score += 15
        elif expense_ratio <= 0.9:
            score += 10
        else:
            score += 5
        
        # Available funds score (25 points)
        available_ratio = available_funds / monthly_income if monthly_income > 0 else 0
        if available_ratio >= 0.3:
            score += 25
        elif available_ratio >= 0.2:
            score += 20
        elif available_ratio >= 0.1:
            score += 15
        elif available_ratio >= 0.05:
            score += 10
        else:
            score += 5
        
        return min(100, score)

# Initialize the planner
planner = ComprehensiveFinancialPlanner()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/calculate-plan", methods=["POST"])
def calculate_plan():
    try:
        data = request.get_json()
        result = planner.calculate_comprehensive_plan(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/expense-categories", methods=["GET"])
def get_expense_categories():
    return jsonify(planner.expense_categories)

if __name__ == "__main__":
    app.run(debug=True)
