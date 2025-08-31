from flask import Flask, render_template, request, url_for, jsonify
import pandas as pd
from flask_cors import CORS
import json
from datetime import datetime, timedelta
import math

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

class SmartAllocator:
    def __init__(self):
        self.categories = {
            'bills': {
                'name': 'Bills',
                'color': 'red',
                'icon': '🏠',
                'description': 'Rent, utilities, phone, internet'
            },
            'food': {
                'name': 'Food',
                'color': 'orange',
                'icon': '🍕',
                'description': 'Groceries, eating out, coffee'
            },
            'transport': {
                'name': 'Transportation',
                'color': 'blue',
                'icon': '🚗',
                'description': 'Gas, car payment, public transit'
            },
            'debt': {
                'name': 'Debt',
                'color': 'red',
                'icon': '💳',
                'description': 'Credit cards, loans, student debt'
            },
            'fun': {
                'name': 'Fun Stuff',
                'color': 'purple',
                'icon': '🎉',
                'description': 'Entertainment, hobbies, shopping'
            },
            'health': {
                'name': 'Health',
                'color': 'green',
                'icon': '🏥',
                'description': 'Insurance, medical, fitness'
            },
            'savings': {
                'name': 'Savings',
                'color': 'green',
                'icon': '💰',
                'description': 'Emergency fund, retirement, investments'
            }
        }
    
    def analyze_spending_patterns(self, expenses):
        """AI-powered analysis of spending patterns"""
        analysis = {
            'total_expenses': sum(float(exp.get('amount', 0)) for exp in expenses),
            'category_breakdown': {},
            'insights': [],
            'recommendations': [],
            'risk_factors': []
        }
        
        # Category breakdown
        for expense in expenses:
            category = expense.get('category', 'other')
            if category not in analysis['category_breakdown']:
                analysis['category_breakdown'][category] = 0
            analysis['category_breakdown'][category] += float(expense.get('amount', 0))
        
        # AI Insights
        total = analysis['total_expenses']
        if total > 0:
            # Bills analysis
            bills_pct = (analysis['category_breakdown'].get('bills', 0) / total) * 100
            if bills_pct > 40:
                analysis['insights'].append("Your bills are taking up a large portion of your income")
                analysis['recommendations'].append("Consider ways to reduce rent or utility costs")
            elif bills_pct < 25:
                analysis['insights'].append("Your bills are well-managed")
                analysis['recommendations'].append("Great job keeping housing costs low!")
            
            # Debt analysis
            debt_pct = (analysis['category_breakdown'].get('debt', 0) / total) * 100
            if debt_pct > 20:
                analysis['risk_factors'].append("High debt payments may limit financial flexibility")
                analysis['recommendations'].append("Focus on debt payoff strategies")
            elif debt_pct < 10:
                analysis['insights'].append("Low debt burden - excellent financial position")
            
            # Savings analysis
            savings_pct = (analysis['category_breakdown'].get('savings', 0) / total) * 100
            if savings_pct < 10:
                analysis['risk_factors'].append("Low savings rate may leave you vulnerable")
                analysis['recommendations'].append("Aim to save at least 10-20% of income")
            elif savings_pct > 20:
                analysis['insights'].append("Excellent savings rate - building wealth!")
            
            # Fun spending analysis
            fun_pct = (analysis['category_breakdown'].get('fun', 0) / total) * 100
            if fun_pct > 25:
                analysis['risk_factors'].append("High entertainment spending may impact long-term goals")
                analysis['recommendations'].append("Consider balancing fun with savings")
            elif fun_pct < 5:
                analysis['insights'].append("Very low entertainment spending - don't forget to enjoy life!")
                analysis['recommendations'].append("Consider allocating some funds for enjoyment")
        
        return analysis

    def calculate_optimal_allocation(self, monthly_income, expenses, goals, strategy="balanced"):
        """Calculate optimal allocation based on income, current expenses, and goals"""
        
        # AI-powered allocation strategy
        if strategy == "balanced":
            # 50/30/20 rule with AI adjustments
            bills_target = monthly_income * 0.3
            food_target = monthly_income * 0.15
            transport_target = monthly_income * 0.1
            fun_target = monthly_income * 0.15
            savings_target = monthly_income * 0.2
            health_target = monthly_income * 0.1
        elif strategy == "aggressive_savings":
            bills_target = monthly_income * 0.25
            food_target = monthly_income * 0.1
            transport_target = monthly_income * 0.1
            fun_target = monthly_income * 0.1
            savings_target = monthly_income * 0.35
            health_target = monthly_income * 0.1
        elif strategy == "debt_focused":
            bills_target = monthly_income * 0.25
            food_target = monthly_income * 0.1
            transport_target = monthly_income * 0.1
            debt_target = monthly_income * 0.3
            fun_target = monthly_income * 0.1
            savings_target = monthly_income * 0.1
            health_target = monthly_income * 0.05
        elif strategy == "enjoyment_focused":
            bills_target = monthly_income * 0.25
            food_target = monthly_income * 0.15
            transport_target = monthly_income * 0.1
            fun_target = monthly_income * 0.25
            savings_target = monthly_income * 0.15
            health_target = monthly_income * 0.1
        else:  # custom
            bills_target = monthly_income * 0.3
            food_target = monthly_income * 0.15
            transport_target = monthly_income * 0.1
            fun_target = monthly_income * 0.2
            savings_target = monthly_income * 0.15
            health_target = monthly_income * 0.1
        
        # Calculate current allocations
        current_allocations = {}
        for expense in expenses:
            category = expense.get('category', 'other')
            if category not in current_allocations:
                current_allocations[category] = 0
            current_allocations[category] += float(expense.get('amount', 0))
        
        # Generate recommendations
        recommendations = []
        adjustments = {}
        
        # Bills - must be covered
        bills_current = current_allocations.get('bills', 0)
        if bills_current > bills_target:
            recommendations.append("Bills exceed target by ${:.2f}".format(bills_current - bills_target))
            adjustments['bills'] = bills_current
        else:
            adjustments['bills'] = bills_current
        
        # Debt optimization
        debt_current = current_allocations.get('debt', 0)
        if debt_current > 0:
            # AI recommendation: prioritize high-interest debt
            recommendations.append("Prioritize high-interest debt payments")
            adjustments['debt'] = debt_current
        
        # Savings optimization
        savings_current = current_allocations.get('savings', 0)
        if savings_current < savings_target:
            recommendations.append("Increase savings by ${:.2f}".format(savings_target - savings_current))
            adjustments['savings'] = savings_target
        else:
            adjustments['savings'] = savings_current
        
        # Fun spending
        fun_current = current_allocations.get('fun', 0)
        remaining_income = monthly_income - sum(adjustments.values())
        if remaining_income > 0:
            adjustments['fun'] = min(fun_target, remaining_income)
        else:
            adjustments['fun'] = 0
        
        return {
            'current_allocations': current_allocations,
            'recommended_allocations': adjustments,
            'recommendations': recommendations,
            'strategy_used': strategy,
            'total_allocated': sum(adjustments.values()),
            'remaining_income': monthly_income - sum(adjustments.values())
        }

    def generate_ai_insights(self, monthly_income, expenses, goals):
        """Generate AI-powered financial insights"""
        insights = {
            'financial_health_score': 0,
            'key_metrics': {},
            'insights': [],
            'action_items': [],
            'trends': []
        }
        
        total_expenses = sum(float(exp.get('amount', 0)) for exp in expenses)
        savings_rate = (monthly_income - total_expenses) / monthly_income * 100
        
        # Calculate financial health score
        score = 0
        
        # Savings rate scoring
        if savings_rate >= 20:
            score += 30
            insights['insights'].append("Excellent savings rate! You're building wealth effectively.")
        elif savings_rate >= 10:
            score += 20
            insights['insights'].append("Good savings rate. Consider increasing to 20% of income for better financial security.")
        elif savings_rate >= 5:
            score += 10
            insights['insights'].append("Moderate savings rate. Focus on increasing savings for emergencies.")
        else:
            insights['action_items'].append("Increase savings rate to at least 10% of income")
        
        # Debt analysis
        debt_expenses = sum(float(exp.get('amount', 0)) for exp in expenses if exp.get('category') == 'debt')
        debt_ratio = debt_expenses / monthly_income * 100
        
        if debt_ratio <= 10:
            score += 25
            insights['insights'].append("Low debt burden - excellent financial position!")
        elif debt_ratio <= 20:
            score += 15
            insights['insights'].append("Manageable debt level. Continue paying down debt.")
        elif debt_ratio <= 30:
            score += 5
            insights['action_items'].append("High debt burden. Focus on debt reduction strategies.")
        else:
            insights['action_items'].append("Critical debt situation. Seek financial counseling.")
        
        # Bills analysis
        bills_expenses = sum(float(exp.get('amount', 0)) for exp in expenses if exp.get('category') == 'bills')
        bills_ratio = bills_expenses / monthly_income * 100
        
        if bills_ratio <= 30:
            score += 25
            insights['insights'].append("Your bills are well-controlled.")
        elif bills_ratio <= 50:
            score += 15
            insights['insights'].append("Your bills are manageable.")
        else:
            insights['action_items'].append("Your bills are high. Look for ways to reduce housing costs.")
        
        # Emergency fund analysis
        savings_expenses = sum(float(exp.get('amount', 0)) for exp in expenses if exp.get('category') == 'savings')
        if savings_expenses >= monthly_income * 0.1:
            score += 20
            insights['insights'].append("Good emergency fund contribution.")
        else:
            insights['action_items'].append("Build emergency fund with at least 10% of income.")
        
        insights['financial_health_score'] = min(100, score)
        insights['key_metrics'] = {
            'savings_rate': round(savings_rate, 1),
            'debt_ratio': round(debt_ratio, 1),
            'bills_ratio': round(bills_ratio, 1),
            'disposable_income': monthly_income - total_expenses
        }
        
        return insights

