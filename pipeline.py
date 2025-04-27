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


