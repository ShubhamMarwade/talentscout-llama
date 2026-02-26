import os
import json
import re
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

TOKEN_LIMITS = {
    "questions": 700,
    "evaluation": 500,
    "default": 400,
}


def safe_json_extract(text: str):
    """Extract JSON from LLM output safely — never raises."""
    if not text:
        return None

    text = text.strip()

    # Strip markdown code fences
    cleaned = re.sub(r"^```(?:json)?\s*", "", text)
    cleaned = re.sub(r"\s*```$", "", cleaned).strip()

    # Strategy 1: direct parse
    for attempt in (cleaned, text):
        try:
            return json.loads(attempt)
        except Exception:
            pass

    # Strategy 2: first {...} block
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if m:
        candidate = re.sub(r",\s*([\]}])", r"\1", m.group())
        try:
            return json.loads(candidate)
        except Exception:
            pass

    # Strategy 3: first [...] block
    m = re.search(r"$$.*$$", text, re.DOTALL)
    if m:
        candidate = re.sub(r",\s*([\]}])", r"\1", m.group())
        try:
            return json.loads(candidate)
        except Exception:
            pass

    # Strategy 4: single quotes → double quotes
    try:
        return json.loads(text.replace("'", '"'))
    except Exception:
        pass

    return None


def _stream_ollama(payload: dict) -> str:
    """POST to Ollama with stream=True and collect all token chunks."""
    CONNECT_TIMEOUT = 15
    CHUNK_TIMEOUT = 300

    url = f"{OLLAMA_HOST}/api/chat"
    payload = {**payload, "stream": True}

    r = requests.post(
        url,
        json=payload,
        stream=True,
        timeout=(CONNECT_TIMEOUT, CHUNK_TIMEOUT),
    )
    r.raise_for_status()

    parts = []
    for raw_line in r.iter_lines():
        if not raw_line:
            continue
        try:
            chunk = json.loads(raw_line)
        except Exception:
            continue

        delta = chunk.get("message", {}).get("content", "")
        if delta:
            parts.append(delta)

        if chunk.get("done"):
            break

    return "".join(parts)


def chat_completion(
    system: str,
    user: str,
    response_format: str = "text",
    num_predict: int | None = None,
    _token_key: str = "default",
) -> dict | str:
    """Call Ollama and return parsed JSON (dict) or plain text (str)."""
    if num_predict is None:
        num_predict = TOKEN_LIMITS.get(_token_key, TOKEN_LIMITS["default"])

    payload = {
        "model": OLLAMA_MODEL,
        "keep_alive": "10m",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "options": {
            "temperature": 0.2,
            "num_predict": num_predict,
        },
    }

    if response_format == "json":
        payload["format"] = "json"

    try:
        content = _stream_ollama(payload)
    except requests.exceptions.ConnectionError:
        print(f"⚠️  Cannot connect to Ollama at {OLLAMA_HOST}. Is it running?")
        return {} if response_format == "json" else ""
    except requests.exceptions.Timeout:
        print("⚠️  Ollama timed out — model produced no output for 5 minutes.")
        return {} if response_format == "json" else ""
    except Exception as e:
        print(f"⚠️  Ollama request failed: {e}")
        return {} if response_format == "json" else ""

    if response_format == "json":
        parsed = safe_json_extract(content)
        if parsed is None:
            print("⚠️  Model returned non-JSON output:")
            print(content[:600])
            return {}
        return parsed

    return content