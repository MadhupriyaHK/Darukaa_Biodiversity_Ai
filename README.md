# Darukaa.Earth: AI Biodiversity Intelligence Chatbot Challenge

> **"Build a system that behaves like an AI environmental scientist, not a chatbot."**

An AI-driven scientific conversational intelligence system for biodiversity restoration, agroecology, and ecosystem resilience. Designed and built strictly to satisfy all core requirements, constraints, and evaluation criteria of the **Darukaa.Earth Hackathon Challenge**.

---

## 1. Problem Statement
Modern agricultural and land-management practices frequently decouple carbon, water, and biotic cycles, leading to severe biodiversity loss, soil carbon depletion, and desertification. When landholders and conservationists query generic LLMs (e.g. ChatGPT wrappers), they receive shallow, ungrounded platitudes (e.g., *"adopt sustainable practices"* or *"conserve water"*).

Generic chatbots lack:
1. Grounded environmental datasets and peer-reviewed scientific literature.
2. The ability to reason across multiple interlocking environmental metrics simultaneously ($\ge 3$ variables).
3. Conversational discipline to request critical baseline variables before prescribing interventions.
4. Transparent, verifiable scientific provenance and quantitative impact projections.

---

## 2. Solution Overview
The **Darukaa.Earth AI Biodiversity Intelligence System** is an AI environmental scientist engine combining:
* **A Grounded Scientific Retrieval Layer (RAG):** Real, peer-reviewed corpus covering the Food and Agriculture Organization (FAO), Intergovernmental Panel on Climate Change (IPCC), International Union for Conservation of Nature (IUCN), and the Convention on Biological Diversity (CBD).
* **Multi-Metric Causal Graph Engine:** Evaluates compound ecological stress across $\ge 3$ variables (e.g., *Soil Organic Carbon $\leftrightarrow$ Water Retention $\leftrightarrow$ Land Use $\leftrightarrow$ Microclimate $\leftrightarrow$ Biodiversity*).
* **Conversational Intelligence & Memory:** Proactively identifies incomplete inputs, poses targeted scientific clarifying questions, and maintains cross-turn state.
* **Evidence-Backed Recommendation Protocol:** Synthesizes actionable, non-obvious interventions with biochemical mechanisms, quantitative improvement estimates, time horizons, confidence metrics, and formal scientific citations.
* **Dual-Mode Operation:** Functions 100% deterministically and offline with zero external API key requirements, while seamlessly upgrading with Google Gemini or OpenAI when API keys are supplied.

---

## 3. Architecture

```
                                 User Input
                      (Natural Language / Structured JSON)
                                      │
                                      ▼
                        ┌───────────────────────────┐
                        │   Conversational Memory   │
                        │   (Multi-Turn Context)    │
                        └─────────────┬─────────────┘
                                      ▼
                        ┌───────────────────────────┐
                        │    Variable Extractor     │
                        │ (Normalizes 10+ Metrics)  │
                        └─────────────┬─────────────┘
                                      ▼
                        ┌───────────────────────────┐
                        │   Clarification Engine    │
                        └─────────────┬─────────────┘
                                      │
             ┌────────────────────────┴────────────────────────┐
             │ (< 3 variables)                                 │ (>= 3 variables)
             ▼                                                 ▼
┌───────────────────────────┐                    ┌───────────────────────────┐
│ Dynamic Clarification Qs  │                    │   Scientific RAG Layer    │
│ (SOC %, Rainfall, LandUse)│                    │ (Vector Store + Metadata) │
└───────────────────────────┘                    └─────────────┬─────────────┘
                                                               │
                                                               ▼
                                                 ┌───────────────────────────┐
                                                 │   Multi-Metric Reasoner   │
                                                 │   (Ecological Causal DB)  │
                                                 └─────────────┬─────────────┘
                                                               │
                                                               ▼
                                                 ┌───────────────────────────┐
                                                 │   Recommendation Engine   │
                                                 │   (Mechanisms + Horizons) │
                                                 └─────────────┬─────────────┘
                                                               │
                                                               ▼
                                                 ┌───────────────────────────┐
                                                 │   Scientific Synthesizer  │
                                                 │ (Deterministic / GenAI)   │
                                                 └─────────────┬─────────────┘
                                                               │
                                                               ▼
                                                 ┌───────────────────────────┐
                                                 │   FastAPI & Dashboard     │
                                                 └───────────────────────────┘
```

