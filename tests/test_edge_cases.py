"""
TEST 6: Edge cases, input validation, and graceful degradation.
Verifies error handling, out-of-range metrics, and absence of hallucinated claims.
"""

import pytest
from pydantic import ValidationError
from src.models.schemas import EnvironmentalProfile
from src.reasoning.variable_extractor import EnvironmentalVariableExtractor
from src.api.server import chat_endpoint
from src.models.schemas import ChatRequest


def test_invalid_soil_ph_raises_validation_error():
    with pytest.raises(ValidationError):
        EnvironmentalProfile(soil_ph=15.5)  # pH must be <= 14.0

    with pytest.raises(ValidationError):
        EnvironmentalProfile(soil_ph=-1.0)  # pH must be >= 0.0


def test_normalizer_handles_malformed_text():
    extracted = EnvironmentalVariableExtractor.extract_from_text(
        "Random gibberish with no ecological variables 12345!@#$"
    )
    assert len(extracted) == 0


@pytest.mark.asyncio
async def test_empty_message_handling():
    req = ChatRequest(message="", session_id="empty_session")
    res = await chat_endpoint(req)
    assert res.status == "clarification_needed"
    assert len(res.clarifying_questions) > 0
