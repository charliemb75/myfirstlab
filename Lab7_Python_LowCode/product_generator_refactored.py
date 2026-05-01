# %% [markdown]
# # Lab 4: Product listings - ChatGPT API

# %% [markdown]
# ## Step 1: Set-Up

"""
Automation of creation of product listings with ChatGPT
Author: Carlos Martinez Boto
"""
import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from typing import List
load_dotenv()
import json
from datasets import load_dataset
import requests
from PIL import Image
import pandas as pd
from pathlib import Path
from IPython.display import display

# Initialize client
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

# %% [markdown]
# ## Step 2: Preparing the Dataset

# Load dataset from HuggingFace
print("Loading product dataset...")
try:
    # Try loading the dataset
    dataset = load_dataset("ashraq/fashion-product-images-small", split="train[:100]")  # First 100 samples
    print(f"✓ Loaded {len(dataset)} products")
    
    # Convert to pandas for easier manipulation
    products_df = pd.DataFrame(dataset)
    print(f"Dataset columns: {products_df.columns.tolist()}")
    
except Exception as e:
    print(f"⚠ Could not load HuggingFace dataset: {e}")
    print("Using local images instead...")
    
    # Alternative: Use local images
    # Create a products.json file with product information
    products_data = [
        {
            "id": 1,
            "name": "Wireless Headphones",
            "price": 79.99,
            "category": "Electronics",
            "image_path": "images/product1.jpg"
        },
        # Add more products...
    ]
    
    products_df = pd.DataFrame(products_data)


# %%
# Create images directory
images_dir = Path("product_images")
images_dir.mkdir(exist_ok=True)
 
print(f"\n✓ Dataset prepared!")
print(f"  Total products: {len(products_df)}")

# %%
# print(products_df['image'].head())
# for _, row in products_df.head().iterrows():
#     display(row["image"])

# %% [markdown]
# ## Step 3: Encoding Images for API

# %%
import base64
from io import BytesIO

# Read an image file and returns a Base64-encoded string
def pil_to_base64(img):
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

# %%
products_df["image_base64"] = products_df["image"].apply(pil_to_base64)
print(products_df[["image", "image_base64"]].head())

# %% [markdown]
# ## Step 4: Creating the Product Listing Prompt

# %%
def create_product_listing_prompt(df_row):
    """
    Create a prompt for generating product listings.
    
    Parameters:
    - product_name: Name of the product
    - price: Price of the product
    - category: Product category
    - additional_info: Optional additional information
    
    Returns:
    - Formatted prompt string
    """
    prompt = f"""You are an expert e-commerce copywriter. Analyze the product image and create a compelling product listing.
 
Product Information:
- ID: {df_row['id']}
- Gender: {df_row['gender']}
- Category: {df_row['masterCategory']}; {df_row['subCategory']}; {df_row['articleType']}
- Colour: {df_row['baseColour']}
- Season, Usage: {df_row['season']}; {df_row['usage']}
- Year: {df_row['year']:.0f}
- Display name: {df_row['productDisplayName']}
 
Please create a professional product listing that includes:
 
1. **Product Title** (catchy, SEO-friendly, 60 characters max)
2. **Product Description** (detailed, 150-200 words)
   - Highlight key features and benefits
   - Use persuasive language
   - Include relevant details visible in the image
3. **Key Features** (bullet points, 5-7 items)
4. **SEO Keywords** (comma-separated, 10-15 relevant keywords)
 
Format your response as JSON with the following structure:
{{
    "title": "Product title here",
    "description": "Full description here",
    "features": ["Feature 1", "Feature 2", ...],
    "keywords": "keyword1, keyword2, ..."
}}
 
Be specific about what you see in the image. Mention colors, materials, design elements, and any distinctive features."""
    
    return prompt

# %%
# Test prompt creation
test_prompt = create_product_listing_prompt(products_df.iloc[0])
 
print("\n" + "="*50)
print("PROMPT TEMPLATE")
print("="*50)
print(test_prompt[:500] + "...")  # Show first 500 characters

# %% [markdown]
# ## Step 5: Calling the ChatGPT API with Vision

# %%
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user",
        "content": [{"type": "text", "text": test_prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{products_df['image_base64'].iloc[0]}"}}]
        }
    ]
)
print(response.choices[0].message.content)

# %% [markdown]
# ## Step 6: Processing Multiple Products

# %%
def generate_response(df_row):
    prompt = create_product_listing_prompt(df_row)
    image = {"url": f"data:image/png;base64,{df_row['image_base64']}"}

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user",
            "content": [{"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": image}]
            }
        ]
    )
    return response.choices[0].message.content

# %%
start = 0
end = 4 # len(products_df)
all_results = []

for idx, row in products_df.iloc[start:end].iterrows():
    print(f"\n===== ROW {idx} =====")

    result = generate_response(row)
    products_df.loc[idx, "listing_raw"] = result

    display(row["image"])
    all_results.append(result)
    print(result)

# %%
with open("product_listings.json", "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2, ensure_ascii=False)


