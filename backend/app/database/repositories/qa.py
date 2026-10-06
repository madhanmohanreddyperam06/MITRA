"""Repository for Q&A data access."""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database.models import QADataset
from app.core.exceptions import DatabaseError


class QARepository:
    """Repository for Q&A-related database operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all Q&A pairs."""
        try:
            result = self.db.execute(select(QADataset))
            qa_pairs = result.scalars().all()
            return [
                {
                    "id": qa.id,
                    "question": qa.question,
                    "answer": qa.answer
                }
                for qa in qa_pairs
            ]
        except Exception as e:
            raise DatabaseError(f"Failed to fetch Q&A pairs: {e}")

    def search_by_question(self, question: str) -> List[Dict[str, Any]]:
        """Search Q&A pairs by question (partial match)."""
        try:
            result = self.db.execute(
                select(QADataset).where(QADataset.question.like(f"%{question}%"))
            )
            qa_pairs = result.scalars().all()
            return [
                {
                    "id": qa.id,
                    "question": qa.question,
                    "answer": qa.answer
                }
                for qa in qa_pairs
            ]
        except Exception as e:
            raise DatabaseError(f"Failed to search Q&A pairs: {e}")

    def get_by_id(self, qa_id: int) -> Optional[Dict[str, Any]]:
        """Get Q&A pair by ID."""
        try:
            qa = self.db.get(QADataset, qa_id)
            if qa:
                return {
                    "id": qa.id,
                    "question": qa.question,
                    "answer": qa.answer
                }
            return None
        except Exception as e:
            raise DatabaseError(f"Failed to fetch Q&A pair by ID: {e}")

    def add(self, question: str, answer: str) -> int:
        """Add a new Q&A pair."""
        try:
            qa = QADataset(question=question, answer=answer)
            self.db.add(qa)
            self.db.commit()
            self.db.refresh(qa)
            return qa.id
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to add Q&A pair: {e}")
