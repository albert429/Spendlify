from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
from functools import wraps
from datetime import datetime
import csv
import io
from flask import send_file
import uuid

# Import your existing modules
from auth import login_user, register_user, logout_user, load_session, save_session
from transactions import (
    add_transaction,
    view_transactions,
    delete_transaction,
    edit_transaction,
    get_user_summary,
    get_top_categories,
)
from goals import add_goal, view_goals, delete_goal, edit_goal
from bill_reminders import (
    add_reminder,
    view_reminders,
    delete_reminder,
    edit_reminder,
    check_due_reminders,
)
from data_handler import (
    load_transactions,
    load_users,
    load_goals,
    load_reminders,
    save_transactions,
    import_transactions,
    export_transactions,
)
from search import search_transactions
from simple_gemini import ask_gemini

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Change this to a fixed secret key in production


# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


# Routes
@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        # Temporarily store credentials for validation
        import getpass
        import sys
        from io import StringIO

        # Mock the input functions
        old_input = __builtins__.input
        old_getpass = getpass.getpass

        inputs = iter([username, password])
        __builtins__.input = lambda _: next(inputs)
        getpass.getpass = lambda _: next(inputs)

        # Capture output
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        result = login_user()

        # Restore
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        __builtins__.input = old_input
        getpass.getpass = old_getpass

        if result:
            session["username"] = result
            users = load_users()
            user_data = users.get(result, {})
            return jsonify(
                {
                    "success": True,
                    "username": result,
                    "name": user_data.get("full_name", result),
                    "currency": user_data.get("currency", "USD"),
                }
            )
        else:
            return jsonify({"success": False, "message": "Invalid credentials"}), 401

    return render_template("login.html")


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    full_name = data.get("full_name")
    username = data.get("username")
    currency = data.get("currency")
    password = data.get("password")

    users = load_users()

    # Validation
    if username in users:
        return jsonify({"success": False, "message": "Username already exists"}), 400

    # Create user (simplified version - you may want to use your register_user function)
    from auth import hash_password
    import uuid

    users[username] = {
        "user_id": str(uuid.uuid4()),
        "full_name": full_name,
        "password_hash": hash_password(password),
        "currency": currency,
    }

    from data_handler import save_users

    save_users(users)

    return jsonify({"success": True, "message": "Registration successful"})


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    username = session.get("username")
    users = load_users()
    user_data = users.get(username, {})

    return render_template(
        "dashboard.html",
        username=username,
        full_name=user_data.get("full_name", username),
        currency=user_data.get("currency", "USD"),
    )


# API Routes
@app.route("/api/summary")
@login_required
def api_summary():
    username = session.get("username")
    summary = get_user_summary(username)

    users = load_users()
    user_data = users.get(username, {})
    currency = user_data.get("currency", "USD")

    totals = summary.get(currency, {"income": 0.0, "expense": 0.0, "net": 0.0})
    top_cats = get_top_categories(username, currency=currency, top_n=5)

    return jsonify(
        {
            "income": totals["income"],
            "expense": totals["expense"],
            "net": totals["net"],
            "currency": currency,
            "top_categories": [
                {"category": c[0], "amount": c[1], "percent": c[2]} for c in top_cats
            ],
        }
    )


@app.route("/api/transactions", methods=["GET"])
@login_required
def api_get_transactions():
    username = session.get("username")
    transactions = load_transactions()
    user_transactions = [t for t in transactions if t["username"] == username]
    return jsonify(user_transactions)


@app.route("/api/transactions", methods=["POST"])
@login_required
def api_add_transaction():
    username = session.get("username")
    data = request.get_json()

    import uuid

    transaction = {
        "id": str(uuid.uuid4()),
        "username": username,
        "amount": float(data["amount"]),
        "currency": data["currency"],
        "category": data["category"],
        "date": data["date"],
        "description": data["description"],
        "type": data["type"],
        "payment": data["payment"],
    }

    transactions = load_transactions()
    transactions.append(transaction)
    save_transactions(transactions)

    return jsonify({"success": True, "transaction": transaction})


@app.route("/api/transactions/<transaction_id>", methods=["DELETE"])
@login_required
def api_delete_transaction(transaction_id):
    username = session.get("username")
    transactions = load_transactions()

    transaction = next(
        (
            t
            for t in transactions
            if t["id"] == transaction_id and t["username"] == username
        ),
        None,
    )

    if transaction:
        transactions.remove(transaction)
        save_transactions(transactions)
        return jsonify({"success": True})

    return jsonify({"success": False, "message": "Transaction not found"}), 404


