from retriever.retriever import or_search_query, elastic_query, get_data_from_elk, get_context_sources
from models.llm_models import generate_response
from prompt_engineering.prompts import handle_query
from utility import process_query
from intent_detection import build_intent_prompt, clean_intent_response

# Step 1: Retrieve relevant data with granular filters + fallback
def retrieve_data(query: str, location: str, experience: str, role: str):
    # Normalize the "Not mentioned" values to empty strings
    loc = location if location.lower() != "not mentioned" else ""
    exp = experience if experience.lower() != "not mentioned" else ""
    rl = role if role.lower() != "not mentioned" else ""

    # Build the query based on what we have (location, experience, role)
    if loc or exp or rl:
        if loc and exp and rl:
            branch = "location+experience+role"
            qb = elastic_query(loc, exp, rl)
        elif loc and rl:
            branch = "location+role"
            qb = elastic_query(loc, "", rl)
        elif loc and exp:
            branch = "location+experience"
            qb = elastic_query(loc, exp, "")
        elif rl and exp:
            branch = "role+experience"
            qb = elastic_query("", exp, rl)
        elif loc:
            branch = "location only"
            qb = elastic_query(loc, "", "")
        elif rl:
            branch = "role only"
            qb = elastic_query("", "", rl)
        elif exp:
            branch = "experience only"
            qb = elastic_query("", exp, "")

        print(f"[Retriever] Branch: {branch}")
        print(f"[Retriever] Query body: {qb}")
        results = get_data_from_elk(qb)

        # If structured query returned zero results, try location-only query (if location is present)
        if not results and loc:
            print("[Retriever] Zero results; retrying location-only fallback")
            qb2 = elastic_query(loc, "", "")
            print(f"[Retriever] Location-only fallback query body: {qb2}")
            results = get_data_from_elk(qb2)

        return results

    # If no structured filters are found, do free-text fallback
    print("[Retriever] No structured filters found, doing free-text fallback")
    qb = or_search_query(query)
    print(f"[Retriever] Free-text query body: {qb}")
    return get_data_from_elk(qb)
# Step 2: Extract context
def extract_context_and_sources(results):
    if not results:
        return "No jobs found. Would you like to try a different location or role?"
    return get_context_sources(results)

# Step 3: Build job search prompt
def generate_prompt(query: str, city: str = None):
    base = handle_query(query, city)
    instruction = (
        "Please present the job opportunities in a friendly, empathetic tone. "
        "If any details are missing, mention it gently. Structure each listing:\n\n"
        "- **Job Title:**\n- **Location:**\n- **Experience:**\n- **Salary:**\n- **Description:**\n\n"
        "If no jobs match, encourage adjusting the search."
    )
    return f"{base}\n\n{instruction}\n\nHere are some jobs I found:\n"

# Step 4: Final response
# def generate_answer(prompt: str, context: str):
#     return generate_response(f"{prompt}\n{context}")
# Step 4: Final response
def generate_answer(prompt: str, context: str, max_tokens: int = 1024):
    full_prompt = f"{prompt}\n{context}"
    return generate_response(full_prompt, max_tokens=max_tokens)


# Main RAG + intent detection pipeline
def rag_pipeline(query: str):
    q = process_query(query)
    print("Processed Query:", q)

    # Intent detection
    ip = build_intent_prompt(q)
    raw = generate_response(ip, max_tokens=300)
    intent = clean_intent_response(raw)
    print("Detected Intent:", intent)

    city       = intent.get("city", "")
    experience = intent.get("experience", "")
    role       = intent.get("role", "")

    # Retrieve & format
    jobs    = retrieve_data(q, city, experience, role)
    context = extract_context_and_sources(jobs)
    prompt  = generate_prompt(q, city)
    answer = generate_answer(prompt, context, max_tokens=1024)

    return answer



# from retriever.retriever import or_search_query, elastic_query, get_data_from_elk, get_context_sources
# from models.llm_models import generate_response
# from prompt_engineering.prompts import handle_query
# from utility import process_query
# from typing import List, Dict
# from intent_detection import build_intent_prompt, clean_intent_response   

# # Step 1: Retrieve relevant data
# def retrieve_data(query: str, location: str, experience: str, role: str):
#     # Validate that each field is not empty
#     if location or experience or role:
#         query_body = elastic_query(location, experience, role)
#     else:
#         query_body = or_search_query(query)
#     return get_data_from_elk(query_body)

