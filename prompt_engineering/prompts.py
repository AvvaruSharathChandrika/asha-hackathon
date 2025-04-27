
# def welcome_message():
#     return "Hi there! I'm here to help you find the perfect job with a warm heart. 😊 What kind of job are you looking for today?"

# def category_prompt(category):
#     if category == "starters":
#         return "It’s wonderful that you’re just starting your career journey! I’m sure we’ll find the right opportunities for you. 💼✨"
#     elif category == "restartes":
#         return "Welcome back to the workforce! Let’s find something that fits your unique skills and experiences. 🌟💪"
#     elif category == "re-risers":
#         return "I’m inspired by your resilience! Let’s search for roles that align with your strength and new ambitions. 🌱💖"
#     else:
#         return "I see you're looking for something specific. Let me know the type of role or category you're interested in!"

# def city_response(city):
#     city = city.lower()
#     if city == "jaipur":
#         return "Ah, the Pink City! 🌸 Jaipur is known for its beautiful architecture and vibrant culture. Let me find some amazing job opportunities for you in this lovely city."
#     elif city == "delhi":
#         return "Delhi, the city of endless opportunities! 🌆 Let’s find you a job that makes your heart sing in this bustling metropolis."
#     elif city == "bangalore":
#         return "Bangalore, the Silicon Valley of India! 🌐 Looking for tech opportunities or something else? Let me help you find a perfect match."
#     elif city == "hyderabad":
#         return "Hyderabad, the city of pearls and a hub for tech and innovation! 🏙️ Whether you’re in IT or another field, let’s explore the amazing opportunities here."
#     elif city == "pune":
#         return "Pune, a city of education and growth! 🎓 Whether you’re looking for IT, education, or any other field, Pune has something wonderful to offer."
#     elif city == "kolkata":
#         return "Kolkata, the city of joy! 🎉 Known for its rich culture, art, and history, it’s a place full of opportunities. Let’s find a great job for you here."
#     elif city == "mumbai":
#         return "Mumbai, the city that never sleeps! 🌃 From finance to media, it’s the heart of opportunity in India. Let’s find your dream job in this dynamic city."
#     elif city == "chennai":
#         return "Chennai, a hub for IT, automobile, and more! 🚗 Let’s find you a job that suits your skills in this vibrant and diverse city."
#     elif city == "bengaluru":
#         return "Bengaluru, the tech capital of India! 💻 With its thriving startup ecosystem, let’s explore tech jobs or others that catch your interest."
#     elif city == "ahmedabad":
#         return "Ahmedabad, a growing city known for its industries and vibrant culture! 🎨 Whether you’re looking for corporate roles or creative ones, Ahmedabad has options."
#     elif city == "chandigarh":
#         return "Chandigarh, the beautiful city of modern design and greenery! 🌳 A mix of culture and opportunities, let’s find the best job for you in this scenic city."
#     elif city == "indore":
#         return "Indore, the cleanest city in India! 🏙️ Known for its educational institutes and vibrant economy, let’s find some amazing jobs in this fast-growing city."
#     elif city == "coimbatore":
#         return "Coimbatore, a blend of tradition and modern industry! 🌟 Known for engineering and textiles, let’s find a role that suits you perfectly in this lovely city."
#     elif city == "nagpur":
#         return "Nagpur, the heart of India! ❤️ Known for its strong agricultural base and growing industries, let’s find a job that fits your needs here."
#     elif city == "surat":
#         return "Surat, the diamond city! 💎 Known for its textile industry and vibrant business scene, let's explore the job opportunities here."
#     elif city == "visakhapatnam":
#         return "Visakhapatnam, a coastal city with a growing industrial base! 🌊 Whether you're into IT, manufacturing, or something else, let’s find the right opportunity."
#     else:
#         return f"{city.title()} is a beautiful place! Let me help you explore jobs that can bring you closer to your dream career in this wonderful city."

# def job_found_response(job_count):
#     if job_count > 0:
#         return f"Yay! 🎉 I found {job_count} opportunities that might be a great fit for you. Let’s explore them together!"
#     else:
#         return "I’m sorry, it looks like there aren’t any jobs that match your exact preferences right now. But don’t worry, I’ll keep searching and let you know if anything pops up. 💡"

# def empathy_message():
#     return "Remember, no matter what, your journey is unique and valuable. If you ever need encouragement, I’m always here to support you. 💖💪"

# def query_reaction(query):
#     if "salary" in query.lower():
#         return "It’s important to feel confident about the compensation. Let’s make sure we find roles that align with your salary expectations. 💰"
#     elif "location" in query.lower():
#         return "Your ideal location matters, and I’ll be sure to find roles that meet your preferences. Let's look for jobs nearby! 🌍"
#     else:
#         return "I understand you’re looking for something special. Let’s keep digging to find the perfect match for you. 🔍✨"

# def goodbye_message():
#     return "Good luck on your job search journey! I believe in you and I’m here whenever you need me. 🌟 Don't hesitate to reach out if you need more help later!"

# # Function to handle the query response based on the context
# def handle_query(query, category=None, city=None):
#     # Apply empathy-based responses
#     if city:
#         return city_response(city)
#     elif category:
#         return category_prompt(category)
#     else:
#         return query_reaction(query)



def welcome_message():
    return "Hi there! I'm here to help you find the perfect job . 😊 What kind of job are you looking for today?"

