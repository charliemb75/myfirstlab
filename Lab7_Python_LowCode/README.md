# Lab7: Python Low-Code Product Generator

## Overview
This folder contains a refactored low-code product generation pipeline that uses the Cohere API to create product listings from a small fashion dataset.

## Files and Purpose
- `product_generator_refactored.py` - Main pipeline implementation.
  - `Config` class: stores model configuration, dataset name, dataset split, and output file path.
  - `ProductListing` model: validates generated listing data using `pydantic`.
  - `init_client()`: loads `COHERE_API_KEY` from `.env` and creates a Cohere client.
  - `load_products()`: loads the dataset using `datasets` and returns a pandas DataFrame.
  - `create_fallback_dataset()`: fallback dataset when remote loading fails.
  - `pil_to_base64()`, `load_image_as_base64()`, `build_image_payload()`: image handling utilities.
  - `create_product_prompt()`: generates prompt text for the model.
  - `call_cohere()`: sends the prompt to the Cohere chat model.
  - `parse_api_response()`: parses the raw model output as JSON.
  - `validate_product_data()`: ensures the model output contains required listing fields.
  - `format_output()`: formats product results for saving.
  - `process_product()`, `process_dataset()`: pipeline functions to process rows and datasets.
  - `save_results()`: writes JSON output to disk.
  - `main()`: end-to-end runner for the full pipeline.

- `tests.py` - Simple functional tests for core helper functions in `product_generator_refactored.py`.
- `product_listings.json` - Output file created by the generator.
- `refactoring_checklist.txt` - Notes and checklist for refactoring or improvements.
- `test_results.txt` - Stored test results / notes.
- `.env` - Environment file used to store `COHERE_API_KEY`.

## Requirements
Install the Python dependencies used by this lab. From the `Lab7_Python_LowCode` folder, run:

```bash
pip install -r requirements.txt
```

## Setup
1. Open `Lab7_Python_LowCode` in your terminal.
2. Create or update `.env` with your Cohere API key:

```text
COHERE_API_KEY=your_api_key_here
```

3. Confirm the dataset config in `product_generator_refactored.py`:
- `Config.DATASET_NAME` is `ashraq/fashion-product-images-small`
- `Config.DATASET_SPLIT` is `train[:100]`
- `Config.OUTPUT_FILE` is `Lab7_Python_LowCode/product_listings.json`

## How to Run
From the `Lab7_Python_LowCode` folder, run:

```bash
python product_generator_refactored.py
```

This will:
- initialize the Cohere client
- load the dataset
- process up to 4 products
- save the generated listings to `Lab7_Python_LowCode/product_listings.json`

## Running Tests
To verify helper functions, run:

```bash
python tests.py
```

## Notes
- The script uses a small dataset from Hugging Face `datasets`.
- If the dataset cannot be loaded, the pipeline falls back to a minimal dummy dataset.
- The Cohere API response is expected to return JSON matching the `ProductListing` model fields.

## File/Folder Map
- `Lab7_Python_LowCode/`
  - `product_generator_refactored.py` — main script and pipeline
  - `tests.py` — local tests for validation and parsing utilities
  - `product_listings.json` — generated JSON output
  - `refactoring_checklist.txt` — refactoring notes
  - `test_results.txt` — saved test output
  - `.env` — environment variables (API key)