---

## 4. Key Features

1. **Retrievable Scientific Knowledge Layer:** Real publications indexed into an in-memory vector store with TF-IDF subword embeddings and cosine similarity.
2. **Proactive Missing-Variable Clarification:** If a user submits an incomplete query (e.g. *"Biodiversity is declining on my land"*), the system pauses and inquires about missing variables (SOC %, rainfall pattern, land use).
3. **Compound Multi-Metric Causal Synthesis:** Explicitly analyzes $\ge 3$ environmental variables simultaneously.
4. **Structured JSON & Natural Language Input:** Accepts conversational prompts as well as direct JSON profiles.
5. **Rigorous Evidence Grounding:** No hallucinated papers, fake DOIs, or fabricated authors.
6. **Actionable Outputs with Time Horizons:** Every recommendation details:
   * What to do
   * Why it works (scientific mechanism)
   * Impacted environmental metrics
   * Quantitative improvement estimates
   * Time horizon (`short_term` 0–1 yr, `medium_term` 2–5 yrs, `long_term` 5+ yrs)
   * Confidence rating (`HIGH` / `MEDIUM`)
   * Verifiable literature reference and citation
7. **Interactive Dashboard & CLI:** Fast, responsive UI with real-time active variable badges, causal telemetry inspector, and citation provenance viewer.

---

## 5. Environmental Variables Covered

The system supports the full spectrum of metrics outlined in the challenge:

| Domain | Metrics | Standard Range / Levels |
| :--- | :--- | :--- |
| **Soil Health** | `soil_ph` | Numeric 0.0 – 14.0 (Optimal: 6.0 – 7.5; Acidic: <5.5; Alkaline: >8.2) |
| | `soil_organic_carbon` | Numeric % (Critical: <0.6%; Healthy: >1.5%) |
| | `soil_moisture` | Categorical (`very_low`, `low`, `moderate`, `high`, `waterlogged`) |
| **Land Use / Cover** | `land_use` | `monoculture wheat`, `monoculture cereal`, `pasture`, `agroforestry`, etc. |
| **Biodiversity Indicators**| `species_richness` | Categorical / Count (`critically_low`, `low`, `moderate`, `high`, `biodiverse`) |
| | `habitat_diversity` | Categorical (`homogenous`, `low`, `moderate`, `heterogeneous`, `complex`) |
| **Climate Factors** | `rainfall` | Categorical / mm (`very_low`, `low`, `moderate`, `high`, `erratic`) |
| | `temperature` | Categorical / °C (`low`, `moderate`, `high`, `extreme`) |
| **Human Impact** | `pollution` | Categorical (`none`, `low`, `moderate`, `high`, `severe`) |
| | `deforestation` | Categorical (`none`, `low`, `moderate`, `severe`, `historical`) |
| **Spatial Context** | `region` / `geo_coordinates` | Ecoregions (e.g. `semi-arid`, `temperate`, `tropical`) + Decimal Lat/Lon |

---

## 6. Scientific Knowledge Corpus

The system indexes authentic research reports in `data/knowledge_base/`:
* **`fao_soil_health.json`**: FAO World Soil Charter & Recarbonizing Global Soils (2021) — covers SOC depletion, microbial respiration, pH modulation, and water holding capacity.
* **`ipcc_land_climate.json`**: IPCC Special Report on Climate Change and Land (SRCCL 2019) — covers monoculture degradation, agroforestry alley cropping, and thermal attenuation.
* **`iucn_biodiversity_corridors.json`**: IUCN Guidelines for Conserving Connectivity (2020) & IPBES Pollinator Assessment (2016) — covers native hedgerows, beetle banks, and pollinator floral continuity.
* **`riparian_buffers_hydrology.json`**: UNEP Nature-based Solutions for Water Security (2020) — covers three-zone riparian vegetative filters, nitrate denitrification, and deforested micro-catchments.
* **`agroecology_silvopasture.json`**: Nature Sustainability & ICRAF (2022) — covers silvopastoral carbon storage, hydraulic lift, and cereal-legume intercropping mycorrhizal networks.
* **`ecological_indicators_soil_water.json`**: Global Soil Biodiversity Initiative & FAO (2020) — covers soil macro-fauna restoration (earthworms/collembola) and drought micro-wetlands.

