import os
import json
import base64
from io import BytesIO
from pathlib import Path
from typing import List, Dict, Any

import pandas as pd
from dotenv import load_dotenv
from datasets import load_dataset
from PIL import Image
from pydantic import BaseModel, ValidationError
from cohere import Client


# =========================
# CONFIG
# =========================

class Config:
    MODEL = "command-r7b-12-2024"
    DATASET_NAME = "ashraq/fashion-product-images-small"
    DATASET_SPLIT = "train[:100]"
    OUTPUT_FILE = "Lab7_Python_LowCode/product_listings.json"


# =========================
# MODELS (Validation)
# =========================

class ProductListing(BaseModel):
    title: str
    description: str
    features: List[str]
    keywords: List[str]


# =========================
# ENV / CLIENT
# =========================

def init_client() -> Client:
    try:
        load_dotenv()
        api_key = os.getenv("COHERE_API_KEY")

        if not api_key:
            raise ValueError("COHERE_API_KEY is missing in environment variables.")

        return Client(api_key=api_key)
    except Exception as e:
        error_msg = (
            f"ERROR in init_client(): {type(e).__name__}\n"
            f"  Location: d:\\Documents\\Bootcamp\\4_Labs\\Lab7_Python_LowCode\\product_generator_refactored.py, line ~32\n"
            f"  Message: {str(e)}\n"
            f"  Suggestion: Ensure COHERE_API_KEY is set in .env file or environment variables. Check if .env file exists and is in the correct directory."
        )
        print(error_msg)
        raise


# =========================
# DATA LOADING
# =========================

def load_products() -> pd.DataFrame:
    try:
        dataset = load_dataset(Config.DATASET_NAME, split=Config.DATASET_SPLIT)
        df = pd.DataFrame(dataset)
        print(f"✓ Loaded dataset with {len(df)} rows")
        return df
    except Exception as e:
        error_msg = (
            f"ERROR in load_products(): {type(e).__name__}\n"
            f"  Location: d:\\Documents\\Bootcamp\\4_Labs\\Lab7_Python_LowCode\\product_generator_refactored.py, line ~55\n"
            f"  Message: {str(e)}\n"
            f"  Suggestion: Check internet connection and dataset name '{Config.DATASET_NAME}'. Ensure 'datasets' library is installed. Verify dataset split '{Config.DATASET_SPLIT}' is valid."
        )
        print(error_msg)
        return create_fallback_dataset()


def create_fallback_dataset() -> pd.DataFrame:
    data = [
        {
            "id": 1,
            "productDisplayName": "Wireless Headphones",
            "image_path": "images/product1.jpg"
        }
    ]
    df = pd.DataFrame(data)
    return df


# =========================
# IMAGE HANDLING
# =========================

def pil_to_base64(img: Image.Image) -> str:
    try:
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")
    except Exception as e:
        error_msg = (
            f"ERROR in pil_to_base64(): {type(e).__name__}\n"
            f"  Location: d:\\Documents\\Bootcamp\\4_Labs\\Lab7_Python_LowCode\\product_generator_refactored.py, line ~80\n"
            f"  Message: {str(e)}\n"
            f"  Suggestion: Ensure the PIL Image object is valid and not corrupted. Check if the image format is supported."
        )
        print(error_msg)
        raise


def load_image_as_base64(row: pd.Series) -> str:
    try:
        if "image" in row and isinstance(row["image"], Image.Image):
            return pil_to_base64(row["image"])

        if "image_path" in row and Path(row["image_path"]).exists():
            img = Image.open(row["image_path"])
            return pil_to_base64(img)

        raise ValueError(f"No valid image found for row {row.get('id')}")
    except Exception as e:
        error_msg = (
            f"ERROR in load_image_as_base64(): {type(e).__name__}\n"
            f"  Location: d:\\Documents\\Bootcamp\\4_Labs\\Lab7_Python_LowCode\\product_generator_refactored.py, line ~90\n"
            f"  Message: {str(e)}\n"
            f"  Suggestion: Check if the image file exists at the specified path. Ensure the image is not corrupted and is in a supported format (PNG, JPG, etc.). Verify the row contains either an 'image' column with PIL Image or 'image_path' with valid file path."
        )
        print(error_msg)
        raise


