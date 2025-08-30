# 🚀 Smart Debt Payoff Optimizer

A sophisticated web application designed to help you optimize your debt payoff strategy using your $8k monthly income. This tool uses advanced algorithms to minimize interest payments and maximize your debt payoff efficiency.

## ✨ Features

### 🎯 Multiple Payoff Strategies
- **Avalanche Method**: Pay highest interest rate first (saves most money)
- **Snowball Method**: Pay smallest balance first (psychological wins)
- **Hybrid Method**: Balance between priority and interest rates

### 💰 Smart Allocation
- **Priority Levels**: Set importance for each debt (Critical to Minimal)
- **Interest Rate Optimization**: Automatically calculates monthly interest
- **Minimum Payment Handling**: Ensures all minimum payments are covered
- **Remaining Fund Distribution**: Optimally allocates extra funds

### 📊 Comprehensive Analytics
- **Real-time Calculations**: See monthly interest and principal breakdown
- **Strategy Comparison**: Compare all three methods side-by-side
- **Payoff Timeline**: Project how long until debt freedom
- **Interest Savings**: Track total interest paid vs. saved

### 🎨 Modern UI/UX
- **React-based Frontend**: Smooth, responsive interface
- **Real-time Updates**: Instant calculations as you type
- **Visual Feedback**: Color-coded priority levels and status
- **Mobile Responsive**: Works perfectly on all devices

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd stupid-fund-allocator
   ```

2. **Navigate to the source directory**
   ```bash
   cd src
   ```

3. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

## 📖 How to Use

### 1. Set Your Income
- Enter your monthly income (default: $8,000)
- Set how much you want to keep in checking (default: $1,000)
- The remaining amount will be used for debt payoff

### 2. Add Your Debts
For each debt, provide:
- **Name**: e.g., "Credit Card", "Student Loan"
- **Current Balance**: Total amount owed
- **Interest Rate**: Annual percentage rate
- **Minimum Payment**: Required monthly payment
- **Priority Level**: How important this debt is to you

### 3. Choose Your Strategy
- **Avalanche**: Best for saving money (pay highest interest first)
- **Snowball**: Best for motivation (pay smallest balance first)
- **Hybrid**: Best for balancing both approaches

### 4. Analyze Results
- View monthly allocation plan
- See principal vs. interest breakdown
- Compare different strategies
- Track your progress over time

## 🎯 Priority Levels Explained

1. **🔥 Critical (1)**: Must pay off immediately (high interest, urgent)
2. **⚡ High (2)**: Important debts that should be prioritized
3. **⚠️ Medium (3)**: Standard priority debts
4. **📊 Low (4)**: Lower priority, can wait longer
5. **💤 Minimal (5)**: Lowest priority, pay last

## 📈 Strategy Comparison

### Avalanche Method
- **Pros**: Saves the most money on interest
- **Cons**: May take longer to see first debt paid off
- **Best for**: People focused on total cost savings

### Snowball Method
- **Pros**: Quick wins provide motivation
- **Cons**: May cost more in total interest
- **Best for**: People who need psychological wins

### Hybrid Method
- **Pros**: Balances financial optimization with personal priorities
- **Cons**: More complex to understand
- **Best for**: People who want the best of both worlds

## 🔧 Technical Details

### Backend (Python/Flask)
- **Framework**: Flask with CORS support
- **Algorithms**: Custom debt payoff optimization
- **Data Processing**: Pandas for calculations
- **APIs**: RESTful endpoints for calculations

### Frontend (React)
- **Framework**: React 18 with Babel
- **Styling**: Tailwind CSS
- **State Management**: React hooks
- **Data Persistence**: LocalStorage

### Key Algorithms
- **Interest Calculation**: Monthly compound interest
- **Allocation Logic**: Priority-based fund distribution
- **Timeline Projection**: Multi-month payoff simulation
- **Strategy Comparison**: Side-by-side analysis

## 📊 API Endpoints

### POST `/allocate`
Calculate optimal debt payoff plan for current month.

**Request Body:**
```json
{
  "monthly_income": 8000,
  "keep_in_checking": 1000,
  "debts": [
    {
      "name": "Credit Card",
      "current_balance": 5000,
      "interest_rate": 18.99,
      "minimum_payment": 150,
      "priority": 1
    }
  ],
  "strategy": "avalanche"
}
```

**Response:**
```json
{
  "allocations": [...],
  "summary": {
    "total_allocated": 2500,
    "total_principal_paid": 2300,
    "total_interest_paid": 200,
    "remaining_funds": 500,
    "strategy_used": "avalanche"
  }
}
```

### POST `/compare-strategies`
Compare all three payoff strategies.

### POST `/timeline`
Generate complete payoff timeline.

## 🎨 Customization

### Adding New Strategies
1. Modify the `calculate_debt_payoff_plan` function in `main.py`
2. Add your strategy logic to the sorting section
3. Update the frontend strategy options

### Styling Changes
- Edit `src/static/css/main.css` for custom styles
- Modify Tailwind classes in the HTML template
- Add new CSS animations and effects

## 🚀 Deployment

### Local Development
```bash
python main.py
```

### Production Deployment
1. Set up a production WSGI server (Gunicorn)
2. Configure environment variables
3. Set up reverse proxy (Nginx)
4. Enable HTTPS

### Docker Deployment
```bash
docker build -t debt-optimizer .
docker run -p 5000:5000 debt-optimizer
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 💡 Tips for Maximum Effectiveness

1. **Be Honest**: Enter accurate debt information for best results
2. **Update Regularly**: Recalculate as your situation changes
3. **Consider Refinancing**: Look for lower interest rates when possible
4. **Stay Disciplined**: Follow the allocation plan consistently
5. **Track Progress**: Use the timeline feature to stay motivated

## 🆘 Support

If you encounter any issues:
1. Check the browser console for errors
2. Verify all debt information is entered correctly
3. Ensure you have sufficient funds for minimum payments
4. Try refreshing the page and re-entering data

---

**Happy debt-free journey! 🎉**
