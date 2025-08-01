import openai
import os

class FeedbackModel:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        openai.api_key = self.api_key

    def analyze_feedback(self, feedback_text):
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You're an M&A analyst learning to identify good acquisition candidates."},
                {"role": "user", "content": feedback_text}
            ]
        )
        return response["choices"][0]["message"]["content"]
