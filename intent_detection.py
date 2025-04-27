# def build_intent_prompt(query: str) -> str:
#     return (
#         f"You are an assistant helping to detect user intent from job search queries.\n\n"
#         f"Extract the following from the query if available:\n"
#         f"- City\n- Category (starter, restarter, reriser)\n- Salary Expectations\n- Experience level\n\n"
#         f"If information is missing, respond with 'Not mentioned'.\n\n"
#         f"Respond ONLY in JSON like:\n"
#         f'{{"city": "...", "category": "...", "salary": "...", "experience": "..."}}\n\n'
#         f"User Query: {query}"
#     )

# import json

# # Step 1: Build better intent prompt
# def build_intent_prompt(query: str) -> str:
#     return (
#         f"You are an expert at extracting structured information from job search queries.\n\n"
#         f"From the user's query, extract and output ONLY a JSON object with these fields:\n"
#         f'- "city": If city mentioned, otherwise "Not mentioned".\n'
#         #f'- "category": "starter" (freshers/new graduates), "restarter" (career break/returning), "reriser" (promotion/senior role), or "Not mentioned".\n'
#         f'- "salary": If salary expectation mentioned, else "Not mentioned".\n'
#         f'- "experience": Extract experience level like "freshers", "2 years", "senior", etc. If missing, say "Not mentioned".\n\n'
#         f"IMPORTANT:\n"
#         f"- Output must be RAW JSON without markdown formatting like ``` or any text.\n"
#         f"- No greetings, no explanations — just pure JSON.\n\n"
#         f"Example:\n"
#         f'Input: "Looking for a marketing job in Bangalore for freshers"\n'
#         f'Output: {{"city": "Bangalore", "salary": "Not mentioned", "experience": "freshers"}}\n\n'
#         f"Now extract from:\n\"\"\"{query}\"\"\""
#     )

# # Step 2: Tiny bonus cleaner (for unexpected ``` or non-JSON)
# def clean_intent_response(response: str) -> dict:
#     try:
#         # Remove ``` or anything before/after JSON
#         cleaned = response.strip().strip("```").strip()
#         # Parse JSON safely
#         return json.loads(cleaned)
#     except Exception as e:
#         print(f"Failed to parse intent response: {response}")
#         return {"city": "", "category": "", "salary": "", "experience": ""}


# import json

# # Step 1: Build intent prompt
# def build_intent_prompt(query: str) -> str:
#     return (
#         f"You are an expert at extracting structured information from job search queries.\n\n"
#         f"From the user's query, extract and output ONLY a JSON object with these fields:\n"
#         f'- "city": If a city is mentioned, otherwise "Not mentioned".\n'
#         f'- "role": The type of job the user is looking for, like "software development", "marketing", etc. If not mentioned, say "Not mentioned".\n'
#         f'- "salary": If salary expectation mentioned, else "Not mentioned".\n'
#         f'- "experience": Extract experience level like "freshers", "2 years", "senior", etc. If missing, say "Not mentioned".\n\n'
#         f"IMPORTANT:\n"
#         f"- Output must be RAW JSON without any markdown formatting like ``` or any text.\n"
#         f"- No greetings, no explanations — just pure JSON.\n\n"
#         f"Example:\n"
#         f'Input: "Looking for a marketing job in Bangalore for freshers"\n'
#         f'Output: {{"city": "Bangalore", "role": "marketing", "salary": "Not mentioned", "experience": "freshers"}}\n\n'
#         f"Now extract from:\n\"\"\"{query}\"\"\""
#     )
# # Step 2: Clean intent response
# def clean_intent_response(response: str) -> dict:
#     try:
#         cleaned = response.strip().strip("```").strip()
#         return json.loads(cleaned)
#     except Exception as e:
#         print(f"Failed to parse intent response: {response}")
#         return {"city": "", "role": "", "salary": "", "experience": ""}



import json

# Step 1: Build intent prompt
def build_intent_prompt(query: str) -> str:
    return (
        f"You are an expert at extracting structured information from job search queries.\n\n"
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

# # Step 2: Clean intent response
# def clean_intent_response(response: str) -> dict:
#     try:
#         # Remove extra whitespaces and code block markers
#         cleaned = response.strip().strip("```").strip()
        
#         # Check if the cleaned response is empty
#         if not cleaned:
#             raise ValueError("Empty response received")

#         # Try to parse the response as JSON
#         return json.loads(cleaned)
    
#     except json.JSONDecodeError:
#         print(f"Failed to parse intent response due to JSON decoding error: {response}")
#         return {"city": "Not mentioned", "role": "Not mentioned", "salary": "Not mentioned", "experience": "Not mentioned"}
#     except ValueError as ve:
#         print(f"Failed to parse intent response due to an error: {ve}")
#         return {"city": "Not mentioned", "role": "Not mentioned", "salary": "Not mentioned", "experience": "Not mentioned"}
#     except Exception as e:
#         print(f"Unexpected error during intent response parsing: {e}")
#         return {"city": "Not mentioned", "role": "Not mentioned", "salary": "Not mentioned", "experience": "Not mentioned"}
