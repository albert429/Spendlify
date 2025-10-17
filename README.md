# 💰 Personal Finance Manager

A comprehensive console-based Python application for managing personal finances, tracking expenses, monitoring income, and generating insightful financial reports.

## 📋 Project Information

**Due Date:** October 24, 2025  
**Duration:** 10 Days  
**Language:** Python 3.x  
**Interface:** Console/Terminal Application

---

## 🎯 Overview

The Personal Finance Manager is a powerful command-line tool that helps users take control of their financial life. Whether you're tracking daily expenses, setting savings goals, or analyzing spending patterns, this application provides all the tools you need to make informed financial decisions.

### Key Highlights

- 🔐 Multi-user support with secure PIN/password protection
- 💳 Complete transaction management (income & expenses)
- 📊 Comprehensive financial reports and analytics
- 🔍 Advanced search and filtering capabilities
- 💾 Persistent data storage with auto-save
- 🎨 Intuitive menu-driven interface

---

## ✨ Core Features

### 👤 User Management
- **Multi-User Support**: Multiple users can maintain separate financial profiles
- **Security**: PIN/password protection for account access
- **Profile Management**: Create, edit, and switch between user profiles
- **Data Isolation**: Each user's financial data remains private and separate

### 💳 Transaction Management
- **Add Transactions**: Record income and expenses with detailed categorization
- **View History**: Browse complete transaction history with formatting
- **Edit Transactions**: Modify existing transaction details
- **Delete Safely**: Remove transactions with confirmation prompts
- **Categories**: Organize transactions by customizable categories

### 📊 Financial Reports
- **Dashboard Summary**: Quick overview of your financial status
- **Monthly Reports**: Detailed breakdown of income and expenses by month
- **Category Analysis**: Spending distribution across different categories
- **Trend Analysis**: Identify spending patterns and financial trends
- **Visual Insights**: Clear presentation of financial data

### 🔍 Search & Filter
- **Date Range Search**: Find transactions within specific time periods
- **Category Filter**: View transactions by category
- **Amount Range**: Filter transactions by amount thresholds
- **Sort Options**: Organize results by date, amount, or category
- **Combined Filters**: Use multiple filters simultaneously

### 💾 Data Management
- **Multiple Formats**: Save data in CSV and JSON formats
- **Auto-Save**: Automatic data persistence after changes
- **Backup System**: Create and restore data backups
- **Data Integrity**: Validation checks to ensure data consistency
- **Import/Export**: Transfer data between systems

---

## 🚀 Advanced Features

This application includes the following advanced capabilities:

### 1. 🎯 Savings Goals with Progress Tracking
- Set multiple savings goals with target amounts and deadlines
- Track progress with percentage completion
- Visual progress indicators
- Goal achievement notifications
- Contribution history

### 2. 📅 Monthly Budget Management
- Define category-specific budgets
- Real-time budget tracking
- Overspending alerts
- Budget vs. actual comparisons
- Rollover options for unused budget

### 3. 🔄 Recurring Transactions
- Automate regular income and expenses
- Multiple frequency options (daily, weekly, monthly, yearly)
- Auto-populate recurring transactions
- Edit or cancel recurring entries
- Preview upcoming transactions

### 4. 📈 ASCII Data Visualization
- Bar charts for category spending
- Line graphs for trend analysis
- Budget utilization meters
- Savings goal progress bars
- Console-friendly graphics

### 5. 🔮 Predictive Analytics
- Forecast future expenses based on historical data
- Predict goal achievement timelines
- Identify unusual spending patterns
- Cash flow projections
- Savings recommendations

### 6. 📁 CSV Import/Export
- Import transactions from bank statements
- Export data for external analysis
- Bulk transaction upload
- Format validation
- Data mapping options

### 7. 🔔 Bill Reminders System
- Set reminders for upcoming bills
- Multiple reminder notifications
- Recurring bill tracking
- Payment history
- Overdue alerts

### 8. 💯 Financial Health Score
- Comprehensive financial wellness assessment
- Scoring across multiple dimensions
- Personalized recommendations
- Track improvement over time
- Benchmark against best practices

---

## 🛠️ Technical Architecture

### Data Structures
```
User Profile:
- user_id (unique identifier)
- username
- password_hash
- created_date
- settings

Transaction:
- transaction_id
- user_id
- type (income/expense)
- amount
- category
- date
- description
- recurring_id (optional)

Category:
- category_id
- name
- type (income/expense)
- budget_limit (optional)

Savings Goal:
- goal_id
- user_id
- name
- target_amount
- current_amount
- deadline
- created_date
```

### File Structure
```
personal_finance_manager/
│
├── main.py                 # Application entry point
├── user_manager.py         # User authentication and management
├── transaction_manager.py  # Transaction operations
├── report_generator.py     # Financial reports and analytics
├── data_handler.py         # File I/O operations
├── menu_system.py          # Menu interface
├── validators.py           # Input validation functions
├── utils.py                # Helper functions
│
├── data/
│   ├── users.json         # User profiles
│   ├── transactions.json  # Transaction records
│   ├── categories.json    # Category definitions
│   └── backups/           # Backup files
│
├── reports/               # Generated reports (optional)
├── requirements.txt       # Dependencies
└── README.md             # This file
```

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone or Download the Project**
   ```bash
   git clone <repository-url>
   cd personal_finance_manager
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python main.py
   ```