# # Step 2: Extract context
# def extract_context_and_sources(results):
#     # If no results, suggest retrying with different search criteria
#     if not results:
#         return "No jobs found. Would you like to try a different city or role?"
    
#     return get_context_sources(results)

# # Step 3: Build job search prompt
# def generate_prompt(query: str, city: str = None):
#     base_prompt = handle_query(query, city)
#     instruction = (
#         "Please present the job opportunities in a friendly, empathetic tone. "
#         "Avoid harsh critique. If any job details are missing (like salary or description), "
#         "mention it gently and offer to help find more details. Structure each job listing like:\n\n"
#         "- **Job Title**: \n- **Location**: \n- **Company**: \n- **Salary** (if available): \n- **Description**: \n"
#         "- **Apply Link** (if available): \n\n"
#         "Only include the job data provided. If no jobs are found, offer encouragement and ask if the user wants to adjust location or role."
#     )
#     return f"{base_prompt}\n\n{instruction}\n\nHere are some jobs I found:\n"

# # Step 4: Final response
# def generate_answer(prompt: str, context: str):
#     full_prompt = f"{prompt}\n{context}"
#     return generate_response(full_prompt)

# # Main rag + intent detection pipeline
# def rag_pipeline(query: str):
#     # Step 0: Preprocess user query
#     processed_query = process_query(query)
#     print("Processed Query:", processed_query)

#     # Step 1: Intent detection
#     intent_prompt = build_intent_prompt(processed_query)
#     intent_response_raw = generate_response(intent_prompt, max_tokens=300)
#     intent = clean_intent_response(intent_response_raw)

#     print(f"Detected Intent: {intent}")

#     # Step 2: Retrieve data
#     city = intent.get("city", "")
#     experience = intent.get("experience", "")
#     role = intent.get("role", "")   # NEW addition

#     # Logging the query data before making the call
#     print(f"Retrieving data for: city={city}, experience={experience}, role={role}")

#     retrieved_data = retrieve_data(processed_query, city, experience, role)

#     # Step 3: Extract context
#     context = extract_context_and_sources(retrieved_data)

#     # Step 4: Build search prompt
#     prompt = generate_prompt(processed_query, city)

#     # Step 5: Generate final answer
#     answer = generate_answer(prompt, context)

#     return answer




# from retriever.retriever import or_search_query, elastic_query, get_data_from_elk, get_context_sources
# from models.llm_models import generate_response
# from prompt_engineering.prompts import handle_query
# from utility import process_query
# from typing import List, Dict
# from intent_detection import build_intent_prompt, clean_intent_response   

# # Step 1: Retrieve relevant data
# def retrieve_data(query: str, location: str, experience: str, role: str):
#     if location or experience or role:
#         query_body = elastic_query(location, experience, role)
#     else:
#         query_body = or_search_query(query)
#     return get_data_from_elk(query_body)

# # Step 2: Extract context
# def extract_context_and_sources(results):
#     return get_context_sources(results)

# # Step 3: Build job search prompt
# def generate_prompt(query: str, city: str = None):
#     base_prompt = handle_query(query, city)
#     instruction = (
#         "Please present the job opportunities in a friendly, empathetic tone. "
#         "Avoid harsh critique. If any job details are missing (like salary or description), "
#         "mention it gently and offer to help find more details. Structure each job listing like:\n\n"
#         "- **Job Title**: \n- **Location**: \n- **Company**: \n- **Salary** (if available): \n- **Description**: \n"
#         "- **Apply Link** (if available): \n\n"
#         "Only include the job data provided. If no jobs are found, offer encouragement and ask if the user wants to adjust location or role."
#     )
#     return f"{base_prompt}\n\n{instruction}\n\nHere are some jobs I found:\n"

# # Step 4: Final response
# def generate_answer(prompt: str, context: str):
#     full_prompt = f"{prompt}\n{context}"
#     return generate_response(full_prompt)

# # Main rag + intent detection pipeline
# def rag_pipeline(query: str):
#     # Step 0: Preprocess user query
#     processed_query = process_query(query)
#     print("Processed Query:", processed_query)

#     # Step 1: Intent detection
#     intent_prompt = build_intent_prompt(processed_query)
#     intent_response_raw = generate_response(intent_prompt, max_tokens=300)
#     intent = clean_intent_response(intent_response_raw)

#     print(f"Detected Intent: {intent}")

#     # Step 2: Retrieve data
#     city = intent.get("city", "")
#     experience = intent.get("experience", "")
#     role = intent.get("role", "")   # NEW addition

