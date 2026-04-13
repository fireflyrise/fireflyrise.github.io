"""
Gemini API Key Validator
========================
Checks that:
  1. A .env file exists in the current directory
  2. GEMINI_API_KEY is present in the .env file
  3. The key is not a placeholder value
  4. The key is active by making a lightweight test call to the Gemini API

Usage:
    python scripts/validate_env.py

Requirements:
    pip install google-genai python-dotenv
"""

import os
import sys
from pathlib import Path

# ── Check .env file exists ─────────────────────────────────────────────────
env_path = Path(".env")
if not env_path.exists():
    print("❌ .env file not found in the current directory.")
    print()
    print("   Create a file named .env in your project folder with this content:")
    print("   GEMINI_API_KEY=AIzaSy...your_key_here")
    print()
    print("   Get a free API key at: https://aistudio.google.com/apikey")
    sys.exit(1)

print("✅ .env file found.")

# ── Load and check key presence ────────────────────────────────────────────
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ GEMINI_API_KEY is missing from your .env file.")
    print()
    print("   Add this line to your .env file:")
    print("   GEMINI_API_KEY=AIzaSy...your_key_here")
    sys.exit(1)

# ── Check for placeholder values ───────────────────────────────────────────
placeholders = [
    "your_api_key_here",
    "your_key_here",
    "AIzaSyXXXX",
    "INSERT_KEY",
    "REPLACE_ME",
    "sk-",
]
if any(p.lower() in api_key.lower() for p in placeholders) or len(api_key) < 20:
    print("❌ GEMINI_API_KEY looks like a placeholder, not a real key.")
    print()
    print("   Replace it with your actual key from: https://aistudio.google.com/apikey")
    sys.exit(1)

print("✅ GEMINI_API_KEY found in .env.")

# ── Live API test ──────────────────────────────────────────────────────────
print("   Testing API key with a live call...")

try:
    from google import genai

    client = genai.Client(api_key=api_key)

    # Lightweight text call — costs nothing, confirms key is active
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Reply with only the word: OK",
    )

    reply = response.text.strip() if response.text else ""
    if reply:
        print("✅ API key is valid and active.")
        print()
        print("   You're ready to generate images. Run:")
        print("   python scripts/generate_images.py scripts/images_manifest.json")
    else:
        print("⚠️  API responded but returned no text. Key may be valid — try running the image generator.")

except Exception as e:
    error_msg = str(e).lower()

    if "api_key_invalid" in error_msg or "invalid" in error_msg:
        print("❌ API key is invalid or has been revoked.")
        print()
        print("   Generate a new key at: https://aistudio.google.com/apikey")

    elif "quota" in error_msg or "billing" in error_msg or "rate" in error_msg:
        print("⚠️  API key is valid but billing or quota issue detected.")
        print()
        print("   Image generation requires a billing account.")
        print("   Check: https://aistudio.google.com/apikey")

    elif "permission" in error_msg or "403" in error_msg:
        print("⚠️  API key exists but may not have image generation permissions enabled.")
        print()
        print("   Verify the key has the Gemini API enabled in Google AI Studio.")

    else:
        print(f"❌ API call failed: {e}")
        print()
        print("   Check your internet connection and try again.")

    sys.exit(1)