### First Time Setup
On first run, the application will:
- Create necessary data directories
- Initialize default categories
- Prompt you to create your first user account

---

## 🎮 Usage Guide

### Getting Started

1. **Launch the Application**
   ```bash
   python main.py
   ```

2. **Create Your Account**
   - Select "Register New User"
   - Choose a username
   - Set a secure PIN/password
   - Confirm your credentials

3. **Login**
   - Enter your username
   - Provide your PIN/password
   - Access your financial dashboard

### Basic Operations

#### Adding Transactions
```
Main Menu → Transactions → Add Transaction
1. Select type (Income/Expense)
2. Enter amount
3. Choose category
4. Add description
5. Set date (or use today)
6. Confirm and save
```

#### Viewing Reports
```
Main Menu → Reports
- Dashboard: Quick financial overview
- Monthly Report: Detailed monthly breakdown
- Category Analysis: Spending by category
- Trends: Spending patterns over time
```

#### Setting Savings Goals
```
Main Menu → Savings Goals → Create New Goal
1. Enter goal name
2. Set target amount
3. Choose deadline
4. Track progress from dashboard
```

### Menu Navigation
- Use number keys to select options
- Type 'back' to return to previous menu
- Type 'help' for context-sensitive assistance
- Type 'exit' or 'quit' to logout/close

---

## 🔒 Security Features

- **Password Protection**: Hashed password storage using industry-standard algorithms
- **Session Management**: Automatic logout after inactivity
- **Data Encryption**: Sensitive data encrypted at rest (optional)
- **Backup Integrity**: Checksums for backup verification
- **Access Control**: User-specific data isolation

---

## 📊 Sample Reports

### Dashboard Summary
```
=====================================
   FINANCIAL DASHBOARD
=====================================
Current Balance: $5,247.82
Monthly Income:  $4,500.00
Monthly Expenses: $3,252.18
Net Savings:     $1,247.82

Budget Status: 72% utilized
Savings Goals: 3 active (2 on track)
Upcoming Bills: $450.00 (next 7 days)
=====================================
```

### Category Breakdown
```
Spending by Category (Current Month)
====================================
Housing       ████████████ $1,200  37%
Food          ████████░░░░ $  650  20%
Transport     █████░░░░░░░ $  420  13%
Entertainment ████░░░░░░░░ $  300   9%
Utilities     ███░░░░░░░░░ $  250   8%
Other         ████░░░░░░░░ $  432  13%
====================================
Total:                   $3,252 100%
```

---

## 🧪 Testing

### Manual Testing Checklist
- [ ] User registration and login
- [ ] Add income transactions
- [ ] Add expense transactions
- [ ] Edit existing transactions
- [ ] Delete transactions
- [ ] Generate all report types
- [ ] Search and filter operations
- [ ] Data persistence (restart app)
- [ ] Backup and restore
- [ ] Multi-user switching

### Test Data
Sample test data is provided in `data/test_data.json` for development purposes.

---

## 🐛 Troubleshooting

### Common Issues

**Problem**: Data file not found error  
**Solution**: Ensure the `data/` directory exists. Run `python main.py --init` to recreate.

**Problem**: Password not working  
**Solution**: Passwords are case-sensitive. Use "Forgot Password" option if available.

**Problem**: Reports showing incorrect data  
**Solution**: Check date filters. Ensure transactions are in correct date format.

**Problem**: Import fails  
**Solution**: Verify CSV format matches expected schema. Check for special characters.

---

## 🚀 Future Enhancements

Potential features for future versions:
- 🌐 Web-based interface
- 📱 Mobile app companion
- 🔗 Bank account integration
- 🤖 AI-powered financial advice
- 📧 Email notifications
- 🌍 Multi-currency support
- 📸 Receipt scanning
- 👥 Shared household budgets

---

## 📚 Learning Outcomes

By completing this project, you will have demonstrated:

✅ **Python Fundamentals**
- Variables, data types, and operators
- Control structures (if/else, loops)
- Functions and modularity
- Object-oriented programming concepts

✅ **Data Management**
- Complex data structures (lists, dictionaries, sets)
- File I/O operations (CSV, JSON)
- Data validation and sanitization
- Error handling and exceptions

✅ **Software Design**
- Menu-driven architecture
- Modular code organization
- User experience design
- Code documentation

✅ **Problem Solving**
- Algorithm development
- Financial calculations
- Search and sort operations
- Data analysis and reporting

---

## 📝 Documentation

### Code Style
- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Include docstrings for all functions and classes
- Comment complex logic

### Version Control
- Commit regularly with descriptive messages
- Use branches for new features
- Tag releases appropriately
---

**Happy Coding! 💻✨**

*Take control of your finances, one transaction at a time.*
