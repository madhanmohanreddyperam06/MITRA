from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn

from nlp_pipeline import NLPPipeline
from knowledge_base import KnowledgeBase
from response_generator import ResponseGenerator

app = FastAPI(title="Smart College Helpdesk Bot API", version="1.0.0")

# Enable CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Streamlit domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
nlp_pipeline = NLPPipeline()
knowledge_base = KnowledgeBase()
response_generator = ResponseGenerator(knowledge_base)

class ChatRequest(BaseModel):
    user_input: str
    user_context: Dict[str, Any] = {}
    conversation_history: List[Dict[str, str]] = []

class ChatResponse(BaseModel):
    response: str
    intent: str = ""
    confidence: float = 0.0
    entities: List[Dict[str, str]] = []

class QAPair(BaseModel):
    question: str
    answer: str

@app.get("/")
async def root():
    return {"message": "Smart College Helpdesk Bot API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "college-helpdesk-bot"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Process user input through NLP pipeline
        processed_input = nlp_pipeline.process(request.user_input)

        # Extract intent and entities
        intent = processed_input.get("intent", "general")
        entities = processed_input.get("entities", [])
        confidence = processed_input.get("confidence", 0.0)

        # Generate response using the response generator
        response = response_generator.generate_response(
            intent=intent,
            entities=entities,
            user_input=request.user_input,
            user_context=request.user_context,
            conversation_history=request.conversation_history
        )

        return ChatResponse(
            response=response,
            intent=intent,
            confidence=confidence,
            entities=entities
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.post("/qa")
async def add_qa_pair(qa_pair: QAPair):
    try:
        qa_id = knowledge_base.add_qa_pair(qa_pair.question, qa_pair.answer)
        return {"message": "Q&A pair added successfully", "id": qa_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding Q&A pair: {str(e)}")

@app.get("/qa", response_model=List[QAPair])
async def get_qa_pairs(question: str = None):
    try:
        qa_pairs = knowledge_base.get_qa_pairs(question)
        return qa_pairs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving Q&A pairs: {str(e)}")

@app.get("/intents")
async def get_available_intents():
    """Get list of available intents"""
    return {
        "intents": [
            "admission_info",
            "course_info", 
            "fee_inquiry",
            "hostel_info",
            "library_info",
            "placement_info",
            "contact_info",
            "general_info"
        ]
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
