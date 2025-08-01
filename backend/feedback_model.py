import openai
import os

class FeedbackModel:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def analyze_feedback(self, feedback_text):
        system_prompt = "You're an M&A analyst learning to identify good acquisition candidates."
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": feedback_text}
        ]

        # Attempt GPT-4o
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )
            content = response.choices[0].message.content
            return {"model_used": "gpt-4o", "content": content}

        # If GPT-4o is unavailable, fallback to GPT-3.5
        except openai.APIError as e:
            if "quota" in str(e).lower() or "gpt-4o" in str(e).lower():
                try:
                    response = self.client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=messages
                    )
                    content = response.choices[0].message.content
                    return {"model_used": "gpt-3.5-turbo", "content": content}
                except Exception as fallback_error:
                    return {"model_used": "error", "content": f"Fallback error: {str(fallback_error)}"}

            return {"model_used": "error", "content": f"GPT-4o API error: {str(e)}"}

        except Exception as general_error:
            return {"model_used": "error", "content": f"Unexpected error: {str(general_error)}"}
