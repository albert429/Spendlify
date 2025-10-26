import os
import datetime
from auth import *
import transactions as tx
from search import run_search
from data_handler import load_transactions
from goals import *
from bill_reminders import *

def clear_screen():
    """Clear the console screen for better UI"""
    os.system('cls' if os.name == 'nt' else 'clear')

def monthly_reports(user):
    """Generate and display monthly report for current user's transactions"""
    # Get current month's start and end dates
    today = datetime.datetime.now()
    start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if today.month == 12:
        end_date = today.replace(year=today.year + 1, month=1, day=1) - datetime.timedelta(days=1)
    else:
        end_date = today.replace(month=today.month + 1, day=1) - datetime.timedelta(days=1)
    
    # Load and filter transactions
    all_transactions = load_transactions()
    monthly_transactions = [
        t for t in all_transactions 
        if t['username'] == user['username'] 
        and start_date <= datetime.datetime.strptime(t['date'], '%Y-%m-%d') <= end_date
    ]
    
    # Calculate totals
    income = sum(float(t['amount']) for t in monthly_transactions if float(t['amount']) > 0)
    expenses = abs(sum(float(t['amount']) for t in monthly_transactions if float(t['amount']) < 0))
    net_balance = income - expenses
    
    # Group transactions by category
    categories = {}
    for transaction in monthly_transactions:
        category = transaction['category']
        amount = float(transaction['amount'])
        if category not in categories:
            categories[category] = {'total': 0, 'count': 0}
        categories[category]['total'] += amount
        categories[category]['count'] += 1
    
    # Display report
    clear_screen()
    print(f"\n{'=' * 50}")
    print(f"Monthly Report for {user['username']} - {today.strftime('%B %Y')}")
    print(f"{'=' * 50}")
    
    print(f"\nSummary:")
    print(f"{'─' * 30}")
    print(f"Total Income:  ${income:,.2f}")
    print(f"Total Expenses: ${expenses:,.2f}")
    print(f"Net Balance:    ${net_balance:,.2f}")
    
    print(f"\nBreakdown by Category:")
    print(f"{'─' * 50}")
    print(f"{'Category':<20} {'Amount':>10} {'Count':>8}")
    print(f"{'─' * 50}")
    for category, data in sorted(categories.items()):
        print(f"{category:<20} ${data['total']:>9,.2f} {data['count']:>8}")
    
    print(f"\n{'=' * 50}")
    input("\nPress Enter to continue...")

def display_header():
    print("""
███████╗██████╗ ███████╗███╗   ██╗██████╗ ██╗     ██╗███████╗██╗   ██╗
██╔════╝██╔══██╗██╔════╝████╗  ██║██╔══██╗██║     ██║██╔════╝╚██╗ ██╔╝
███████╗██████╔╝█████╗  ██╔██╗ ██║██║  ██║██║     ██║█████╗   ╚████╔╝ 
╚════██║██╔═══╝ ██╔══╝  ██║╚██╗██║██║  ██║██║     ██║██╔══╝    ╚██╔╝  
███████║██║     ███████╗██║ ╚████║██████╔╝███████╗██║██║        ██║   
╚══════╝╚═╝     ╚══════╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝╚═╝        ╚═╝   """)
    print("=" * 80)
    print("💰 Personal Finance Manager".center(80))
    print("=" * 80)

def display_main_menu():
    """Display the main menu options"""
    print("\n📋 MAIN MENU\n")
    print("1. 💳 Add/View/edit/delete Transactions (Income/Expense)")
    print("2. 📈 Dashboard Summary")
    print("3. 📅 Monthly Reports")
    print("4. 🔍 Search & Filter Transactions")
    print("5. 🎯 Savings Goals")
    print("6. 🔔 Bill Reminder")
    print("7. 👤 Switch User")
    print("8. ❓ Help")
    print("9. 🚪 Exit")
    print("\n" + "=" * 80)

def display_user_info(current_user):
    """Display current user information"""
    print(f"👤 Current User: {current_user['name']} | Currency: {current_user['currency']}")
    print(f"📅 Today's Date: {datetime.datetime.now().strftime('%B %d, %Y')}")
    check_due_reminders(current_user['username'])


# ==================== USER MANAGEMENT ====================

