import google.generativeai as genai
import json
import re
import os
genai.configure(api_key="AIzaSyA0SlEVcamDSIGGwzCne7x1HNDJNdDW1VU")

def ask_gemini_mcq_generation(text: str):
    """
    Sends the provided notes text to Gemini and requests MCQ generation.
    Returns a list of dicts with keys: question, options, answer.
    """

    prompt = f"""
Generate as many multiple-choice questions as possible from the following notes.
Each question must include exactly four plausible options and one correct answer.
Return ONLY a valid JSON array strictly matching this format:

[
  {{
    "question": "string",
    "options": ["string", "string", "string", "string"],
    "answer": "string"
  }}
]

Do not include explanations, markdown, or extra text.
Here are the notes:
\"\"\"{text}\"\"\"
"""

   
    response = genai.GenerativeModel("gemini-2.5-flash").generate_content(prompt)
    json_text = response.text.strip()
    json_match = re.search(r'\[.*\]', json_text, re.DOTALL)
    if not json_match:
        raise ValueError("Gemini did not return valid JSON.")

    try:
        quiz_data = json.loads(json_match.group(0))
    except json.JSONDecodeError:
        raise ValueError("Failed to parse Gemini response as JSON.")
    valid_quiz = []
    for q in quiz_data:
        if (
            isinstance(q, dict)
            and "question" in q
            and "options" in q
            and "answer" in q
            and isinstance(q["options"], list)
        ):
            valid_quiz.append(q)

    return valid_quiz