def build_image_payload(base64_str: str) -> Dict[str, Any]:
    try:
        return {
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{base64_str}"}
        }
    except Exception as e:
        error_msg = (
            f"ERROR in build_image_payload(): {type(e).__name__}\n"
            f"  Location: d:\\Documents\\Bootcamp\\4_Labs\\Lab7_Python_LowCode\\product_generator_refactored.py, line ~110\n"
            f"  Message: {str(e)}\n"
            f"  Suggestion: Ensure base64_str is a valid string. Check if the base64 encoding is correct."
        )
        print(error_msg)
        raise


# =========================
# PROMPT
# =========================

def create_product_prompt(product: Dict[str, Any]) -> str:
    try:
        return f"""
You are an expert e-commerce copywriter.

Product Info:
- Name: {product.get('productDisplayName')}
- Category: {product.get('masterCategory')}
- Subcategory: {product.get('subCategory')}
- Type: {product.get('articleType')}
- Color: {product.get('baseColour')}

Return JSON:
{{
  "title": "...",
  "description": "...",
  "features": ["..."],
  "keywords": ["..."]
}}
"""
    except Exception as e:
        error_msg = (
            f"ERROR in create_product_prompt(): {type(e).__name__}\n"
            f"  Location: d:\\Documents\\Bootcamp\\4_Labs\\Lab7_Python_LowCode\\product_generator_refactored.py, line ~120\n"
            f"  Message: {str(e)}\n"
            f"  Suggestion: Ensure the product parameter is a valid dictionary with expected keys. Check if product.get() calls are working correctly."
        )
        print(error_msg)
        raise


# =========================
# API CALL
# =========================

def call_cohere(client: Client, prompt: str, image_b64: str = None) -> str:
    try:
        response = client.chat(
            model=Config.MODEL,
            max_tokens=512,
            message=prompt
        )
        return response.text
    except Exception as e:
        error_msg = (
            f"ERROR in call_cohere(): {type(e).__name__}\n"
            f"  Location: d:\\Documents\\Bootcamp\\4_Labs\\Lab7_Python_LowCode\\product_generator_refactored.py, line ~150\n"
            f"  Message: {str(e)}\n"
            f"  Suggestion: Check API key validity and network connection. Ensure Cohere client is properly initialized. Verify model '{Config.MODEL}' is available. Check prompt length and content."
        )
        print(error_msg)
        raise RuntimeError(f"Cohere API call failed: {e}")


# =========================
# RESPONSE HANDLING
# =========================

def parse_api_response(raw_text: str) -> Dict[str, Any]:
    try:
        raw_text = raw_text.strip()
        
        if raw_text.startswith("```"):
            raw_text = raw_text.strip("`")
            raw_text = raw_text.replace("json\n", "", 1)

        return json.loads(raw_text)
    except json.JSONDecodeError as e:
        error_msg = (
            f"ERROR in parse_api_response(): {type(e).__name__}\n"
            f"  Location: d:\\Documents\\Bootcamp\\4_Labs\\Lab7_Python_LowCode\\product_generator_refactored.py, line ~165\n"
            f"  Message: {str(e)}\n"
            f"  Suggestion: Check the raw API response format. Ensure the model returned valid JSON. Look for markdown code blocks or extra text in the response."
        )
        print(error_msg)
        raise ValueError("Invalid JSON returned by model")
    except Exception as e:
        error_msg = (
            f"ERROR in parse_api_response(): {type(e).__name__}\n"
            f"  Location: d:\\Documents\\Bootcamp\\4_Labs\\Lab7_Python_LowCode\\product_generator_refactored.py, line ~165\n"
            f"  Message: {str(e)}\n"
            f"  Suggestion: Ensure raw_text is a valid string. Check for None or unexpected data types."
        )
        print(error_msg)
        raise


def validate_product_data(data: Dict[str, Any]) -> ProductListing:
    try:
        return ProductListing(**data)
    except ValidationError as e:
        error_msg = (
            f"ERROR in validate_product_data(): {type(e).__name__}\n"
            f"  Location: d:\\Documents\\Bootcamp\\4_Labs\\Lab7_Python_LowCode\\product_generator_refactored.py, line ~185\n"
            f"  Message: {str(e)}\n"
            f"  Suggestion: Check the data dictionary structure. Ensure it contains required fields: title (str), description (str), features (list), keywords (list). Verify data types match the ProductListing model."
        )
        print(error_msg)
        raise ValueError(f"Validation failed: {e}")
    except Exception as e:
        error_msg = (
            f"ERROR in validate_product_data(): {type(e).__name__}\n"
            f"  Location: d:\\Documents\\Bootcamp\\4_Labs\\Lab7_Python_LowCode\\product_generator_refactored.py, line ~185\n"
            f"  Message: {str(e)}\n"
            f"  Suggestion: Ensure data is a valid dictionary. Check if pydantic is properly installed."
        )
        print(error_msg)
        raise