def user_login_menu():
    while True:
        clear_screen()
        display_header()
        print("🔐 USER LOGIN")
        print("1. Login")
        print("2. Register New User")
        print("=" * 80)
        choice = input("\n👉 Enter your choice (1-2): ").strip()
        if choice == '1':
            username = login_user()
        elif choice == '2':
            username = register_user()
        else:
            print("\n❌ Invalid choice! Please enter 1 or 2.")
            input("\nPress Enter to continue...")
            continue

        # If login/register failed, loop again
        if not username:
            input("\nPress Enter to continue...")
            continue

        # Build the current_user dict expected by display_user_info()
        users = load_users()
        user_record = users.get(username)
        if user_record:
            return {
                "username": username,
                "name": user_record.get("full_name", username),
                "currency": user_record.get("currency", "USD")
            }
        return {"username": username, "name": username, "currency": "USD"}

def help_menu():
    """Display help and user guide"""
    clear_screen()
    display_header()
    print("\n❓ HELP & USER GUIDE\n")
    print("=" * 80)
    print("\n📖 How to Use Spendlify:\n")
    print("• Add transactions by selecting option 1 from the main menu")
    print("• View your financial dashboard to see summary of income and expenses")
    print("• Set savings goals and track your progress")
    print("• Create budgets for different spending categories")
    print("• Generate reports to analyze your spending patterns")
    print("• Use search and filter to find specific transactions")
    print("\n💡 Tips:")
    print("• Always categorize your transactions for better tracking")
    print("• Review your monthly reports regularly")
    print("• Set realistic budgets and savings goals")
    print("• Back up your data regularly using the export feature")
    print("\n" + "=" * 80)
    input("\nPress Enter to return to main menu...")

def dashboard_summary(current_user):
    clear_screen()
    print("\n📈 DASHBOARD SUMMARY\n")
    pref_cur = current_user.get('currency', 'USD')
    summary = tx.get_user_summary(current_user['username'])
    totals = summary.get(pref_cur, {'income': 0.0, 'expense': 0.0, 'net': 0.0})
    income = totals['income']
    expense = totals['expense']
    net = totals['net']
    top_cats = tx.get_top_categories(current_user['username'], currency=pref_cur, top_n=3)
    cur_symbols = {'USD': '$', 'EUR': '€', 'GBP': '£', 'JPY': '¥', 'EGP': 'E£'}
    sym = cur_symbols.get(pref_cur, '')
    box_w = 62
    def hline():
        print('.' + '-' * (box_w - 2) + '.')
    hline()
    title = f"Dashboard Summary"
    print('|' + title.center(box_w - 2) + '|')
    hline()
    print('| ' + f"User: {current_user['name']}".ljust(box_w - 3) + '|')
    print('| ' + f"Period: {datetime.datetime.now().strftime('%B %Y')}".ljust(box_w - 3) + '|')
    hline()
    # Totals
    print('| ' + 'Total Income:'.ljust(30) + f"{sym}{income:,.2f}".rjust(box_w - 34) + ' |')
    print('| ' + 'Total Expenses:'.ljust(30) + f"{sym}{expense:,.2f}".rjust(box_w - 34) + ' |')
    print('| ' + 'Net Savings:'.ljust(30) + f"{sym}{net:,.2f}".rjust(box_w - 34) + ' |')
    print('|' + ' ' * (box_w - 2) + '|')
    # Current Balance (we use net as balance since there is no stored starting balance)
    print('| ' + 'Current Balance:'.ljust(30) + f"{sym}{net:,.2f}".rjust(box_w - 34) + ' |')
    hline()
    print('\nTop Spending Categories:')
    if not top_cats:
        print('No expense categories found for this currency.')
    else:
        for i, (cat, amt, pct) in enumerate(top_cats, start=1):
            print(f"{i}. {cat.ljust(12)} {sym}{amt:,.2f}    ({pct:.1f}%)")
    print('\n' + '=' * 80)
    input("\nPress Enter to return to main menu...")

