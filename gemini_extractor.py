import os
import google.generativeai as genai
import re
import json
from dotenv import load_dotenv

load_dotenv()

def extract_deals_with_gemini(html_content: str) -> list:
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY not found in .env")

    genai.configure(api_key=gemini_api_key)

    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = """
    Extract all deals from this page.

    For each deal, return the following fields:
    - title
    - revenue
    - ebitda
    - askingPrice
    - industry
    - dealCaption

    Respond ONLY with a valid JSON object inside a markdown-style code block like this:

    ```json
    {
      "deals": [
        {
          "title": "Deal Title",
          "revenue": "$1,000,000",
          "ebitda": "$200,000",
          "askingPrice": "$500,000",
          "industry": "Industry Name",
          "dealCaption": "Brief summary of the deal"
        }
      ]
    }
    """.strip()

    try:
        response = model.generate_content(f"{prompt}\n\n{html_content}")
        match = re.search(r"```json\n(.*?)\n```", response.text, re.DOTALL)
        if match:
            json_data = match.group(1)
            return json.loads(json_data)["deals"]
        else:
            print("❌ No JSON found.")
            return []
    except Exception as e:
        print(f"❌ Gemini error: {e}")
        return []
