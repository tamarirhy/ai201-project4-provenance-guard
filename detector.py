import json
import os

from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def analyze_text(text):
    """
    Uses the Groq API as the first detection signal.

    Returns:
    {
        "attribution": "likely_ai" or "likely_human",
        "score": float (0.0 - 1.0)
    }
    """

    prompt = f"""
You are an AI attribution system.

Analyze the writing below.

Return ONLY valid JSON.

The JSON must look exactly like this:

{{
    "attribution": "likely_ai",
    "score": 0.87
}}

Rules:

- attribution must be either "likely_ai" or "likely_human"
- score must be a decimal between 0 and 1
- Higher scores mean stronger evidence the writing is AI-generated.
- Do not include explanations.
- Do not include markdown.
- Do not include extra text.

Writing:

\"\"\"
{text}
\"\"\"
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        result = response.choices[0].message.content.strip()

        parsed = json.loads(result)

        return {
            "attribution": parsed["attribution"],
            "score": float(parsed["score"])
        }

    except Exception as e:
        print("Groq Error:", e)

        # Safe fallback so the app doesn't crash
        return {
            "attribution": "unknown",
            "score": 0.0
        }