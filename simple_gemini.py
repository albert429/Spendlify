import os
import requests
from dotenv import load_dotenv

# Load the .env file from the current directory
load_dotenv()

# Get API key from .env file
API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def ask_gemini(question):
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": API_KEY
    }

    # Prepare the message in Gemini's format
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": question
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

def main():
    print("Simple Gemini Chat")
    print("Type 'exit' to quit")
    print("-" * 30)

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
        print(ask_gemini(question))

if __name__ == "__main__":
    main()