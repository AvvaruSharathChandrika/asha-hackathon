import json
# Step 1: Build intent prompt
def build_intent_prompt(query: str) -> str:
    return (
        f"You are an assistant designed specifically for job seekers who are women, and your role is to help them find jobs in a safe, inclusive, and empathetic environment.\n\n"
        f"Here are some important guidelines for your behavior:\n"
        f"- Be empathetic and kind in your responses, understanding that every user is on a personal journey.\n"
        f"- Avoid any stereotypes related to gender, family, or any other factor that could make the user feel uncomfortable.\n"
        f"- Ensure that the job suggestions or recommendations are non-discriminatory, welcoming, and suitable for all women, regardless of background.\n"
        f"- Use language that empowers women and promotes equality.\n\n"
        f"From the user's query, extract and output ONLY a JSON object with these fields:\n"
        f'- "city": If a city is mentioned, otherwise "Not mentioned".\n'
        f'- "role": The type of job the user is looking for, like "software development", "marketing", etc. If not mentioned, say "Not mentioned".\n'
        f'- "salary": If salary expectation mentioned, else "Not mentioned".\n'
        f'- "experience": Extract experience level like "freshers", "2 years", "senior", etc. If missing, say "Not mentioned".\n\n'
        f"IMPORTANT:\n"
        f"- Output must be RAW JSON without any markdown formatting like ``` or any text.\n"
        f"- No greetings, no explanations — just pure JSON.\n\n"
        f"Example:\n"
        f'Input: "Looking for a marketing job in Bangalore for freshers"\n'
        f'Output: {{"city": "Bangalore", "role": "marketing", "salary": "Not mentioned", "experience": "freshers"}}\n\n'
        f"Now extract from:\n\"\"\"{query}\"\"\""
    )

# Step 2: Clean intent response
def clean_intent_response(response: str) -> dict:
    try:
        # Remove extra whitespaces and code block markers
        cleaned = response.strip().strip("```").strip()
        
        # Check if the cleaned response is empty
        if not cleaned:
            raise ValueError("Empty response received")

        # Try to parse the response as JSON
        intent = json.loads(cleaned)
        
        # --- ADD THIS NEW PART HERE ---
        # Fix city casing to title case
        if intent.get("city") and intent["city"] != "Not mentioned":
            intent["city"] = intent["city"].title()
        # --------------------------------

        return intent
    
    except json.JSONDecodeError:
        print(f"Failed to parse intent response due to JSON decoding error: {response}")
        return {"city": "Not mentioned", "role": "Not mentioned", "salary": "Not mentioned", "experience": "Not mentioned"}
    except ValueError as ve:
        print(f"Failed to parse intent response due to an error: {ve}")
        return {"city": "Not mentioned", "role": "Not mentioned", "salary": "Not mentioned", "experience": "Not mentioned"}
    except Exception as e:
        print(f"Unexpected error during intent response parsing: {e}")
        return {"city": "Not mentioned", "role": "Not mentioned", "salary": "Not mentioned", "experience": "Not mentioned"}
