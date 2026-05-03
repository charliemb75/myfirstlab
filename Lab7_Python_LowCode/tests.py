from product_generator_refactored import validate_product_data, create_product_prompt, parse_api_response, format_output, load_image_as_base64, build_image_payload
from product_generator_refactored import ProductListing
import pandas as pd

# =========================
# TEST: validate_product_data
# =========================

valid_data = {
    "title": "Test Product",
    "description": "This is a test description",
    "features": ["Feature 1", "Feature 2"],
    "keywords": ["test, product"]
}

invalid_data = {
    "title": "Missing fields"
}

print("\n--- validate_product_data ---")

try:
    result = validate_product_data(valid_data)
    print("✓ Valid data passed:", result)
except Exception as e:
    print("✗ Valid data failed:", e)

try:
    validate_product_data(invalid_data)
    print("✗ Invalid data should have failed")
except Exception as e:
    print("✓ Invalid data correctly failed:", e)


# =========================
# TEST: create_product_prompt
# =========================

print("\n--- create_product_prompt ---")

product = {
    "productDisplayName": "Cool Sneakers",
    "masterCategory": "Footwear",
    "subCategory": "Shoes",
    "articleType": "Sneakers",
    "baseColour": "White"
}

prompt = create_product_prompt(product)

print("Prompt preview:")
print(prompt[:200])

assert "Cool Sneakers" in prompt
print("✓ Prompt contains product info")

# =========================
# TEST: parse_api_response
# =========================

print("\n--- parse_api_response ---")

valid_json = '{"title": "Test", "description": "Desc", "features": ["A"], "keywords": ["x"]}'
invalid_json = 'Not JSON'

try:
    parsed = parse_api_response(valid_json)
    print("✓ Parsed JSON:", parsed)
except Exception as e:
    print("✗ Should not fail:", e)

try:
    parse_api_response(invalid_json)
    print("✗ Invalid JSON should fail")
except Exception as e:
    print("✓ Correctly failed:", e)

# =========================
# TEST: format_output
# =========================

print("\n--- format_output ---")

product = {"id": 1, "productDisplayName": "Test Product"}

listing = ProductListing(
    title="Title",
    description="Desc",
    features=["A", "B"],
    keywords=["x, y"]
)

formatted = format_output(product, listing)

print(formatted)

assert formatted["id"] == 1
assert "listing" in formatted
print("✓ Output formatted correctly")

# =========================
# TEST: image encoding
# =========================

print("\n--- load_image_as_base64 ---")

from PIL import Image

# Create dummy image
img = Image.new("RGB", (10, 10), color="red")

row = pd.Series({"id": 1, "image": img})

try:
    b64 = load_image_as_base64(row)
    print("✓ Image encoded, length:", len(b64))
except Exception as e:
    print("✗ Image encoding failed:", e)

# =========================
# TEST: build_image_payload
# =========================

print("\n--- build_image_payload ---")

payload = build_image_payload("abc123")

print(payload)

assert payload["type"] == "image_url"
assert "data:image/png;base64,abc123" in payload["image_url"]["url"]
print("✓ Payload correct")