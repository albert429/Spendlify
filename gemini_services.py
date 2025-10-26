"""gemini_services.py

Lightweight CLI chat assistant adapter for a Gemini-like HTTP API.

Usage:
  - Set environment variables GEMINI_API_KEY and GEMINI_API_URL (the exact endpoint URL)
  - From your `main_menu.py` call:
      from gemini_services import start_gemini_chat_cli
      start_gemini_chat_cli(current_user)

The module will store per-user conversation histories in `data/gemini_histories/<username>.json`.
The HTTP request/response shapes are handled flexibly — adapt `send_to_gemini` if your provider has
an exact contract (you said you'll provide API details later).
"""

import os
import json
import requests
import textwrap

DEFAULT_API_URL = os.getenv("GEMINI_API_URL", "https://api.gemini.example/v1")
API_KEY = os.getenv("GEMINI_API_KEY")
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-1")

HISTORY_DIR = os.path.join("data", "gemini_histories")
os.makedirs(HISTORY_DIR, exist_ok=True)


def _get_headers(api_key: str):
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def _try_post(url: str, payload: dict, headers: dict, timeout: int = 30):
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=timeout)
        resp.raise_for_status()
        return resp
    except requests.RequestException:
        return None


def send_to_gemini(messages, api_url=None, api_key=None, model=None, timeout=30):
    """Send a list of messages to a Gemini-like HTTP chat endpoint.

    messages: list of {"role":"user|assistant|system","content":"..."}
    Returns (True, assistant_text) on success or (False, error_message) on failure.
    """
    api_key = api_key or API_KEY
    if not api_key:
        return False, "Missing GEMINI_API_KEY environment variable."

    api_url = api_url or DEFAULT_API_URL
    model = model or DEFAULT_MODEL

    headers = _get_headers(api_key)

    payload = {"model": model, "messages": messages}

    # Candidate endpoints to try; adapt if you have an exact endpoint
    candidates = [
        api_url,
        api_url.rstrip("/") + "/v1/chat/completions",
        api_url.rstrip("/") + "/v1/chat",
        api_url.rstrip("/") + "/v1/responses",
        api_url.rstrip("/") + "/chat",
    ]

    for url in candidates:
        resp = _try_post(url, payload, headers, timeout=timeout)
        if not resp:
            continue
        try:
            data = resp.json()
        except Exception:
            return False, f"Invalid JSON response from {url}"

        # Common response shapes handling
        # 1) OpenAI-like: {choices:[{message:{content: ...}}]}
        if isinstance(data, dict):
            if "choices" in data and isinstance(data["choices"], list) and data["choices"]:
                choice = data["choices"][0]
                if isinstance(choice, dict):
                    # openai-style
                    msg = choice.get("message")
                    if isinstance(msg, dict) and "content" in msg:
                        return True, msg["content"]
                    # completion text
                    if "text" in choice:
                        return True, choice["text"]

            # 2) Google-like: {output:[{content:[{text:...}]}, ...]}
            if "output" in data:
                out = data["output"]
                if isinstance(out, list) and out:
                    first = out[0]
                    # patterns inside
                    if isinstance(first, dict):
                        # output -> content -> list of pieces with 'text'
                        content = first.get("content")
                        if isinstance(content, list):
                            texts = []
                            for c in content:
                                if isinstance(c, dict) and "text" in c:
                                    texts.append(c["text"])
                            if texts:
                                return True, "\n".join(texts)
                        # maybe first itself has 'text'
                        if "text" in first:
                            return True, first["text"]

            # 3) direct text field
            if "text" in data and isinstance(data["text"], str):
                return True, data["text"]

        # fallback: try to find any string value in JSON
        def _find_text(obj):
            if isinstance(obj, str):
                return obj
            if isinstance(obj, dict):
                for v in obj.values():
                    r = _find_text(v)
                    if r:
                        return r
            if isinstance(obj, list):
                for item in obj:
                    r = _find_text(item)
                    if r:
                        return r
            return None

        t = _find_text(data)
        if t:
            return True, t

    return False, "No working endpoint responded successfully. Check GEMINI_API_URL and GEMINI_API_KEY."


def history_path_for_user(username: str):
    safe = username.replace("/", "_")
    return os.path.join(HISTORY_DIR, f"{safe}.json")


def load_history(username: str):
    path = history_path_for_user(username)
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_history(username: str, messages):
    path = history_path_for_user(username)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Warning: failed to save history: {e}")


def start_gemini_chat_cli(current_user: dict):
    """Start an interactive CLI chat session for the given user.

    current_user must be a dict containing at least 'username' and optionally 'name'.
    """
    username = current_user.get("username") if isinstance(current_user, dict) else str(current_user)
    display_name = current_user.get("name", username) if isinstance(current_user, dict) else username

    print("\n=== Gemini CLI Assistant ===")
    print(f"User: {display_name} ({username})")
    print("Type your message and press Enter. Commands: /exit, /clear, /history, /reset, /help")

    # Load previous conversation
    conv = load_history(username)
    if not conv:
        # Seed with a gentle system prompt
        conv = [
            {"role": "system", "content": "You are a helpful assistant integrated into Spendlify, a personal finance manager. Keep answers concise and friendly."}
        ]

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting chat.")
            save_history(username, conv)
            break

        if not user_input:
            continue

        if user_input.startswith("/"):
            cmd = user_input.lower()
            if cmd == "/exit":
                save_history(username, conv)
                print("Conversation saved. Goodbye.")
                break
            if cmd == "/clear":
                try:
                    os.system('cls' if os.name == 'nt' else 'clear')
                except Exception:
                    pass
                continue
            if cmd == "/history":
                print("\n--- Conversation history (last 20) ---")
                for m in conv[-20:]:
                    role = m.get("role", "?")
                    print(f"[{role}] {m.get('content')}")
                print("--- end ---\n")
                continue
            if cmd == "/reset":
                conv = [conv[0]] if conv else []
                save_history(username, conv)
                print("Conversation reset (system prompt preserved).")
                continue
            if cmd == "/help":
                print("Commands: /exit (save & exit), /clear (clear screen), /history (show recent), /reset (clear convo)")
                continue
            print("Unknown command. Type /help for commands.")
            continue

        # append user message
        conv.append({"role": "user", "content": user_input})

        # Send to Gemini-like API
        ok, resp = send_to_gemini(conv)
        if not ok:
            print(f"Error: {resp}")
            # do not append assistant if failed; allow retry
            continue

        assistant_text = resp if isinstance(resp, str) else str(resp)
        # Save assistant message
        conv.append({"role": "assistant", "content": assistant_text})

        # Persist history
        save_history(username, conv)

        # Print nicely
        print("\nAssistant:")
        for paragraph in assistant_text.split("\n\n"):
            print(textwrap.fill(paragraph, width=80))
            print()


if __name__ == "__main__":
    # quick local runner
    dummy = {"username": "local", "name": "Local User"}
    start_gemini_chat_cli(dummy)
