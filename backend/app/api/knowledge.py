"""API router for knowledge management endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.repositories.qa import QARepository
from app.schemas.knowledge import QAPair, QAPairResponse
from app.core.logging import logger
from app.core.exceptions import MITRAError
from app.core.security import get_current_active_user

router = APIRouter()


@router.post("/qa", response_model=dict)
async def add_qa_pair(
    qa_pair: QAPair,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Add a new Q&A pair to the knowledge base.

    This endpoint allows adding new question-answer pairs to the dataset.
    Requires authentication.
    """
    logger.info(f"Adding Q&A pair: {qa_pair.question[:50]}...")

    try:
        qa_repo = QARepository(db)
        qa_id = qa_repo.add(qa_pair.question, qa_pair.answer)

        logger.info(f"Successfully added Q&A pair with ID: {qa_id}")

        return {"message": "Q&A pair added successfully", "id": qa_id}

    except MITRAError as e:
        logger.error(f"MITRA error adding Q&A pair: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error adding Q&A pair: {e}")
        raise


@router.get("/qa")
async def get_qa_pairs(
    question: str = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Retrieve Q&A pairs from the knowledge base.

    Optionally filter by question text (partial match).
    Requires authentication.
    """
    logger.info(f"Retrieving Q&A pairs with filter: {question}")

    try:
        qa_repo = QARepository(db)

        if question:
            qa_pairs = qa_repo.search_by_question(question)
        else:
            qa_pairs = qa_repo.get_all()

        logger.info(f"Retrieved {len(qa_pairs)} Q&A pairs")

        return qa_pairs

    except MITRAError as e:
        logger.error(f"MITRA error retrieving Q&A pairs: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error retrieving Q&A pairs: {e}")
        raise