@app.route("/api/transactions/<transaction_id>", methods=["PUT"])
@login_required
def api_edit_transaction(transaction_id):
    username = session.get("username")
    data = request.get_json()
    transactions = load_transactions()

    transaction = next(
        (
            t
            for t in transactions
            if t["id"] == transaction_id and t["username"] == username
        ),
        None,
    )

    if transaction:
        transaction.update(
            {
                "amount": float(data.get("amount", transaction["amount"])),
                "currency": data.get("currency", transaction["currency"]),
                "category": data.get("category", transaction["category"]),
                "date": data.get("date", transaction["date"]),
                "description": data.get("description", transaction["description"]),
                "type": data.get("type", transaction["type"]),
                "payment": data.get("payment", transaction["payment"]),
            }
        )
        save_transactions(transactions)
        return jsonify({"success": True, "transaction": transaction})

    return jsonify({"success": False, "message": "Transaction not found"}), 404


@app.route("/api/goals", methods=["GET"])
@login_required
def api_get_goals():
    username = session.get("username")
    goals = load_goals()
    user_goals = [g for g in goals if g["username"] == username]
    return jsonify(user_goals)


@app.route("/api/goals", methods=["POST"])
@login_required
def api_add_goal():
    username = session.get("username")
    data = request.get_json()

    import uuid

    status = (
        "completed"
        if float(data["current_amount"]) >= float(data["target_amount"])
        else "active"
    )

    goal = {
        "id": str(uuid.uuid4()),
        "username": username,
        "title": data["title"],
        "target_amount": float(data["target_amount"]),
        "current_amount": float(data["current_amount"]),
        "deadline": data["deadline"],
        "status": status,
    }

    from data_handler import save_goals

    goals = load_goals()
    goals.append(goal)
    save_goals(goals)

    return jsonify({"success": True, "goal": goal})


@app.route("/api/goals/<goal_id>", methods=["DELETE"])
@login_required
def api_delete_goal(goal_id):
    username = session.get("username")
    goals = load_goals()

    goal = next(
        (g for g in goals if g["id"] == goal_id and g["username"] == username), None
    )

    if goal:
        from data_handler import save_goals

        goals.remove(goal)
        save_goals(goals)
        return jsonify({"success": True})

    return jsonify({"success": False, "message": "Goal not found"}), 404


@app.route("/api/goals/<goal_id>", methods=["PUT"])
@login_required
def api_edit_goal(goal_id):
    username = session.get("username")
    data = request.get_json()
    goals = load_goals()

    goal = next(
        (g for g in goals if g["id"] == goal_id and g["username"] == username), None
    )

    if goal:
        # Calculate new status
        current_amount = float(data.get("current_amount", goal["current_amount"]))
        target_amount = float(data.get("target_amount", goal["target_amount"]))
        status = "completed" if current_amount >= target_amount else "active"

        goal.update(
            {
                "title": data.get("title", goal["title"]),
                "target_amount": target_amount,
                "current_amount": current_amount,
                "deadline": data.get("deadline", goal["deadline"]),
                "status": status,
            }
        )

        from data_handler import save_goals

        save_goals(goals)
        return jsonify({"success": True, "goal": goal})

    return jsonify({"success": False, "message": "Goal not found"}), 404


@app.route("/api/reminders", methods=["GET"])
@login_required
def api_get_reminders():
    username = session.get("username")
    reminders = load_reminders()
    user_reminders = [r for r in reminders if r["username"] == username]
    return jsonify(user_reminders)


@app.route("/api/reminders", methods=["POST"])
@login_required
def api_add_reminder():
    username = session.get("username")
    data = request.get_json()

    import uuid

    reminder = {
        "id": str(uuid.uuid4()),
        "username": username,
        "title": data["title"],
        "amount": float(data["amount"]),
        "deadline": data["deadline"],
    }

    from data_handler import save_reminders

    reminders = load_reminders()
    reminders.append(reminder)
    save_reminders(reminders)

    return jsonify({"success": True, "reminder": reminder})


@app.route("/api/reminders/<reminder_id>", methods=["PUT"])
@login_required
def api_edit_reminder(reminder_id):
    username = session.get("username")
    data = request.get_json()
    reminders = load_reminders()

    reminder = next(
        (r for r in reminders if r["id"] == reminder_id and r["username"] == username),
        None,
    )

    if reminder:
        reminder.update(
            {
                "title": data.get("title", reminder["title"]),
                "amount": float(data.get("amount", reminder["amount"])),
                "deadline": data.get("deadline", reminder["deadline"]),
            }
        )

        from data_handler import save_reminders

        save_reminders(reminders)
        return jsonify({"success": True, "reminder": reminder})

    return jsonify({"success": False, "message": "Reminder not found"}), 404


