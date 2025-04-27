"""
This module is main entry point for the FastAPI application.
"""
import sys
import traceback
import uvicorn
import nltk
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Tuple

from pipeline import rag_pipeline

nltk.download('stopwords')
nltk.download('punkt')

# Initialize the FastAPI
app = FastAPI(title="ASHA BOT",
              description="Backend API for Asha Chatbot Application",
              version="0.1.0"
              )

origins = ["*"]
app.add_middleware(SessionMiddleware, secret_key="!secret")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Status"])
async def health_check():
    """A simple health check endpoint to verify the status of the API.

    Returns:
        JSONResponse (dict): A JSON response with status code and text
    """
    return JSONResponse(status_code=200, content={"status_code": 200,
                                                  "text": "I am up & running"}
                        )

class ChatInput(BaseModel):
    """
    Schema for user input to chatbot.
    """
    message: str
    history: List[Tuple[str, str]] = []

@app.post("/search", tags=["Search"])
async def search(search_input: ChatInput):
    """
    Performs a search using conversational input (message + history).
    """
    try:
        start_time = time.time()
        message = search_input.message
        history = search_input.history

        if message.strip() == "":
            return JSONResponse(status_code=601, content={"error": "Error: Message cannot be empty"})

        # Pass only the latest message to RAG (optionally: use history later)
        result = rag_pipeline(message)

        print(f"Message: {message} | Time : {round(time.time() - start_time, 2)} sec")

        return JSONResponse(status_code=200, content={"response": result})

    except Exception as exception:
        print(
            f"Internal Error at line no \
                {sys.exc_info()[-1].tb_lineno}|{traceback.print_exc()}|{type(exception).__name__}")
        print(traceback.print_exc())
        return JSONResponse(status_code=602,
                        content={"error": "Internal Error: Something went wrong while processing"})

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
