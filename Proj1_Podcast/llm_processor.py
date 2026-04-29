"""
Input: string with combined content of text, pdf, api (output of data_processor.py)
Output: podcast script as a python string.
Example:
"text = "[Speaker1]: Hello, I'm Speaker 1\n[Speaker2]: Hello, I'm Speaker 2"
"""
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

# Initialize client (make sure OPENAI_API_KEY is set in your environment)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_podcast_script(file_path):
    # Step 1: Read input text file
    with open(file_path, "r", encoding="utf-8") as f:
        input_text = f.read()

    # Step 2: Create prompt
    prompt = f"""
You are a podcast script writer.

Convert the following text into a conversation between two speakers.

Rules:
- Use exactly this format:
  [Speaker1]: ...
  [Speaker2]: ...
- Alternate between Speaker1 and Speaker2
- Keep it natural and engaging like a real podcast
- Do NOT add anything outside the dialogue
- Output must be a single string, separating each intervention in a new line (\n)

TEXT:
{input_text}
"""

    # Step 3: Call OpenAI API
    response = client.responses.create(
        model="gpt-4o",
        input=prompt,
        temperature=0.5
    )

    # Step 4: Extract result
    script = response.output[0].content[0].text

    return script


if __name__ == "__main__":
    file_path = "Proj1_Podcast/example_text.txt"  # your input file
    script = generate_podcast_script(file_path)
    print(script)