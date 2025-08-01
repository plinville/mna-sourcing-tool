import os
from openai import OpenAI

class FeedbackModel:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        self.client = OpenAI(api_key=api_key)

    def analyze_feedback(self, feedback_text):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You're an M&A analyst learning to identify good acquisition candidates."},
                {"role": "user", "content": feedback_text}
            ]
        )
        return response.choices[0].message.content