---

## 7. Multi-Metric Reasoning Engine

Treating environmental variables in isolation fails in real ecosystems. The system encodes causal feedback chains:

```
[Soil Organic Carbon <= 0.6%] + [Rainfall = low] + [Land Use = monoculture wheat]
                              │
                              ▼
  • Soil Health: Depleted SOC degrades macro-aggregates & drops Available Water Capacity (AWC).
  • Water Dynamics: Bare, unmulched soil accelerates capillary evaporation and surface crusting.
  • Vegetation Architecture: Monoculture eliminates root-depth diversity and seasonal nectar supply.
  • Habitat Quality: Surface heat & drought drive massive die-off of mycorrhizae and pollinators.
                              │
                              ▼
  Synergistic Intervention: Agroforestry alley cropping with drought-hardy legumes + minimum tillage
  + permanent organic mulching simultaneously rebuilds SOC, moderates canopy heat, and creates floral corridors.
```

---

## 8. Input & Output Specifications

### A. Structured JSON Input Schema
Send via `POST /api/analyze` or `POST /api/chat`:
```json
{
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
```

### B. Structured Recommendation Output Schema
```json
{
  "what_to_do": "Introduce legume-based winter or off-season cover crops (e.g., Vicia villosa, Medicago sativa)",
  "why_it_works": "Leguminous root exudates release low-molecular-weight organic carbon compounds that stimulate mycorrhizal fungi and nitrogen-fixing Rhizobia. This biological activity forms water-stable micro-aggregates (<250 μm), protecting organic matter from oxidation under elevated temperatures and expanding the soil hydraulic retention curve.",
  "impacted_metrics": ["species_richness", "soil_organic_carbon"],
  "quantitative_estimate": "Increases soil organic carbon by 15-25% over 2-3 years, improves available water capacity (AWC) by 12-18%, and raises bacterial and fungal taxonomic richness by 30-35% compared to conventional monoculture fallows.",
  "time_horizon": "medium_term",
  "confidence": "high",
  "citations": [
    {
      "id": "FAO-SOC-001",
      "source_org": "FAO (Food and Agriculture Organization of the United Nations)",
      "title": "Recarbonizing Global Soils: A technical manual of recommended management practices. Volume 3",
      "year": 2021,
      "citation_text": "FAO. 2021. Recarbonizing Global Soils: A technical manual of recommended management practices. Rome, FAO. https://doi.org/10.4060/cb6378en"
    }
  ]
}
```

---

## 9. Local Setup and Installation

### Prerequisites
* **Python 3.10+** (Tested and validated on Python 3.14 on Windows 11).

### 1. Clone or Open the Repository
```powershell
cd C:\Users\madhu_3wwf98f\OneDrive\Desktop\Darukaa_Biodiversity_Ai
```

### 2. Install Required Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Configure Optional Environment Variables
Copy `.env.example` to `.env`:
```powershell
cp .env.example .env
```
*(Optional: add your `GEMINI_API_KEY` or `OPENAI_API_KEY`. If left empty, the internal deterministic scientific reasoning engine runs fully offline without requiring an API key).*

---

## 10. How to Run the System