def category_prompt(category):
    if category == "starters":
        return "It’s wonderful that you’re just starting your career journey! I’m sure we’ll find the right opportunities for you. 💼✨"
    elif category == "restartes":
        return "Welcome back to the workforce! Let’s find something that fits your unique skills and experiences. 🌟💪"
    elif category == "re-risers":
        return "I’m inspired by your resilience! Let’s search for roles that align with your strength and new ambitions. 🌱💖"
    else:
        return "I see you're looking for something specific. Let me know the type of role or category you're interested in!"

def city_response(city):
    responses = {
        "jaipur": "Ah, the Pink City! 🌸 Jaipur is known for its beautiful architecture and vibrant culture. Let me find some amazing job opportunities for you in this lovely city.",
        "delhi": "Delhi, the city of endless opportunities! 🌆 Let’s find you a job that makes your heart sing in this bustling metropolis.",
        "bangalore": "Bangalore, the Silicon Valley of India! 🌐 Looking for tech opportunities or something else? Let me help you find a perfect match.",
        "hyderabad": "Hyderabad, the city of pearls and a hub for tech and innovation! 🏙️ Whether you’re in IT or another field, let’s explore the amazing opportunities here.",
        "pune": "Pune, a city of education and growth! 🎓 Whether you’re looking for IT, education, or any other field, Pune has something wonderful to offer.",
        "kolkata": "Kolkata, the city of joy! 🎉 Known for its rich culture, art, and history, it’s a place full of opportunities. Let’s find a great job for you here.",
        "mumbai": "Mumbai, the city that never sleeps! 🌃 From finance to media, it’s the heart of opportunity in India. Let’s find your dream job in this dynamic city.",
        "chennai": "Chennai, a hub for IT, automobile, and more! 🚗 Let’s find you a job that suits your skills in this vibrant and diverse city.",
        "bengaluru": "Bengaluru, the tech capital of India! 💻 With its thriving startup ecosystem, let’s explore tech jobs or others that catch your interest.",
        "ahmedabad": "Ahmedabad, a growing city known for its industries and vibrant culture! 🎨 Whether you’re looking for corporate roles or creative ones, Ahmedabad has options.",
        "chandigarh": "Chandigarh, the beautiful city of modern design and greenery! 🌳 A mix of culture and opportunities, let’s find the best job for you in this scenic city.",
        "indore": "Indore, the cleanest city in India! 🏙️ Known for its educational institutes and vibrant economy, let’s find some amazing jobs in this fast-growing city.",
        "coimbatore": "Coimbatore, a blend of tradition and modern industry! 🌟 Known for engineering and textiles, let’s find a role that suits you perfectly in this lovely city.",
        "nagpur": "Nagpur, the heart of India! ❤️ Known for its strong agricultural base and growing industries, let’s find a job that fits your needs here.",
        "surat": "Surat, the diamond city! 💎 Known for its textile industry and vibrant business scene, let's explore the job opportunities here.",
        "visakhapatnam": "Visakhapatnam, a coastal city with a growing industrial base! 🌊 Whether you're into IT, manufacturing, or something else, let’s find the right opportunity."
    }
    return responses.get(city.lower(), f"{city.title()} is a beautiful place! Let me help you explore jobs that can bring you closer to your dream career in this wonderful city.")

def job_found_response(job_count):
    if job_count > 0:
        return f"Yay! 🎉 I found {job_count} opportunities that might be a great fit for you. Let’s explore them together!"
    else:
        return "I’m sorry, it looks like there aren’t any jobs that match your exact preferences right now. But don’t worry, I’ll keep searching and let you know if anything pops up. 💡"

def empathy_message():
    return "Remember, no matter what, your journey is unique and valuable. If you ever need encouragement, I’m always here to support you. 💖💪"

def query_reaction(query):
    if "salary" in query.lower():
        return "It’s important to feel confident about the compensation. Let’s make sure we find roles that align with your salary expectations. 💰"
    elif "location" in query.lower():
        return "Your ideal location matters, and I’ll be sure to find roles that meet your preferences. Let's look for jobs nearby! 🌍"
    else:
        return "I understand you’re looking for something special. Let’s keep digging to find the perfect match for you. 🔍✨"

def goodbye_message():
    return "Good luck on your job search journey! I believe in you and I’m here whenever you need me. 🌟 Don't hesitate to reach out if you need more help later!"

def handle_query(query, category=None, city=None):
    greeting = "Here's what I found for you! Let's take a look together:"
    if city:
        return f"{city_response(city)}\n\n{greeting}"
    elif category:
        return f"{category_prompt(category)}\n\n{greeting}"
    else:
        return f"{query_reaction(query)}\n\n{greeting}"



def generate_prompt(query: str, category: str, city: str = None):
    base_prompt = handle_query(query, category, city)
    instruction = (
        "Please present the job opportunities in a friendly, empathetic tone. "
        "Avoid harsh critique. If any job details are missing (like salary or description), "
        "mention it gently and offer to help find more details. Structure each job listing like:\n\n"
        "- **Job Title**: \n- **Location**: \n- **Company**: \n- **Salary** (if available): \n- **Description**: \n"
        "- **Apply Link** (if available): \n\n"
        "Only include the job data provided. If no jobs are found, offer encouragement and ask if the user wants to adjust location or role."
    )
    return f"{base_prompt}\n\n{instruction}\n\nHere are some jobs I found:\n"