#     retrieved_data = retrieve_data(processed_query, city, experience, role)

#     # Step 3: Extract context
#     context = extract_context_and_sources(retrieved_data)

#     # Step 4: Build search prompt
#     prompt = generate_prompt(processed_query, city)

#     # Step 5: Generate final answer
#     answer = generate_answer(prompt, context)

#     return answer






# from retriever.retriever import or_search_query, elastic_query, get_data_from_elk, get_context_sources
# from models.llm_models import generate_response
# from prompt_engineering.prompts import handle_query
# from utility import process_query
# from typing import List, Dict
# from intent_detection import build_intent_prompt, clean_intent_response   

# # Step 1: Retrieve relevant data
# def retrieve_data(query: str, location: str, experience: str, role: str):
#     if location or experience or role:
#         query_body = elastic_query(location, experience, role)
#     else:
#         query_body = or_search_query(query)
#     return get_data_from_elk(query_body)

# # Step 2: Extract context
# def extract_context_and_sources(results):
#     return get_context_sources(results)

# # Step 3: Build job search prompt
# def generate_prompt(query: str, city: str = None):
#     base_prompt = handle_query(query, city)
#     instruction = (
#         "Please present the job opportunities in a friendly, empathetic tone. "
#         "Avoid harsh critique. If any job details are missing (like salary or description), "
#         "mention it gently and offer to help find more details. Structure each job listing like:\n\n"
#         "- **Job Title**: \n- **Location**: \n- **Company**: \n- **Salary** (if available): \n- **Description**: \n"
#         "- **Apply Link** (if available): \n\n"
#         "Only include the job data provided. If no jobs are found, offer encouragement and ask if the user wants to adjust location or role."
#     )
#     return f"{base_prompt}\n\n{instruction}\n\nHere are some jobs I found:\n"

# # Step 4: Final response
# def generate_answer(prompt: str, context: str):
#     full_prompt = f"{prompt}\n{context}"
#     return generate_response(full_prompt)

# # Main rag + intent detection pipeline
# def rag_pipeline(query: str):
#     # Step 0: Preprocess user query
#     processed_query = process_query(query)
#     print("Processed Query:", processed_query)

#     # Step 1: Intent detection
#     intent_prompt = build_intent_prompt(processed_query)
#     intent_response_raw = generate_response(intent_prompt, max_tokens=300)
#     intent = clean_intent_response(intent_response_raw)

#     print(f"Detected Intent: {intent}")

#     # Step 2: Retrieve data
#     city = intent.get("city", "")
#     experience = intent.get("experience", "")
#     role = intent.get("role", "")   # NEW addition

#     retrieved_data = retrieve_data(processed_query, city, experience, role)

#     # Step 3: Extract context
#     context = extract_context_and_sources(retrieved_data)

#     # Step 4: Build search prompt
#     prompt = generate_prompt(processed_query, city)

#     # Step 5: Generate final answer
#     answer = generate_answer(prompt, context)

#     return answer






# from retriever.retriever import or_search_query, elastic_query, get_data_from_elk, get_context_sources
# from models.llm_models import generate_response
# from prompt_engineering.prompts import handle_query
# from utility import process_query
# from typing import List, Dict
# from intent_detection import build_intent_prompt, clean_intent_response

# # Step 1: Retrieve relevant data
# def retrieve_data(query: str, location: str, experience: str, role: str):
#     # Try full search with role
#     if location or experience or role:
#         query_body = elastic_query(location=location, experience=experience, role=role)
#         results = get_data_from_elk(query_body)
        
#         # SMART FALLBACK: If no results and role was used, retry without role
#         if not results and role:
#             print("[Fallback] No results found with role. Retrying without role...")
#             query_body = elastic_query(location=location, experience=experience)
#             results = get_data_from_elk(query_body)
#     else:
#         # If no structured info, fallback to keyword search
#         query_body = or_search_query(query)
#         results = get_data_from_elk(query_body)

#     return results

# # Step 2: Extract context
# def extract_context_and_sources(results):
#     return get_context_sources(results)

