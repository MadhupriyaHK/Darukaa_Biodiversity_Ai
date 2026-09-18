"""
TEST 1: Incomplete biodiversity query handling.
Verifies that the system asks clarifying questions instead of giving generic recommendations.
"""

import pytest
from src.api.server import chat_endpoint
from src.models.schemas import ChatRequest


@pytest.mark.asyncio
async def test_incomplete_query_triggers_clarification():
    req = ChatRequest(
        message="Biodiversity is declining on my land.",
        session_id="test_incomplete_session"
    )
    res = await chat_endpoint(req)

    assert res.status == "clarification_needed", "System should require clarification for incomplete input"
    assert len(res.clarifying_questions) >= 2, "System must provide at least 2 targeted clarifying questions"
    
    # Check that questions target critical missing environmental parameters
    asked_vars = [q.variable for q in res.clarifying_questions]
    assert "soil_organic_carbon" in asked_vars or "rainfall" in asked_vars or "land_use" in asked_vars
    assert "Please provide the following environmental parameters" in res.reply
