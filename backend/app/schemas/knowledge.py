"""Pydantic schemas for knowledge-related requests and responses."""
from pydantic import BaseModel, Field


class QAPair(BaseModel):
    """Schema for Q&A pair."""
    question: str = Field(..., min_length=1, max_length=500, description="Question")
    answer: str = Field(..., min_length=1, max_length=2000, description="Answer")


class QAPairResponse(BaseModel):
    """Schema for Q&A pair response."""
    id: int
    question: str
    answer: str