# # Step 3: Build job search prompt
# def generate_prompt(query: str, city: str = None):
#     base_prompt = handle_query(query, city)
#     instruction = (
#         "Please present the job opportunities in a friendly, empathetic tone. "
#         "Avoid harsh critique. If any job details are missing (like salary or description), "
#         "mention it gently and offer to help find more details. Structure each job listing like:\n\n"
#         "- **Job Title**: \n- **Location**: \n- **Company**: \n- **Salary** (if available): \n- **Description**: \n"
#         "- **Apply Link** (if available): \n\n"
#         "Only include the job data provided. If no jobs are found, offer encouragement and ask if the user wants to adjust location or role."
#     )
#     return f"{base_prompt}\n\n{instruction}\n\nHere are some jobs I found:\n"

# # Step 4: Final response
# def generate_answer(prompt: str, context: str):
#     full_prompt = f"{prompt}\n{context}"
#     return generate_response(full_prompt)

# # Main rag + intent detection pipeline
# def rag_pipeline(query: str):
#     # Step 0: Preprocess user query
#     processed_query = process_query(query)
#     print("Processed Query:", processed_query)

#     # Step 1: Intent detection
#     intent_prompt = build_intent_prompt(processed_query)
#     intent_response_raw = generate_response(intent_prompt, max_tokens=300)
#     intent = clean_intent_response(intent_response_raw)

#     print(f"Detected Intent: {intent}")

#     # Step 2: Retrieve data
#     city = intent.get("city", "")
#     experience = intent.get("experience", "")
#     role = intent.get("role", "")
#     retrieved_data = retrieve_data(processed_query, city, experience, role)

#     # Step 3: Extract context
#     context = extract_context_and_sources(retrieved_data)

#     # Step 4: Build search prompt
#     prompt = generate_prompt(processed_query, city)

#     # Step 5: Generate final answer
#     answer = generate_answer(prompt, context)

#     return answer



# from retriever.retriever import or_search_query, elastic_query, get_data_from_elk, get_context_sources
# from models.llm_models import generate_response
# from prompt_engineering.prompts  import handle_query
# from utility import process_query
# from typing import List


# # Step 1: Retrieve relevant data
# def retrieve_data(query: str, location: str, category: str, experience: str):
#     if location or category or experience:
#         query_body = elastic_query(location, category, experience)
#     else:
#         query_body = or_search_query(query)
#     return get_data_from_elk(query_body)

# # Step 2: Extract context
# def extract_context_and_sources(results):
#     return get_context_sources(results)

# # Step 3: Build a prompt using context and empathy
# def generate_prompt(query: str, category: str, city: str = None):
#     base_prompt = handle_query(query, category, city)
#     return f"{base_prompt}\n\nHere are some jobs I found:\n"

# # Step 4: Generate final answer using LLM
# def generate_answer(prompt: str, context: str):
#     full_prompt = f"{prompt}\n{context}"
#     return generate_response(full_prompt)

# # Main pipeline function
# def rag_pipeline(query: str, location: str = "", category: str = "", experience: str = "", city: str = None):
    
#     # Step 0: Preprocess the query
#     processed_query = process_query(query)
#     print("processed_query", processed_query)
    
#     # Step 1: Retrieve data from Elasticsearch
#     retrieved_data = retrieve_data(processed_query, location, category, experience)
    
#     # Step 2: Extract context and sources
#     context = extract_context_and_sources(retrieved_data)
    
#     # Step 3: Generate the prompt
#     prompt = generate_prompt(processed_query, category, city)
    
#     # Step 4: Generate the answer using the RAG model
#     answer = generate_answer(prompt, context)
    
#     return answer

# 



# from retriever.retriever import or_search_query, elastic_query, get_data_from_elk, get_context_sources
# from models.llm_models import generate_response
# from prompt_engineering.prompts import handle_query
# from intent_detection import build_intent_prompt  # (new import for intent detection)
# from utility import process_query
# from typing import List, Dict
# import json

# # Step 1: Retrieve relevant data
# def retrieve_data(query: str, location: str, category: str, experience: str):
#     if location or category or experience:
#         query_body = elastic_query(location, category, experience)
#     else:
#         query_body = or_search_query(query)
#     return get_data_from_elk(query_body)

# # Step 2: Extract context
# def extract_context_and_sources(results):
#     return get_context_sources(results)

# # New Step: Detect intent from query
# def detect_intent_entities(query: str) -> dict:
#     """
#     Detect city, category, salary, experience from the query.
#     """
#     intent_prompt = build_intent_prompt(query)
#     response = generate_response(intent_prompt, max_tokens=200)

#     # Safely parse JSON
#     try:
#         result = json.loads(response)
#     except Exception as e:
#         print("Failed to parse intent response:", response)
#         result = {"city": "", "category": "", "salary": "", "experience": ""}
#     return result

