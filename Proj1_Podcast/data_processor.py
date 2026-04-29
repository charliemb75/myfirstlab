"""
Input: MVP: text. Then PDF, then API, target audience (kids, experts, general public...), style (MVP = 2 people conversation)
Output: string with combined content of text, pdf, api (input for llm_processor.py)
"""

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ----------- LOADERS -----------

def load_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def load_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # remove scripts/styles
    for tag in soup(["script", "style"]):
        tag.decompose()

    return soup.get_text(separator="\n")


def load_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


# ----------- SUMMARIZATION -----------

def summarize_text(text):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"Summarize the following text clearly and concisely:\n\n{text}"
    )
    return response.output_text


# ----------- MAIN PIPELINE -----------

def process_sources(sources):
    combined_text = ""

    for source in sources:
        if source.endswith(".txt"):
            combined_text += load_txt(source)

        elif source.endswith(".pdf"):
            combined_text += load_pdf(source)

        elif source.startswith("http"):
            combined_text += load_url(source)

        else:
            print(f"Unknown source: {source}")

        combined_text += "\n\n---NEW SOURCE---\n\n"

        print(combined_text)

    return summarize_text(combined_text)


# ----------- USAGE -----------

if __name__ == "__main__":
    sources = [
        "https://www.ibm.com/reports/threat-intelligence?utm_content=SRCWW&p1=Search&p4=401463774&p5=b&p9=193665805663&gclsrc=aw.ds&gad_source=1&gad_campaignid=23555261032&gbraid=0AAAAA-h2TOGTgKWKKruykFrmHc5Dlu2X0&gclid=Cj0KCQjwkrzPBhCqARIsAJN460kR7tT1Z4qqfJfhvv8X9-hW41GbHhajP1mwldXcVsSBY82iIjzHXgYaAhdYEALw_wcB",
        "Proj1_Podcast/MS_ISAC_Prompt_Injections_20260311.pdf"
    ]

    summary = process_sources(sources)

    print(summary)