### Option A: Interactive Web Dashboard (Recommended)
```powershell
python run.py
```
Open your browser at:
* **Dashboard:** [http://localhost:8000](http://localhost:8000)
* **Interactive API Swagger Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

### Option B: Interactive CLI Mode
```powershell
python run.py --cli
```

### Option C: Automated Hackathon Demonstration Mode
```powershell
python run.py --demo
```

---

## 11. Automated Test Suite

Run the full pytest test suite:
```powershell
python -m pytest tests -v
```

### Test Coverage Summary:
* `tests/test_clarification.py`: Verifies incomplete inputs trigger clarifying questions without premature generic advice.
* `tests/test_multi_metric.py`: Verifies the exact PDF scenario (SOC 0.3%, low rainfall, monoculture wheat, semi-arid) triggers $\ge 3$ variable reasoning and cited recommendations.
* `tests/test_structured_input.py`: Verifies direct JSON profile ingestion and schema validation.
* `tests/test_multi_turn.py`: Verifies cross-turn memory persistence and state retention.
* `tests/test_retrieval.py`: Verifies semantic vector search and exact literature provenance.
* `tests/test_edge_cases.py`: Verifies validation constraints (e.g. soil pH boundaries), empty inputs, and error handling.

---

## 12. Project Structure

```
Darukaa_Biodiversity_Ai/
├── data/
│   ├── knowledge_base/
│   │   ├── fao_soil_health.json
│   │   ├── ipcc_land_climate.json
│   │   ├── iucn_biodiversity_corridors.json
│   │   ├── riparian_buffers_hydrology.json
│   │   ├── agroecology_silvopasture.json
│   │   └── ecological_indicators_soil_water.json
│   └── ecological_knowledge_graph.json
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── models/
│   │   ├── schemas.py
│   │   └── environmental_metrics.py
│   ├── knowledge/
│   │   ├── corpus.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   └── retriever.py
│   ├── reasoning/
│   │   ├── variable_extractor.py
│   │   ├── causal_graph.py
│   │   └── recommendation_engine.py
│   ├── conversation/
│   │   ├── memory.py
│   │   └── clarification_engine.py
│   ├── llm/
│   │   └── provider.py
│   ├── api/
│   │   └── server.py
│   └── ui/
│       └── web_interface.py
├── tests/
│   ├── test_clarification.py
│   ├── test_multi_metric.py
│   ├── test_structured_input.py
│   ├── test_multi_turn.py
│   ├── test_retrieval.py
│   └── test_edge_cases.py
├── submission/
│   └── Darukaa_Submission_Guide.md
├── run.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## 13. Hackathon Requirement Mapping Audit

| Requirement in Darukaa Challenge PDF | Implementation Module | Status |
| :--- | :--- | :---: |
| **Knowledge System (Critical)**: Retrievable knowledge layer (not just prompts) covering Soil, Land Use, Biodiversity, Climate, Human Impact. | `data/knowledge_base/*.json`, `src/knowledge/corpus.py`, `src/knowledge/vector_store.py`, `src/knowledge/retriever.py` | **100% Complete** |
| **Conversational Intelligence**: Clarifying questions for incomplete queries; multi-turn memory. | `src/conversation/clarification_engine.py`, `src/conversation/memory.py`, `tests/test_clarification.py` | **100% Complete** |
| **Evidence-Backed Recommendations**: Concrete actions, mechanisms, quantitative metrics, citations (FAO, IPCC). | `src/reasoning/recommendation_engine.py`, `src/knowledge/corpus.py` | **100% Complete** |
| **Multi-Metric Reasoning**: Connects $\ge 3$ environmental variables simultaneously (e.g. SOC + Rainfall + Monoculture). | `src/reasoning/causal_graph.py`, `data/ecological_knowledge_graph.json` | **100% Complete** |
| **Input Handling**: Natural-language text + structured JSON schema + optional spatial coordinates. | `src/models/schemas.py`, `src/reasoning/variable_extractor.py`, `src/api/server.py` | **100% Complete** |
| **Output Quality**: Recommendation, impacted metrics, time horizon (short/medium/long), confidence level. | `src/models/schemas.py`, `src/reasoning/recommendation_engine.py` | **100% Complete** |
| **Zero Hallucination Constraint**: No fake papers, no generic advice like "use sustainable practices". | `src/llm/provider.py`, `src/knowledge/retriever.py` | **100% Complete** |
