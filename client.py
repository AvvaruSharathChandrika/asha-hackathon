# import requests

# API_URL = "http://localhost:8000/search"  # Updated endpoint

# def send_query_to_bot(query: str, city: str = None, category: str = None, experience: str = None) -> str:
#     """
#     Sends user query and optional metadata to the FastAPI backend and returns the chatbot response.

#     Parameters:
#         query (str): The user’s message or job-related question.
#         city (str): Optional city name.
#         category (str): Optional category (e.g., 'starters', 'restartes', 're-risers').
#         experience (str): Optional experience filter.

#     Returns:
#         str: The chatbot's response or error message.
#     """
#     payload = {
#         "query": query,
#         "city": city,
#         "category": category,
#         "experience": experience
#     }

#     try:
#         print(f"Sending request to {API_URL} with: {payload}")
#         response = requests.post(API_URL, json=payload, timeout=40)
#         response.raise_for_status()
#         data = response.json()
#         print("🔍 Raw response from server:", data)

#         if "response" in data:
#             return data["response"]
#         elif "error" in data:
#             return f"❌ Server Error: {data['error']}"
#         else:
#             return "⚠️ Unexpected response format from the server."

#     except requests.exceptions.ConnectionError:
#         return "🔌 Could not connect to the server. Is it running?"
#     except requests.exceptions.Timeout:
#         return "⏳ The request timed out. Please try again."
#     except requests.exceptions.HTTPError as e:
#         return f"🚨 HTTP error: {str(e)}"
#     except Exception as e:
#         return f"❗ Unexpected error: {str(e)}"




import requests

API_URL = "http://localhost:8000/search"

def send_query_to_bot(user_input: str, history: list) -> str:
    """
    Sends the conversation context and new user input to the FastAPI backend.
    
    Parameters:
        user_input (str): The latest user message.
        history (list): A list of past messages (tuples of user, assistant).
        
    Returns:
        str: The chatbot's response.
    """
    payload = {
        "message": user_input,
        "history": history
    }

    try:
        print(f"Sending request to {API_URL} with: {payload}")
        response = requests.post(API_URL, json=payload, timeout=40)
        response.raise_for_status()
        data = response.json()
        print("🔍 Raw response from server:", data)

        if "response" in data:
            return data["response"]
        elif "error" in data:
            return f"❌ Server Error: {data['error']}"
        else:
            return "⚠️ Unexpected response format from the server."

    except requests.exceptions.ConnectionError:
        return "🔌 Could not connect to the server. Is it running?"
    except requests.exceptions.Timeout:
        return "⏳ The request timed out. Please try again."
    except requests.exceptions.HTTPError as e:
        return f"🚨 HTTP error: {str(e)}"
    except Exception as e:
        return f"❗ Unexpected error: {str(e)}"
