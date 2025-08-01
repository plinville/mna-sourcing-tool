import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_feedback(feedback_text):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You're an M&A analyst learning to identify good acquisition candidates."},
            {"role": "user", "content": feedback_text}
        ]
    )
    return response["choices"][0]["message"]["content"]
