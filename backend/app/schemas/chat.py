"""Pydantic schemas for chat-related requests and responses."""
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any


class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""
    user_input: str = Field(..., min_length=1, max_length=1000, description="User's message")
    user_context: Dict[str, Any] = Field(default_factory=dict, description="Additional user context")
    conversation_history: List[Dict[str, str]] = Field(default_factory=list, description="Conversation history")

    @field_validator('user_input')
    @classmethod
    def validate_user_input(cls, v: str) -> str:
        """Validate user input is not empty or just whitespace."""
        if not v or not v.strip():
            raise ValueError("user_input cannot be empty")
        return v.strip()

    @field_validator('conversation_history')
    @classmethod
    def validate_conversation_history(cls, v: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Validate conversation history length."""
        if len(v) > 20:
            raise ValueError("conversation_history cannot exceed 20 entries")
        return v


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""
    response: str = Field(..., description="Generated response")
    intent: str = Field(default="", description="Detected intent")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Confidence score")
    entities: List[Dict[str, str]] = Field(default_factory=list, description="Extracted entities")