@app.route("/api/reminders/<reminder_id>", methods=["DELETE"])
@login_required
def api_delete_reminder(reminder_id):
    username = session.get("username")
    reminders = load_reminders()

    reminder = next(
        (r for r in reminders if r["id"] == reminder_id and r["username"] == username),
        None,
    )

    if reminder:
        from data_handler import save_reminders

        reminders.remove(reminder)
        save_reminders(reminders)
        return jsonify({"success": True})

    return jsonify({"success": False, "message": "Reminder not found"}), 404


@app.route("/api/ai/chat", methods=["POST"])
@login_required
def api_ai_chat():
    username = session.get("username")
    data = request.get_json()
    question = data.get("question")

    users = load_users()
    user_data = users.get(username, {})
    current_user = {
        "username": username,
        "name": user_data.get("full_name", username),
        "currency": user_data.get("currency", "USD"),
    }

    response = ask_gemini(question, current_user)
    return jsonify({"response": response})


# CSV Import Route - FIXED
@app.route("/api/transactions/import", methods=["POST"])
@login_required
def api_import_transactions():
    username = session.get("username")

    if "file" not in request.files:
        return jsonify({"success": False, "message": "No file provided"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"success": False, "message": "No file selected"}), 400

    if not file.filename.endswith(".csv"):
        return jsonify({"success": False, "message": "File must be a CSV"}), 400

    try:
        # Read the CSV file
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.DictReader(stream)

        transactions = load_transactions()
        imported_count = 0
        errors = []

        for row_num, row in enumerate(csv_reader, start=2):
            try:
                # Validate required fields
                required_fields = [
                    "amount",
                    "currency",
                    "category",
                    "date",
                    "description",
                    "type",
                    "payment",
                ]
                missing_fields = [
                    field
                    for field in required_fields
                    if field not in row or not row[field]
                ]

                if missing_fields:
                    errors.append(
                        f"Row {row_num}: Missing fields: {', '.join(missing_fields)}"
                    )
                    continue

                # Validate amount
                try:
                    amount = float(row["amount"])
                    if amount <= 0:
                        errors.append(f"Row {row_num}: Amount must be greater than 0")
                        continue
                except ValueError:
                    errors.append(f"Row {row_num}: Invalid amount value")
                    continue

                # Validate date format
                try:
                    datetime.strptime(row["date"], "%Y-%m-%d")
                except ValueError:
                    errors.append(
                        f"Row {row_num}: Invalid date format (use YYYY-MM-DD)"
                    )
                    continue

                # Validate type
                if row["type"].lower() not in ["income", "expense"]:
                    errors.append(f"Row {row_num}: Type must be 'income' or 'expense'")
                    continue

                # Create transaction
                transaction = {
                    "id": str(uuid.uuid4()),
                    "username": username,
                    "amount": amount,
                    "currency": row["currency"].upper(),
                    "category": row["category"],
                    "date": row["date"],
                    "description": row["description"],
                    "type": row["type"].lower(),
                    "payment": row["payment"],
                }

                transactions.append(transaction)
                imported_count += 1

            except Exception as e:
                errors.append(f"Row {row_num}: {str(e)}")
                continue

        # Save transactions
        if imported_count > 0:
            save_transactions(transactions)

        response_data = {
            "success": True,
            "count": imported_count,
            "message": f"Successfully imported {imported_count} transactions",
        }

        if errors:
            response_data["warnings"] = errors[:10]  # Limit to first 10 errors

        return jsonify(response_data)

    except Exception as e:
        print(f"Import error: {e}")
        return (
            jsonify({"success": False, "message": f"Error importing file: {str(e)}"}),
            500,
        )


# CSV Export Route - FIXED
@app.route("/api/transactions/export", methods=["GET"])
@login_required
def api_export_transactions():
    username = session.get("username")

    try:
        transactions = load_transactions()
        user_transactions = [t for t in transactions if t["username"] == username]

        if not user_transactions:
            return (
                jsonify({"success": False, "message": "No transactions to export"}),
                404,
            )

        # Create CSV in memory
        output = io.StringIO()
        fieldnames = [
            "amount",
            "currency",
            "category",
            "date",
            "description",
            "type",
            "payment",
        ]
        writer = csv.DictWriter(output, fieldnames=fieldnames)

        writer.writeheader()
        for tx in user_transactions:
            writer.writerow(
                {
                    "amount": tx["amount"],
                    "currency": tx["currency"],
                    "category": tx["category"],
                    "date": tx["date"],
                    "description": tx["description"],
                    "type": tx["type"],
                    "payment": tx["payment"],
                }
            )

        # Convert to bytes for download
        output.seek(0)
        
        # Create response with proper headers
        from flask import Response
        
        response = Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename={username}_transactions_{datetime.now().strftime('%Y%m%d')}.csv"
            }
        )
        
        return response

    except Exception as e:
        print(f"Export error: {e}")
        return (
            jsonify(
                {"success": False, "message": f"Error exporting transactions: {str(e)}"}
            ),
            500,
        )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
