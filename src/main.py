from flask import Flask, render_template, request, url_for, jsonify
import pandas as pd
from flask_cors import CORS
import json
from datetime import datetime, timedelta

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

def calculate_debt_payoff_plan(monthly_income, keep_in_checking, debts, strategy="avalanche"):
    """
    Calculate optimal debt payoff plan using different strategies
    
    Strategies:
    - avalanche: Pay highest interest rate first (saves most money)
    - snowball: Pay smallest balance first (psychological wins)
    - hybrid: Balance between avalanche and snowball
    """
    available_funds = float(monthly_income - keep_in_checking)
    
    # Create a copy of debts to work with
    debts_copy = []
    for debt in debts:
        debt_copy = debt.copy()
        debt_copy['current_balance'] = float(debt['current_balance'])
        debt_copy['interest_rate'] = float(debt['interest_rate'])
        debt_copy['minimum_payment'] = float(debt['minimum_payment'])
        debt_copy['priority'] = int(debt.get('priority', 5))  # Default priority 5
        debts_copy.append(debt_copy)
    
    # Sort debts based on strategy
    if strategy == "avalanche":
        # Sort by interest rate (highest first), then by priority (lowest first)
        debts_copy.sort(key=lambda x: (-x['interest_rate'], x['priority']))
    elif strategy == "snowball":
        # Sort by balance (smallest first), then by priority
        debts_copy.sort(key=lambda x: (x['current_balance'], x['priority']))
    elif strategy == "hybrid":
        # Sort by priority first, then by interest rate
        debts_copy.sort(key=lambda x: (x['priority'], -x['interest_rate']))
    
    # First, pay all minimum payments
    total_minimum_payments = sum(debt['minimum_payment'] for debt in debts_copy)
    remaining_funds = available_funds - total_minimum_payments
    
    if remaining_funds < 0:
        # Not enough to cover minimum payments
        return {
            "error": f"Insufficient funds. Need ${total_minimum_payments:.2f} for minimum payments, but only have ${available_funds:.2f} available."
        }
    
    # Allocate remaining funds to highest priority/interest debts
    allocations = []
    for debt in debts_copy:
        allocation = debt['minimum_payment']  # Start with minimum payment
        
        if remaining_funds > 0:
            # Add extra payment to this debt
            extra_payment = min(remaining_funds, debt['current_balance'] - debt['minimum_payment'])
            allocation += extra_payment
            remaining_funds -= extra_payment
        
        # Calculate interest paid this month
        monthly_interest = (debt['current_balance'] - allocation) * (debt['interest_rate'] / 100 / 12)
        
        # Calculate new balance after payment
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
    
    # Calculate summary statistics
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

def calculate_payoff_timeline(monthly_income, keep_in_checking, debts, strategy="avalanche"):
    """Calculate how long it will take to pay off all debts"""
    timeline = []
    current_debts = [debt.copy() for debt in debts]
    month = 0
    
    while any(debt['current_balance'] > 0 for debt in current_debts):
        month += 1
        
        # Calculate this month's allocation
        result = calculate_debt_payoff_plan(monthly_income, keep_in_checking, current_debts, strategy)
        
        if 'error' in result:
            timeline.append({
                'month': month,
                'error': result['error']
            })
            break
        
        # Update debt balances for next month
        for i, allocation in enumerate(result['allocations']):
            current_debts[i]['current_balance'] = allocation['new_balance']
        
        timeline.append({
            'month': month,
            'allocations': result['allocations'],
            'summary': result['summary']
        })
        
        # Stop if all debts are paid off
        if all(debt['current_balance'] <= 0 for debt in current_debts):
            break
        
        # Safety check to prevent infinite loop
        if month > 120:  # 10 years max
            break
    
    return timeline

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/allocate", methods=["POST"])
def allocate():
    data = request.json
    monthly_income = float(data["monthly_income"])
    keep_in_checking = float(data["keep_in_checking"])
    debts = data["debts"]
    strategy = data.get("strategy", "avalanche")
    
    result = calculate_debt_payoff_plan(monthly_income, keep_in_checking, debts, strategy)
    return jsonify(result)

@app.route("/timeline", methods=["POST"])
def timeline():
    data = request.json
    monthly_income = float(data["monthly_income"])
    keep_in_checking = float(data["keep_in_checking"])
    debts = data["debts"]
    strategy = data.get("strategy", "avalanche")
    
    timeline = calculate_payoff_timeline(monthly_income, keep_in_checking, debts, strategy)
    return jsonify({"timeline": timeline})

@app.route("/compare-strategies", methods=["POST"])
def compare_strategies():
    data = request.json
    monthly_income = float(data["monthly_income"])
    keep_in_checking = float(data["keep_in_checking"])
    debts = data["debts"]
    
    strategies = ["avalanche", "snowball", "hybrid"]
    results = {}
    
    for strategy in strategies:
        timeline = calculate_payoff_timeline(monthly_income, keep_in_checking, debts, strategy)
        total_interest = sum(
            month['summary']['total_interest_paid'] 
            for month in timeline 
            if 'summary' in month
        )
        months_to_payoff = len([month for month in timeline if 'error' not in month])
        
        results[strategy] = {
            'months_to_payoff': months_to_payoff,
            'total_interest_paid': round(total_interest, 2),
            'total_payments': round(sum(
                month['summary']['total_allocated'] 
                for month in timeline 
                if 'summary' in month
            ), 2)
        }
    
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
