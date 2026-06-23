"""
test_key.py — Step 0 checkpoint: verify your Anthropic API key works.

Run:
    source venv/bin/activate
    python test_key.py

The API key is loaded from .env (see python-dotenv below).
Copy .env.example → .env and paste your key — never commit .env to git.

What this file does:
    Sends one short message to Claude and prints the reply.
    If you see a friendly sentence, your setup (venv + API key + anthropic SDK) is good.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# load_dotenv()
# ---------------------------------------------------------------------------
# Reads key=value pairs from a .env file in the project root and injects
# them into os.environ — as if you had run `export ANTHROPIC_API_KEY=...`.
#
# Why .env instead of hardcoding or shell export?
#   - one place for secrets on your machine
#   - .env is in .gitignore so it never gets pushed to GitHub
#   - same pattern used in production (Docker, cloud deploys, etc.)
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

# ---------------------------------------------------------------------------
# import anthropic
# ---------------------------------------------------------------------------
# Official Anthropic Python SDK — wraps their HTTP API so you call
# client.messages.create(...) instead of hand-building JSON + requests.
import anthropic


# ---------------------------------------------------------------------------
# client = anthropic.Anthropic()
# ---------------------------------------------------------------------------
# Creates a client that talks to https://api.anthropic.com.
# After load_dotenv(), ANTHROPIC_API_KEY is in the environment and the
# SDK picks it up automatically (sent as Authorization: Bearer <key>).
client = anthropic.Anthropic()


# ---------------------------------------------------------------------------
# client.messages.create(...)
# ---------------------------------------------------------------------------
# Core chat call: send messages in, get a model reply out.
#
#   model       — which Claude version (speed/cost/capability trade-off)
#   max_tokens  — max length of the reply (cost + safety cap)
#   messages    — conversation turns: list of {"role", "content"} dicts
#
# This is a zero-shot prompt: one user message, no examples in the prompt.
msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=100,
    messages=[
        {"role": "user", "content": "Say hello in one short sentence."}
    ],
)


# ---------------------------------------------------------------------------
# print(msg.content[0].text)
# ---------------------------------------------------------------------------
# Response shape: msg.content is a list of blocks (usually text).
# For simple replies, read the first text block: msg.content[0].text
#
# You'll reuse this pattern in rag.py (Step 5).
print(msg.content[0].text)