def format_output(product: Dict[str, Any], listing: ProductListing) -> Dict[str, Any]:
    try:
        return {
            "id": product.get("id"),
            "name": product.get("productDisplayName"),
            "listing": listing.model_dump()
        }
    except Exception as e:
        error_msg = (
            f"ERROR in format_output(): {type(e).__name__}\n"
            f"  Location: d:\\Documents\\Bootcamp\\4_Labs\\Lab7_Python_LowCode\\product_generator_refactored.py, line ~205\n"
            f"  Message: {str(e)}\n"
            f"  Suggestion: Ensure product is a valid dictionary and listing is a ProductListing instance. Check if model_dump() method is available."
        )
        print(error_msg)
        raise


# =========================
# PIPELINE
# =========================

def process_product(client: Client, row: pd.Series) -> Dict[str, Any]:
    try:
        product_dict = row.to_dict()

        prompt = create_product_prompt(product_dict)

        raw_response = call_cohere(client, prompt)
        parsed = parse_api_response(raw_response)
        validated = validate_product_data(parsed)

        return format_output(product_dict, validated)

    except Exception as e:
        error_msg = (
            f"ERROR in process_product(): {type(e).__name__}\n"
            f"  Location: d:\\Documents\\Bootcamp\\4_Labs\\Lab7_Python_LowCode\\product_generator_refactored.py, line ~215\n"
            f"  Message: {str(e)}\n"
            f"  Suggestion: Check the row data structure. Ensure client is properly initialized. Verify API response parsing and validation steps. Check individual function calls within this pipeline."
        )
        print(error_msg)
        return {
            "id": row.get("id"),
            "error": str(e)
        }


def process_dataset(client: Client, df: pd.DataFrame, limit: int = 5) -> List[Dict]:
    try:
        print(f"Limit set to {limit} rows")
        
        results = []

        for idx, row in df.head(limit).iterrows():
            print(f"Processing row {idx}")
            result = process_product(client, row)
            results.append(result)

        return results
    except Exception as e:
        error_msg = (
            f"ERROR in process_dataset(): {type(e).__name__}\n"
            f"  Location: d:\\Documents\\Bootcamp\\4_Labs\\Lab7_Python_LowCode\\product_generator_refactored.py, line ~235\n"
            f"  Message: {str(e)}\n"
            f"  Suggestion: Ensure df is a valid pandas DataFrame. Check client initialization. Verify limit is a positive integer. Check process_product function for individual row errors."
        )
        print(error_msg)
        raise


# =========================
# OUTPUT
# =========================

def save_results(results: List[Dict], file_path: str):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"✓ Results saved to {file_path}")
    except Exception as e:
        error_msg = (
            f"ERROR in save_results(): {type(e).__name__}\n"
            f"  Location: d:\\Documents\\Bootcamp\\4_Labs\\Lab7_Python_LowCode\\product_generator_refactored.py, line ~255\n"
            f"  Message: {str(e)}\n"
            f"  Suggestion: Check write permissions for the directory. Ensure file_path is a valid string. Verify results is JSON serializable. Check disk space."
        )
        print(error_msg)
        raise


# =========================
# MAIN
# =========================

def main():
    try:
        client = init_client()
        df = load_products()

        results = process_dataset(client, df, limit=4)
        save_results(results, Config.OUTPUT_FILE)
    except Exception as e:
        error_msg = (
            f"ERROR in main(): {type(e).__name__}\n"
            f"  Location: d:\\Documents\\Bootcamp\\4_Labs\\Lab7_Python_LowCode\\product_generator_refactored.py, line ~275\n"
            f"  Message: {str(e)}\n"
            f"  Suggestion: Check the overall pipeline. Ensure all dependencies are installed. Verify configuration values. Run individual functions to isolate the issue."
        )
        print(error_msg)
        raise


if __name__ == "__main__":
    main()