def calculate_debt_payoff_plan(monthly_income, keep_in_checking, debts, strategy="avalanche"):
    """Calculate optimal debt payoff plan using different strategies"""
    available_funds = float(monthly_income - keep_in_checking)
    
    # Create a copy of debts to work with
    debts_copy = []
    for debt in debts:
        debt_copy = debt.copy()
        debt_copy['current_balance'] = float(debt['current_balance'])
        debt_copy['interest_rate'] = float(debt['interest_rate'])
        debt_copy['minimum_payment'] = float(debt['minimum_payment'])
        # Convert priority string to numeric value
        priority_str = debt.get('priority', 'medium')
        if priority_str == 'high':
            debt_copy['priority'] = 1
        elif priority_str == 'medium':
            debt_copy['priority'] = 2
        elif priority_str == 'low':
            debt_copy['priority'] = 3
        else:
            debt_copy['priority'] = 2  # default to medium
        debts_copy.append(debt_copy)
    
    # Sort debts based on strategy
    if strategy == "avalanche":
        debts_copy.sort(key=lambda x: (-x['interest_rate'], x['priority']))
    elif strategy == "snowball":
        debts_copy.sort(key=lambda x: (x['current_balance'], x['priority']))
    elif strategy == "hybrid":
        debts_copy.sort(key=lambda x: (x['priority'], -x['interest_rate']))
    
    # First, pay all minimum payments
    total_minimum_payments = sum(debt['minimum_payment'] for debt in debts_copy)
    remaining_funds = available_funds - total_minimum_payments
    
    if remaining_funds < 0:
        return {
            "error": "Insufficient funds. Need ${:.2f} for minimum payments, but only have ${:.2f} available.".format(
                total_minimum_payments, available_funds
            )
        }
    
    # Allocate remaining funds to highest priority/interest debts
    allocations = []
    for debt in debts_copy:
        allocation = debt['minimum_payment']
        
        if remaining_funds > 0:
            extra_payment = min(remaining_funds, debt['current_balance'] - debt['minimum_payment'])
            allocation += extra_payment
            remaining_funds -= extra_payment
        
        monthly_interest = (debt['current_balance'] - allocation) * (debt['interest_rate'] / 100 / 12)
        new_balance = max(0, debt['current_balance'] - allocation + monthly_interest)
        
        allocations.append({
            'name': debt['name'],
            'current_balance': debt['current_balance'],
            'interest_rate': debt['interest_rate'],
            'minimum_payment': debt['minimum_payment'],
            'priority': debt['priority'],
            'allocated': round(allocation, 2),
            'new_balance': round(new_balance, 2),
            'interest_paid': round(monthly_interest, 2),
            'principal_paid': round(allocation - monthly_interest, 2)
        })
    
    total_allocated = sum(item['allocated'] for item in allocations)
    total_interest_paid = sum(item['interest_paid'] for item in allocations)
    total_principal_paid = sum(item['principal_paid'] for item in allocations)
    
    return {
        'allocations': allocations,
        'summary': {
            'total_allocated': round(total_allocated, 2),
            'total_interest_paid': round(total_interest_paid, 2),
            'total_principal_paid': round(total_principal_paid, 2),
            'remaining_funds': round(remaining_funds, 2),
            'strategy_used': strategy
        }
    }

