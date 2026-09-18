"""
TEST 3: Structured JSON input handling.
Verifies that the system accepts and correctly processes structured JSON input.
"""

import pytest
from src.api.server import chat_endpoint, analyze_structured_profile
from src.models.schemas import ChatRequest, EnvironmentalProfile, GeoCoordinates


@pytest.mark.asyncio
async def test_structured_profile_direct():
    profile = EnvironmentalProfile(
        soil_ph=6.5,
        soil_organic_carbon=0.3,
        soil_moisture="low",
        rainfall="low",
        temperature="high",
        land_use="monoculture wheat",
        species_richness="low",
        habitat_diversity="low",
        pollution="none",
        deforestation="none",
        region="semi-arid",
        geo_coordinates=GeoCoordinates(latitude=31.5, longitude=-102.3)
    )

    reasoning = await analyze_structured_profile(profile)
    assert reasoning.status == "complete"
    assert reasoning.variables_analyzed.get("soil_organic_carbon") == 0.3
    assert reasoning.variables_analyzed.get("soil_ph") == 6.5
    assert len(reasoning.recommendations) > 0


@pytest.mark.asyncio
async def test_structured_profile_via_chat_endpoint():
    profile = EnvironmentalProfile(
        soil_organic_carbon=0.5,
        rainfall="low",
        land_use="monoculture cereal"
    )
    req = ChatRequest(
        structured_data=profile,
        session_id="test_structured_chat_session"
    )
    res = await chat_endpoint(req)
    assert res.status == "complete"
    assert res.variables_in_context.get("soil_organic_carbon") == 0.5
