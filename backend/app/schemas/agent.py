"""Agent execution request/response schemas."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, field_serializer


class AgentRunRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    agents: Optional[List[str]] = None


class AgentRunResponse(BaseModel):
    session_id: str
    status: str
    agents_executed: List[str]
    result: Dict[str, Any]
    reasoning: Optional[str] = None
    tokens_used: int = 0
    execution_time_ms: float = 0.0


class AgentLogResponse(BaseModel):
    id: Any
    session_id: str
    agent_name: str
    action: Optional[str] = None
    status: str
    reasoning: Optional[str] = None
    tokens_used: int = 0
    execution_time_ms: Optional[float] = None
    created_at: str

    @field_serializer('id')
    def serialize_uuid(self, v: Any) -> str:
        return str(v)

    model_config = {"from_attributes": True}


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    history: List[ChatMessage] = []