def monthly_reports(user):
    today = datetime.datetime.now()
    start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if today.month == 12:
        end_date = today.replace(year=today.year + 1, month=1, day=1) - datetime.timedelta(days=1)
    else:
        end_date = today.replace(month=today.month + 1, day=1) - datetime.timedelta(days=1)
    
    all_transactions = load_transactions()
    monthly_transactions = [
        t for t in all_transactions 
        if t['username'] == user['username'] 
        and start_date <= datetime.datetime.strptime(t['date'], '%Y-%m-%d') <= end_date
    ]

    income = sum(float(t['amount']) for t in monthly_transactions if float(t['amount']) > 0)
    expenses = abs(sum(float(t['amount']) for t in monthly_transactions if float(t['amount']) < 0))
    net_balance = income - expenses

    categories = {}
    for transaction in monthly_transactions:
        category = transaction['category']
        amount = float(transaction['amount'])
        if category not in categories:
            categories[category] = {'total': 0, 'count': 0}
        categories[category]['total'] += amount
        categories[category]['count'] += 1
    
    # Display report
    clear_screen()
    print(f"\n{'=' * 50}")
    print(f"Monthly Report for {user['username']} - {today.strftime('%B %Y')}")
    print(f"{'=' * 50}")
    
    print(f"\nSummary:")
    print(f"{'─' * 30}")
    print(f"Total Income:  ${income:,.2f}")
    print(f"Total Expenses: ${expenses:,.2f}")
    print(f"Net Balance:    ${net_balance:,.2f}")
    
    print(f"\nBreakdown by Category:")
    print(f"{'─' * 50}")
    print(f"{'Category':<20} {'Amount':>10} {'Count':>8}")
    print(f"{'─' * 50}")
    for category, data in sorted(categories.items()):
        print(f"{category:<20} ${data['total']:>9,.2f} {data['count']:>8}")
    
    print(f"\n{'=' * 50}")
    input("\nPress Enter to continue...")

# ==================== MAIN PROGRAM ====================

def main():
    # Login or register
    current_user = user_login_menu()

    while True:
        clear_screen()
        display_user_info(current_user)
        display_main_menu()

        choice = input("\n👉 Enter your choice (1-15): ").strip()

        match choice:
            case '1':
                while True:
                    print ("💳 Transactions:\n1.add\n2.View\n3.edit\n4.delete\n")
                    choice2 = input("\n👉 Enter your choice (1-4): ").strip()
                    match choice2:
                        case '1':
                            tx.add_transaction(current_user['username'])
                            input("\nPress Enter to return to main menu...")
                            break
                        case '2':
                            tx.view_transactions(current_user['username'])
                            input("\nPress Enter to return to main menu...")
                            break
                        case '3':
                            tx.edit_transaction(current_user['username'])
                            input("\nPress Enter to return to main menu...")
                            break
                        case '4':
                            tx.delete_transaction(current_user['username'])
                            input("\nPress Enter to return to main menu...")
                            break
            case '2':
                dashboard_summary(current_user)
            case '3':
                monthly_reports(current_user)
            case '4':
                run_search(current_user['username'])
                input("\nPress Enter to return to main menu...")
            case '5':
                while True:
                    print ("🎯Goals:\n1.add\n2.View\n3.edit\n4.delete\n")
                    choice2 = input("\n👉 Enter your choice (1-4): ").strip()
                    match choice2:
                        case '1':
                            add_goal(current_user['username'])
                            input("\nPress Enter to return to main menu...")
                            break
                        case '2':
                            view_goals(current_user['username'])
                            input("\nPress Enter to return to main menu...")
                            break
                        case '3':
                            edit_goal(current_user['username'])
                            input("\nPress Enter to return to main menu...")
                            break
                        case '4':
                            delete_goal(current_user['username'])
                            input("\nPress Enter to return to main menu...")
                            break
            case '6':
                while True:
                    print ("🔔 Bill Reminder:\n1.add\n2.View\n3.edit\n4.delete\n")
                    choice2 = input("\n👉 Enter your choice (1-4): ").strip()
                    match choice2:
                        case '1':
                            add_reminder(current_user['username'])
                            input("\nPress Enter to return to main menu...")
                            break
                        case '2':
                            view_reminders(current_user['username'])
                            input("\nPress Enter to return to main menu...")
                            break
                        case '3':
                            edit_reminder(current_user['username'])
                            input("\nPress Enter to return to main menu...")
                            break
                        case '4':
                            delete_reminder(current_user['username'])
                            input("\nPress Enter to return to main menu...")
                            break
            case '7':
                current_user = user_login_menu()
            case '8':
                help_menu()
            case '9':
                clear_screen()
                print("\n" + "=" * 80)
                print("✨ Thank you for using Spendlify! ✨".center(80))
                print("💰 Keep tracking, keep saving! 💰".center(80))
                print("=" * 80 + "\n")
                break
            case _:
                print("\n❌ Invalid choice! Please enter a number between 1 and 15.")
                input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()