# # Step 3: Generate user-friendly prompt
# def generate_prompt(query: str, category: str, city: str = None):
#     base_prompt = handle_query(query, category, city)
#     instruction = (
#         "Please present the job opportunities in a friendly, empathetic tone. "
#         "Avoid harsh critique. If any job details are missing (like salary or description), "
#         "mention it gently and offer to help find more details. Structure each job listing like:\n\n"
#         "- **Job Title**: \n- **Location**: \n- **Company**: \n- **Salary** (if available): \n- **Description**: \n"
#         "- **Apply Link** (if available): \n\n"
#         "Only include the job data provided. If no jobs are found, offer encouragement and ask if the user wants to adjust location or role."
#     )
#     return f"{base_prompt}\n\n{instruction}\n\nHere are some jobs I found:\n"

# # Step 4: Generate final answer
# def generate_answer(prompt: str, context: str):
#     full_prompt = f"{prompt}\n{context}"
#     return generate_response(full_prompt)

# # Main RAG Pipeline
# def rag_pipeline(query: str):
#     # Step 0: Preprocess the query
#     processed_query = process_query(query)
#     print("processed_query:", processed_query)

#     # Step 1: Detect intent (First Gemini API call)
#     detected_entities = detect_intent_entities(processed_query)

#     city = detected_entities.get("city", "")
#     category = detected_entities.get("category", "")
#     experience = detected_entities.get("experience", "")

#     print(f"Detected: city={city}, category={category}, experience={experience}")

#     # Step 2: Retrieve data (based on detected info)
#     retrieved_data = retrieve_data(processed_query, city, category, experience)

#     # Step 3: Extract context
#     context = extract_context_and_sources(retrieved_data)

#     # Step 4: Build prompt
#     prompt = generate_prompt(processed_query, category, city)

#     # Step 5: Final answer (Second Gemini API call)
#     answer = generate_answer(prompt, context)

#     return answer

# from retriever.retriever import or_search_query, elastic_query, get_data_from_elk, get_context_sources
# from models.llm_models import generate_response
# from prompt_engineering.prompts import handle_query
# from utility import process_query
# from typing import List, Dict
# from intent_detection import build_intent_prompt, clean_intent_response   

# # Step 1: Retrieve relevant data


# def retrieve_data(query: str, location: str, experience: str):
#     if location or experience:
#         query_body = elastic_query(location, experience)
#     else:
#         query_body = or_search_query(query)
#     return get_data_from_elk(query_body)

# # Step 2: Extract context
# def extract_context_and_sources(results):
#     return get_context_sources(results)

# # Step 3: Build job search prompt
# def generate_prompt(query: str, city: str = None):
#     base_prompt = handle_query(query, city)
#     instruction = (
#         "Please present the job opportunities in a friendly, empathetic tone. "
#         "Avoid harsh critique. If any job details are missing (like salary or description), "
#         "mention it gently and offer to help find more details. Structure each job listing like:\n\n"
#         "- **Job Title**: \n- **Location**: \n- **Company**: \n- **Salary** (if available): \n- **Description**: \n"
#         "- **Apply Link** (if available): \n\n"
#         "Only include the job data provided. If no jobs are found, offer encouragement and ask if the user wants to adjust location or role."
#     )
#     return f"{base_prompt}\n\n{instruction}\n\nHere are some jobs I found:\n"

# # Step 4: Final response
# def generate_answer(prompt: str, context: str):
#     full_prompt = f"{prompt}\n{context}"
#     return generate_response(full_prompt)

# # Main rag + intent detection pipeline
# def rag_pipeline(query: str):
#     # Step 0: Preprocess user query
#     processed_query = process_query(query)
#     print("Processed Query:", processed_query)

#     # Step 1: Intent detection
#     intent_prompt = build_intent_prompt(processed_query)
#     intent_response_raw = generate_response(intent_prompt, max_tokens=300)
#     intent = clean_intent_response(intent_response_raw)

#     print(f"Detected Intent: {intent}")

#     # Step 2: Retrieve data
#     city = intent.get("city", "")
#     experience = intent.get("experience", "")
#     retrieved_data = retrieve_data(processed_query, city, experience)

#     # Step 3: Extract context
#     context = extract_context_and_sources(retrieved_data)

#     # Step 4: Build search prompt
#     prompt = generate_prompt(processed_query, city)

#     # Step 5: Generate final answer
#     answer = generate_answer(prompt, context)

#     return answer
