"""
Website Image Generator — Google Gemini (model resolved at build time)
=======================================================================
Reads IMAGES_MANIFEST (a JSON file defining every image needed for the site)
and generates each one using the Gemini image model specified in the manifest.

All images are converted to WebP format and compressed before saving.
WebP is smaller and faster than JPEG/PNG for web delivery.

The model name is NOT hardcoded here — it is set in images_manifest.json
by Claude after searching ai.google.dev for the current best model.

Usage:
    python scripts/generate_images.py scripts/images_manifest.json

Output:
    All images saved to the images/ folder in WebP format (.webp extension).

Requirements:
    pip install google-genai pillow python-dotenv

.env file (project root, same level as index.html):
    GEMINI_API_KEY=your_api_key_here
"""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from PIL import Image

# ── Load API key from .env ─────────────────────────────────────────────────
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("ERROR: GEMINI_API_KEY not found in .env file.")
    print("Run: python scripts/validate_env.py")
    sys.exit(1)

# ── Load manifest (model name lives here) ─────────────────────────────────
if len(sys.argv) < 2:
    print("Usage: python scripts/generate_images.py scripts/images_manifest.json")
    sys.exit(1)

manifest_path = Path(sys.argv[1])
if not manifest_path.exists():
    print(f"ERROR: Manifest file not found: {manifest_path}")
    sys.exit(1)

with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

# ── Resolve model from manifest ────────────────────────────────────────────
MODEL = manifest.get("model", "").strip()
if not MODEL or "REPLACE_WITH" in MODEL:
    print("ERROR: No valid 'model' key in manifest.")
    print("Claude must search ai.google.dev for the current Gemini image model")
    print("and set the 'model' field in images_manifest.json before running this.")
    print("Reference: https://ai.google.dev/gemini-api/docs/models")
    sys.exit(1)

# ── WebP compression settings ──────────────────────────────────────────────
# quality=82: visually lossless at normal viewing, ~30-50% smaller than JPEG
# method=6:   maximum compression effort (slower but smaller files)
WEBP_QUALITY = 82
WEBP_METHOD  = 6

# ── Gemini client ──────────────────────────────────────────────────────────
from google import genai
from google.genai import types

client = genai.Client(api_key=api_key)

# ── Output folder ──────────────────────────────────────────────────────────
OUTPUT_DIR = Path("images")
OUTPUT_DIR.mkdir(exist_ok=True)

# ── Force .webp extension on all output filenames ─────────────────────────
def to_webp_filename(filename):
    return Path(filename).stem + ".webp"

# ── Generate each image ────────────────────────────────────────────────────
images = manifest.get("images", [])
print(f"\nGenerating {len(images)} images")
print(f"Model   : {MODEL}")
print(f"Format  : WebP (quality={WEBP_QUALITY}, method={WEBP_METHOD})")
print(f"Output  : {OUTPUT_DIR}/\n")

success_count = 0
fail_count    = 0

for idx, item in enumerate(images, 1):
    webp_filename = to_webp_filename(item["filename"])
    prompt        = item["prompt"]
    aspect        = item.get("aspect_ratio", "16:9")
    resolution    = item.get("resolution", "1K")
    output_path   = OUTPUT_DIR / webp_filename

    print(f"[{idx}/{len(images)}] {webp_filename}")
    print(f"Prompt : {prompt[:90]}...")

    try:
        # Call Gemini API
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio=aspect,
                    image_size=resolution,
                ),
            ),
        )

        # Extract PIL image from response
        pil_image = None
        for part in response.parts:
            pil_image = part.as_image()
            if pil_image:
                break

        if pil_image is None:
            print(f"WARNING: No image returned for {webp_filename} — skipping\n")
            fail_count += 1
            continue

        # WebP requires RGB mode — convert if needed
        # Flatten any transparency onto a white background
        if pil_image.mode in ("RGBA", "P", "LA"):
            background = Image.new("RGB", pil_image.size, (255, 255, 255))
            if pil_image.mode == "P":
                pil_image = pil_image.convert("RGBA")
            mask = pil_image.split()[-1] if pil_image.mode in ("RGBA", "LA") else None
            background.paste(pil_image, mask=mask)
            pil_image = background
        elif pil_image.mode != "RGB":
            pil_image = pil_image.convert("RGB")

        # Save as compressed WebP
        pil_image.save(
            str(output_path),
            format="WEBP",
            quality=WEBP_QUALITY,
            method=WEBP_METHOD,
        )

        file_kb = output_path.stat().st_size / 1024
        print(f"Saved  : {output_path} ({file_kb:.0f} KB)\n")
        success_count += 1

    except Exception as e:
        print(f"ERROR  : {e}\n")
        fail_count += 1

# ── Summary ────────────────────────────────────────────────────────────────
print("-" * 50)
print(f"Generated : {success_count} images")
if fail_count:
    print(f"Failed    : {fail_count} images")
print(f"Location  : {OUTPUT_DIR.resolve()}")
print()
print("NOTE: All HTML/CSS references must use .webp filenames.")
print("      The skill generates <img> tags with .webp already.")
print("-" * 50)
