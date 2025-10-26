import os
import requests
import datetime
from dotenv import load_dotenv
from transactions import load_transactions
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def ask_gemini(question, current_user):
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": API_KEY
    }

    # Load user's transactions
    all_transactions = load_transactions()
    user_transactions = [tx for tx in all_transactions if tx['username'] == current_user['username']]

    # Create context with user info and transactions
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    context = f"""Current date: {current_date}
    User: {current_user['username']}
    Recent transactions:
    """
    # Add last 5 transactions to context
    for tx in user_transactions[-5:]:
        context += f"- {tx['date']}: {tx['amount']} {tx['currency']} for {tx['category']}\n"

    # Combine context with user's question
    full_prompt = f"""{context}
    User's question: {question}"""

    # Prepare the message in Gemini's format
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": full_prompt
                    }
                ]
            }
        ]
    }

    try:
        # Send request to Gemini
        response = requests.post(
            API_URL,
            headers=headers,
            json=data
        )
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse the response
        result = response.json()
        
        # Get the answer text from the response
        answer = result["candidates"][0]["content"]["parts"][0]["text"]
        return answer

    except requests.RequestException as e:
        return f"Error connecting to Gemini: {str(e)}"
    except KeyError as e:
        return f"Error parsing Gemini response: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

def main(current_user=None):
    print("Simple Gemini Chat")
    print("Type 'exit' to quit")
    print("-" * 30)

    # Create a test user for demo purposes
    test_user = {
        "username": "test_user",
        "name": "Test User"
    }

    while True:
        # Get user's question
        question = input("\nYour question: ")
        
        # Check if user wants to exit
        if question.lower() == 'exit':
            print("Goodbye!")
            break
        
        # Skip empty questions
        if not question.strip():
            continue
        
        # Get and print Gemini's response
        print("\nGemini's answer:")
        print(ask_gemini(question, current_user))

if __name__ == "__main__":
    main()