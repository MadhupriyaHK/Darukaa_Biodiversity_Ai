"""
TEST 4: Multi-turn conversation context and memory.
Verifies that information provided in earlier turns is retained and reused across turns.
"""

import pytest
from src.api.server import chat_endpoint
from src.models.schemas import ChatRequest


@pytest.mark.asyncio
async def test_multi_turn_memory_persistence():
    session_id = "test_turn_persistence_session"

    # Turn 1: Incomplete statement
    req_1 = ChatRequest(message="Biodiversity is declining on my land.", session_id=session_id)
    res_1 = await chat_endpoint(req_1)
    assert res_1.status == "clarification_needed"
    assert res_1.variables_in_context.get("species_richness") == "low"

    # Turn 2: User provides soil organic carbon only
    req_2 = ChatRequest(message="The soil organic carbon is 0.3%.", session_id=session_id)
    res_2 = await chat_endpoint(req_2)
    # Memory should retain species_richness from Turn 1 AND soil_organic_carbon from Turn 2
    assert res_2.variables_in_context.get("species_richness") == "low"
    assert res_2.variables_in_context.get("soil_organic_carbon") == 0.3

    # Turn 3: User provides rainfall and land use
    req_3 = ChatRequest(message="Rainfall is low and I have monoculture wheat.", session_id=session_id)
    res_3 = await chat_endpoint(req_3)
    assert res_3.status == "complete"
    assert res_3.variables_in_context.get("species_richness") == "low"
    assert res_3.variables_in_context.get("soil_organic_carbon") == 0.3
    assert res_3.variables_in_context.get("rainfall") == "low"
    assert "wheat" in str(res_3.variables_in_context.get("land_use"))
