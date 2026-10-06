"""API router for chat endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.repositories.admissions import AdmissionRepository
from app.database.repositories.courses import CourseRepository
from app.database.repositories.facilities import FacilityRepository
from app.database.repositories.contacts import ContactRepository
from app.database.repositories.qa import QARepository
from typing import Optional
from app.services.chat_service import ChatService
from app.schemas.chat import ChatRequest, ChatResponse
from app.core.logging import logger
from app.core.exceptions import MITRAError
from app.core.security import get_optional_current_user
from app.nlp_pipeline import NLPPipeline

router = APIRouter()

# Initialize NLP pipeline (stateless, can be global)
nlp_pipeline = NLPPipeline()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: Optional[dict] = Depends(get_optional_current_user)
):
    """
    Process user chat message and generate response.

    This endpoint:
    1. Processes user input through NLP pipeline
    2. Extracts intent and entities
    3. Retrieves relevant information from database
    4. Generates appropriate response

    Supports both authenticated users and guest visitors.
    """
    user_str = f"user {current_user['id']}" if current_user else "anonymous guest"
    logger.info(f"Received chat request from {user_str}: {request.user_input[:50]}...")

    try:
        # Process user input through NLP pipeline
        processed_input = nlp_pipeline.process(request.user_input)

        # Extract intent and entities
        intent = processed_input.get("intent", "general")
        entities = processed_input.get("entities", [])
        confidence = processed_input.get("confidence", 0.0)

        # Log confidence level
        if confidence < 0.5:
            logger.warning(f"Low confidence detected: {confidence} for intent: {intent}")

        # Initialize repositories
        admission_repo = AdmissionRepository(db)
        course_repo = CourseRepository(db)
        facility_repo = FacilityRepository(db)
        contact_repo = ContactRepository(db)
        qa_repo = QARepository(db)

        # Initialize service
        chat_service = ChatService(
            admission_repo=admission_repo,
            course_repo=course_repo,
            facility_repo=facility_repo,
            contact_repo=contact_repo,
            qa_repo=qa_repo
        )

        # Generate response using the service
        response = chat_service.process_query(
            intent=intent,
            entities=entities,
            user_input=request.user_input,
            user_context=request.user_context,
            conversation_history=request.conversation_history
        )

        logger.info(f"Generated response for intent: {intent}")

        return ChatResponse(
            response=response,
            intent=intent,
            confidence=confidence,
            entities=entities
        )

    except MITRAError as e:
        logger.error(f"MITRA error in chat endpoint: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {e}")
        raise
