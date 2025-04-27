import os
import google.generativeai as genai

# Configure the API key
genai.configure(api_key="")

# Load the model
model = genai.GenerativeModel("models/gemini-1.5-pro")


def generate_response(prompt: str, max_tokens: int = 1024) -> str:
    try:
        full_prompt = (
            "You are a friendly, empathetic job assistant. Present job data clearly and supportively. "
            "Mention missing details (like salary) gently. Always be kind.\n\n"
            f"{prompt}"
        )

        response = model.generate_content(
            full_prompt,
            generation_config={
                "max_output_tokens": max_tokens
            }
        )
        return response.text.strip()

    except Exception as e:
        return f"Error generating response: {str(e)}"


# def generate_response(prompt: str, max_tokens: int = 100) -> str:
#     """
#     Generates a response using Google's Gemini model (gemini-pro).

#     :param prompt: Prompt text to send to the model.
#     :param max_tokens: Maximum number of tokens in the output.
#     :return: Model's response text.
#     """
#     try:
#         response = model.generate_content(
#             prompt,
#             generation_config={
#                 "max_output_tokens": max_tokens
#             }
#         )
#         return response.text.strip()
#     except Exception as e:
#         return f"Error: {str(e)}"
