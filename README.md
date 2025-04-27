# Asha-Hackathon

# Asha: Your Partner in Every Career Dream
This project is a modular job search assistant with empathetic, intent-based responses. It integrates a conversational bot with a job search system, providing personalized job recommendations and additional features like LinkedIn networking in the future.
# Architecture Overview:
	• Frontend: Collects user input through Gradio.
	• API Layer: FastAPI processes the data and communicates with other components.
	• Intent Detection: Uses a Large Language Model (LLM) to detect user intent (job role, city, experience).
	• Retriever: Fetches job data from an Elasticsearch index containing 30K+ job records from Kaggle.
	• Response Generation: Empathetic responses are generated and shown to the user.
# Technologies Used:
	• Gradio: For building the frontend interface.
	• FastAPI: For API layer handling requests and responses.
	• OpenAI models: For intent detection and natural language processing.
	• Elasticsearch: To store and query the job dataset.
	• Redis (Future Integration): For session memory to remember user context.
	• LinkedIn API (Future Integration): To recommend professional connections based on job selections.
# Setup Instructions:
	• Install required Python libraries (FastAPI, Gradio, OpenAI, Elasticsearch client)
	• Set up an Elasticsearch server with the job dataset (30K+ jobs from Kaggle)
	• Run FastAPI server and Gradio frontend simultaneously
	• Connect frontend to backend through API calls
# Integration Process:
	1. User Input: User sends a query via Gradio interface.
	2. FastAPI: The query is processed by FastAPI and passed to the Intent Detection module.
	3. Intent Detection: The LLM detects user intent (city, job role, experience).
	4. Job Retrieval: The retriever queries Elasticsearch to fetch relevant job data.
	5. Empathetic Response Generation: The system generates a personalized, empathetic response based on the retrieved job data.
	6. Display Response: The generated response is displayed back to the user via Gradio interface.
# Future Enhancements:
	• Session Memory: Redis will be used to store user session context, enabling the assistant to remember previous interactions.
	• LinkedIn Integration: The LinkedIn API will be integrated to suggest professional connections from the selected job companies.
