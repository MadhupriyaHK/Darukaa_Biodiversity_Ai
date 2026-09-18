"""
Multi-turn Conversation Memory and State Manager.
Maintains session history, persists accumulated environmental variables across turns,
and prevents re-asking for already provided information.
"""

import uuid
from typing import Dict, Any, List, Optional
from src.models.schemas import ChatMessage


class ConversationSession:
    """Represents an active multi-turn conversation session."""

    def __init__(self, session_id: Optional[str] = None):
        self.session_id: str = session_id or str(uuid.uuid4())
        self.history: List[ChatMessage] = []
        self.accumulated_variables: Dict[str, Any] = {}
        self.last_clarification_asked: List[str] = []

    def add_message(self, role: str, content: str) -> None:
        self.history.append(ChatMessage(role=role, content=content))

    def update_variables(self, new_variables: Dict[str, Any]) -> None:
        """Merges new environmental parameters into existing memory."""
        for k, v in new_variables.items():
            if v is not None:
                self.accumulated_variables[k] = v

    def get_variables(self) -> Dict[str, Any]:
        return dict(self.accumulated_variables)

    def clear(self) -> None:
        self.history.clear()
        self.accumulated_variables.clear()
        self.last_clarification_asked.clear()


class MemoryManager:
    """Manages active conversation sessions in-memory."""

    def __init__(self):
        self.sessions: Dict[str, ConversationSession] = {}

    def get_or_create_session(self, session_id: Optional[str] = None) -> ConversationSession:
        if session_id and session_id in self.sessions:
            return self.sessions[session_id]

        new_id = session_id or str(uuid.uuid4())
        session = ConversationSession(session_id=new_id)
        self.sessions[new_id] = session
        return session

    def reset_session(self, session_id: str) -> bool:
        if session_id in self.sessions:
            self.sessions[session_id].clear()
            return True
        return False