# Initialize the smart allocator
smart_allocator = SmartAllocator()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/allocate", methods=["POST"])
def allocate():
    try:
        data = request.get_json()
        monthly_income = float(data.get('monthly_income', 0))
        keep_in_checking = float(data.get('keep_in_checking', 0))
        debts = data.get('debts', [])
        strategy = data.get('strategy', 'avalanche')
        
        # Calculate debt payoff plan
        result = calculate_debt_payoff_plan(monthly_income, keep_in_checking, debts, strategy)
        
        if 'error' in result:
            return jsonify(result), 400
        
        # Calculate timeline
        timeline = calculate_payoff_timeline(monthly_income, keep_in_checking, debts, strategy)
        
        # Compare strategies
        comparison = compare_strategies(monthly_income, keep_in_checking, debts)
        
        # Calculate total interest saved (compared to minimum payments only)
        total_interest_saved = 0
        if result['allocations']:
            total_interest_saved = sum(item['interest_paid'] for item in result['allocations'])
        
        return jsonify({
            'allocation': result['allocations'],
            'total_interest_saved': total_interest_saved,
            'timeline': timeline,
            'strategy_comparison': comparison
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/categories", methods=["GET"])
def get_categories():
    return jsonify(smart_allocator.categories)

def calculate_payoff_timeline(monthly_income, keep_in_checking, debts, strategy):
    """Calculate the timeline for paying off all debts"""
    timeline = []
    current_debts = [debt.copy() for debt in debts]
    month = 0
    total_interest_paid = 0
    
    while any(float(debt['current_balance']) > 0 for debt in current_debts):
        month += 1
        result = calculate_debt_payoff_plan(monthly_income, keep_in_checking, current_debts, strategy)
        
        if 'error' in result:
            timeline.append({'month': month, 'error': result['error']})
            break
        
        # Track which debts were paid off this month
        debts_paid_off = []
        for i, allocation in enumerate(result['allocations']):
            old_balance = float(current_debts[i]['current_balance'])
            new_balance = allocation['new_balance']
            if old_balance > 0 and new_balance <= 0:
                debts_paid_off.append(current_debts[i]['name'])
            current_debts[i]['current_balance'] = new_balance
        
        # Calculate interest paid this month
        interest_paid = sum(allocation['interest_paid'] for allocation in result['allocations'])
        total_interest_paid += interest_paid
        
        # Calculate total remaining debt
        total_remaining = sum(max(0, float(debt['current_balance'])) for debt in current_debts)
        
        timeline.append({
            'month': month,
            'total_remaining': total_remaining,
            'debts_paid_off': debts_paid_off,
            'interest_paid': interest_paid,
            'total_interest_paid': total_interest_paid
        })
        
        if all(float(debt['current_balance']) <= 0 for debt in current_debts):
            break
        
        if month > 120:  # Cap at 10 years
            break
    
    return timeline

@app.route("/timeline", methods=["POST"])
def timeline():
    data = request.json
    monthly_income = float(data["monthly_income"])
    keep_in_checking = float(data["keep_in_checking"])
    debts = data["debts"]
    strategy = data.get("strategy", "avalanche")
    
    timeline = calculate_payoff_timeline(monthly_income, keep_in_checking, debts, strategy)
    return jsonify({"timeline": timeline})

def compare_strategies(monthly_income, keep_in_checking, debts):
    """Compare different debt payoff strategies with advanced analysis"""
    strategies = ["avalanche", "snowball", "hybrid", "due_date", "bonus_optimized"]
    results = {}
    
    # Calculate minimum payment baseline
    total_min_payments = sum(float(debt['minimum_payment']) for debt in debts)
    total_interest_min_only = 0
    
    # Calculate total interest if only making minimum payments
    current_debts = [debt.copy() for debt in debts]
    month = 0
    while any(float(debt['current_balance']) > 0 for debt in current_debts) and month < 120:
        month += 1
        for debt in current_debts:
            if float(debt['current_balance']) > 0:
                interest = float(debt['current_balance']) * float(debt['interest_rate']) / 100 / 12
                total_interest_min_only += interest
                payment = float(debt['minimum_payment'])
                new_balance = float(debt['current_balance']) + interest - payment
                debt['current_balance'] = max(0, new_balance)
    
    # Calculate equal payment strategy (the bad one)
    available_funds = float(monthly_income - keep_in_checking)
    extra_funds = available_funds - total_min_payments
    
    if extra_funds > 0:
        # Distribute extra funds equally among all debts
        equal_extra = extra_funds / len(debts)
        equal_payment_timeline = []
        equal_debts = [debt.copy() for debt in debts]
        month = 0
        total_interest_equal = 0
        
        while any(float(debt['current_balance']) > 0 for debt in equal_debts) and month < 120:
            month += 1
            monthly_interest = 0
            
            for debt in equal_debts:
                if float(debt['current_balance']) > 0:
                    interest = float(debt['current_balance']) * float(debt['interest_rate']) / 100 / 12
                    monthly_interest += interest
                    payment = float(debt['minimum_payment']) + equal_extra
                    new_balance = float(debt['current_balance']) + interest - payment
                    debt['current_balance'] = max(0, new_balance)
            
            total_interest_equal += monthly_interest
            total_remaining = sum(max(0, float(debt['current_balance'])) for debt in equal_debts)
            
            equal_payment_timeline.append({
                'month': month,
                'total_remaining': total_remaining,
                'interest_paid': monthly_interest
            })
        
        results['equal_payment'] = {
            'months_to_payoff': len(equal_payment_timeline),
            'total_interest': round(total_interest_equal, 2),
            'interest_saved': round(total_interest_min_only - total_interest_equal, 2),
            'bonus_saved': 0,
            'total_savings': round(total_interest_min_only - total_interest_equal, 2)
        }
    else:
        results['equal_payment'] = {
            'months_to_payoff': 0,
            'total_interest': 0,
            'interest_saved': 0,
            'bonus_saved': 0,
            'total_savings': 0
        }
    
    for strategy in strategies:
        timeline = calculate_payoff_timeline(monthly_income, keep_in_checking, debts, strategy)
        
        if timeline and 'error' not in timeline[0]:
            total_interest = sum(month['interest_paid'] for month in timeline)
            months_to_payoff = len(timeline)
            interest_saved = total_interest_min_only - total_interest
            total_bonus_saved = sum(month.get('total_bonus_saved', 0) for month in timeline)
            
            results[strategy] = {
                'months_to_payoff': months_to_payoff,
                'total_interest': round(total_interest, 2),
                'interest_saved': round(interest_saved, 2),
                'bonus_saved': round(total_bonus_saved, 2),
                'total_savings': round(interest_saved + total_bonus_saved, 2)
            }
        else:
            results[strategy] = {
                'months_to_payoff': 0,
                'total_interest': 0,
                'interest_saved': 0,
                'bonus_saved': 0,
                'total_savings': 0
            }
    
    return results

@app.route("/compare-strategies", methods=["POST"])
def compare_strategies_route():
    data = request.json
    monthly_income = float(data["monthly_income"])
    keep_in_checking = float(data["keep_in_checking"])
    debts = data["debts"]
    
    comparison = compare_strategies(monthly_income, keep_in_checking, debts)
    return jsonify(comparison)

if __name__ == "__main__":
    app.run(debug=True)
