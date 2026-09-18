"""
TEST 2: Multi-metric scenario reasoning.
Verifies the exact use case from the Darukaa challenge PDF:
- Soil organic carbon: 0.3%
- Rainfall: low
- Crop: monoculture wheat
- Region: semi-arid
"""

import pytest
from src.api.server import chat_endpoint
from src.models.schemas import ChatRequest


@pytest.mark.asyncio
async def test_multi_metric_scenario():
    user_query = "Soil organic carbon: 0.3%, rainfall: low, crop: monoculture wheat, region: semi-arid"
    req = ChatRequest(message=user_query, session_id="test_multi_metric_session")
    res = await chat_endpoint(req)

    assert res.status == "complete", "System should complete analysis when >= 3 variables are present"
    assert res.analysis is not None, "Analysis output must be generated"
    
    # Check that variables were correctly extracted
    vars_detected = res.variables_in_context
    assert vars_detected.get("soil_organic_carbon") == 0.3
    assert vars_detected.get("rainfall") == "low"
    assert "wheat" in str(vars_detected.get("land_use"))

    # Check that multi-metric causal reasoning was performed (>= 3 variables)
    assert len(res.analysis.causal_relationships) > 0
    causal_text = " ".join(res.analysis.causal_relationships)
    assert "Soil" in causal_text or "Carbon" in causal_text
    assert "Water" in causal_text or "Rainfall" in causal_text

    # Check that recommendations are concrete, non-obvious, and backed by evidence
    assert len(res.analysis.recommendations) > 0
    rec = res.analysis.recommendations[0]
    assert rec.what_to_do is not None and len(rec.what_to_do) > 10
    assert rec.why_it_works is not None and len(rec.why_it_works) > 15
    assert len(rec.impacted_metrics) >= 1
    assert rec.time_horizon in ["short_term", "medium_term", "long_term"]
    assert rec.quantitative_estimate is not None

    # Check that credible citations exist
    assert len(rec.citations) > 0
    sources = [c.source_org for c in rec.citations]
    assert any("FAO" in s or "IPCC" in s for s in sources)
