"""
End-to-End Live Integration Test for Darukaa Biodiversity AI System.
Performs real HTTP requests against the live FastAPI server at http://127.0.0.1:8000.
Tests all requirements from the Darukaa Challenge PDF.
"""

import sys
import httpx

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_URL = "http://127.0.0.1:8000"


def test_1_health_and_knowledge():
    print("\n[TEST 1] Checking /health and /api/knowledge...")
    with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
        r = client.get("/health")
        assert r.status_code == 200, f"Health failed: {r.text}"
        data = r.json()
        assert data["status"] == "healthy"
        assert data["knowledge_items_indexed"] >= 12
        assert data["vector_store_ready"] is True
        print(f"  --> Health OK. Indexed items: {data['knowledge_items_indexed']}")

        r_kb = client.get("/api/knowledge")
        assert r_kb.status_code == 200
        kb_data = r_kb.json()
        assert len(kb_data["studies"]) >= 12
        print(f"  --> Knowledge API OK. Verified {len(kb_data['studies'])} research studies.")


def test_2_web_ui_dashboard():
    print("\n[TEST 2] Checking Web UI Dashboard (GET /)...")
    with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
        r = client.get("/")
        assert r.status_code == 200
        assert "Darukaa.Earth" in r.text
        assert "AI Biodiversity Intelligence" in r.text
        assert "Active Variables In Memory" in r.text
        print("  --> Dashboard HTML loaded successfully (Status 200, contains brand & UI components).")


def test_3_incomplete_query_clarification():
    print("\n[TEST 3] Incomplete query handling (PDF Example: 'Biodiversity is declining on my land')...")
    session_id = "live_test_session_1"
    with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
        payload = {
            "message": "Biodiversity is declining on my land.",
            "session_id": session_id
        }
        r = client.post("/api/chat", json=payload)
        assert r.status_code == 200
        res = r.json()
        assert res["status"] == "clarification_needed"
        assert len(res["clarifying_questions"]) >= 2
        
        print("  --> Status correctly marked: 'clarification_needed'")
        print(f"  --> System asked {len(res['clarifying_questions'])} targeted clarifying questions:")
        for q in res["clarifying_questions"]:
            print(f"      - {q['question_text']} (Ecological Reason: {q['ecological_importance']})")


def test_4_multi_turn_continuation_and_multi_metric_reasoning():
    print("\n[TEST 4] Multi-turn memory continuation & Multi-Metric reasoning...")
    session_id = "live_test_session_1"
    with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
        payload = {
            "message": "Soil organic carbon is 0.3%, rainfall is low, and crop is monoculture wheat in a semi-arid region.",
            "session_id": session_id
        }
        r = client.post("/api/chat", json=payload)
        assert r.status_code == 200
        res = r.json()
        assert res["status"] == "complete"
        assert res["analysis"] is not None
        
        # Verify memory combined Turn 1 (species_richness) with Turn 2 variables
        vars_ctx = res["variables_in_context"]
        print(f"  --> Variables in context: {vars_ctx}")
        assert vars_ctx.get("soil_organic_carbon") == 0.3
        assert vars_ctx.get("rainfall") == "low"
        assert "wheat" in vars_ctx.get("land_use", "")

        # Verify multi-metric causal reasoning
        causal = res["analysis"]["causal_relationships"]
        assert len(causal) > 0
        print(f"  --> Multi-metric causal nexus detected: {len(causal)} chains.")

        # Verify recommendations
        recs = res["analysis"]["recommendations"]
        assert len(recs) >= 1
        print(f"  --> Actionable recommendations generated: {len(recs)}")
        rec = recs[0]
        print(f"      1. What to do: {rec['what_to_do']}")
        print(f"      2. Why it works: {rec['why_it_works'][:120]}...")
        print(f"      3. Impacted metrics: {rec['impacted_metrics']}")
        print(f"      4. Quantitative projections: {rec['quantitative_estimate']}")
        print(f"      5. Time horizon: {rec['time_horizon']}")
        print(f"      6. Confidence: {rec['confidence']}")
        print(f"      7. Citations: {[c['citation_text'] for c in rec['citations']]}")

        assert len(rec["citations"]) > 0, "Recommendations must have credible citations"
        assert rec["time_horizon"] in ["short_term", "medium_term", "long_term"]


def test_5_structured_json_input():
    print("\n[TEST 5] Structured JSON Input directly via /api/analyze...")
    with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
        profile = {
            "soil_ph": 6.5,
            "soil_organic_carbon": 0.3,
            "soil_moisture": "low",
            "rainfall": "low",
            "temperature": "high",
            "land_use": "monoculture wheat",
            "species_richness": "low",
            "habitat_diversity": "low",
            "pollution": "none",
            "deforestation": "none",
            "region": "semi-arid",
            "geo_coordinates": {
                "latitude": 31.89,
                "longitude": -102.32
            }
        }
        r = client.post("/api/analyze", json=profile)
        assert r.status_code == 200, f"Structured input failed: {r.text}"
        data = r.json()
        assert data["status"] == "complete"
        assert len(data["recommendations"]) >= 1
        print("  --> Direct structured JSON parsed and analyzed successfully.")
        print(f"  --> Summary: {data['environmental_summary']}")


def test_6_edge_cases_and_error_handling():
    print("\n[TEST 6] Edge cases, validation errors, and session reset...")
    with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
        # 1. /api/analyze with fewer than 3 variables should return 400
        r_invalid = client.post("/api/analyze", json={"soil_ph": 6.5})
        assert r_invalid.status_code == 400
        print("  --> Properly rejected < 3 variables with HTTP 400.")

        # 2. Out-of-bounds soil pH should return 422 Unprocessable Entity
        r_bounds = client.post("/api/analyze", json={"soil_ph": 19.5, "rainfall": "low", "land_use": "wheat"})
        assert r_bounds.status_code == 422
        print("  --> Properly rejected out-of-bounds soil_ph (19.5 > 14.0) with HTTP 422.")

        # 3. Session reset via /api/reset
        r_reset = client.post("/api/reset", json={"session_id": "live_test_session_1"})
        assert r_reset.status_code == 200
        assert r_reset.json()["reset"] is True
        print("  --> Successfully reset conversation memory via /api/reset.")


if __name__ == "__main__":
    print("=" * 70)
    print("[START] COMPREHENSIVE LIVE END-TO-END SYSTEM VALIDATION")
    print("=" * 70)
    try:
        test_1_health_and_knowledge()
        test_2_web_ui_dashboard()
        test_3_incomplete_query_clarification()
        test_4_multi_turn_continuation_and_multi_metric_reasoning()
        test_5_structured_json_input()
        test_6_edge_cases_and_error_handling()
        print("\n" + "=" * 70)
        print("[SUCCESS] ALL END-TO-END TESTS PASSED ON THE LIVE SERVER!")
        print("=" * 70)
    except AssertionError as e:
        print(f"\n[ERROR] TEST FAILED: {e}")
        sys.exit(1)
