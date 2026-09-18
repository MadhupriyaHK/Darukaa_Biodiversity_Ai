# Darukaa.Earth Hackathon Challenge: Submission Document Guide (.docx)

Use the content below to populate your **submission Word document (`.docx`)** to be uploaded on the **My Jobs / Applied Job page**.

---

# Darukaa.Earth AI Biodiversity Intelligence Challenge Submission

**Candidate Name:** [Your Name]  
**Application ID / Role:** AI Engineer / Biodiversity Intelligence  
**Submission Date:** [Current Date]

---

## 1. Repository Access & Deployment Links

* **GitHub Repository Link:** [Paste your GitHub Repository Link here]
  * *(Note: If the repository is private, access has been granted to the following Darukaa reviewer accounts as instructed in the challenge specification):*
    * `ankita.dasgupta@darukaa.com`
    * `harsh.kumar@darukaa.com`
    * `utkarsh.gauniyal@darukaa.com`
    * `guneet.mutreja@darukaa.com`
* **Live Demo URL:** [Paste your deployed URL here, e.g. Render / Hugging Face Spaces / AWS / Ngrok link, or state: "Local demo available via `python run.py` (see Section 3)"]

---

## 2. Project Overview & Architecture

### System Purpose
The **Darukaa.Earth AI Biodiversity Intelligence System** is an AI environmental scientist designed to evaluate complex, multi-variable ecosystem challenges. Rather than providing generic chatbot advice (e.g., *"use sustainable practices"*), it uses multi-metric causal reasoning across at least 3 environmental variables and grounds every recommendation in peer-reviewed scientific literature (FAO, IPCC, IUCN, UNEP, Nature).

### Architecture Summary
* **Retrievable Knowledge Layer (RAG):** 6 domain datasets covering Soil Health (pH, SOC, moisture), Land Cover/Cropping, Biodiversity Indicators, Climate, and Human Impact. Indexed in an in-memory vector database with subword n-gram TF-IDF embeddings and cosine similarity.
* **Conversational Intelligence & Memory:** Automatically flags incomplete user inputs (e.g., *"Biodiversity is declining on my land"*) and poses scientifically targeted clarifying questions before prescribing interventions. Maintains multi-turn context across turns.
* **Multi-Metric Causal Engine:** Formulates cross-variable feedback loops (e.g., *Low Soil Organic Carbon + Low Rainfall + Monoculture Wheat $\rightarrow$ Evapotranspiration Spike $\rightarrow$ Mycorrhizal & Pollinator Collapse $\rightarrow$ Systemic Desertification*).
* **Scientific Recommendation Protocol:** Strictly requires:
  1. What to do (actionable, non-obvious intervention)
  2. Why it works (biochemical / ecological mechanism)
  3. Impacted environmental metrics
  4. Quantified improvement projections
  5. Implementation time horizon (`short_term`, `medium_term`, `long_term`)
  6. Confidence rating (`HIGH` / `MEDIUM`)
  7. Exact literature citation with report title and DOI/reference
* **Dual-Engine Execution:** Runs 100% deterministically and offline with zero paid API keys needed, and seamlessly elevates with Google Gemini or OpenAI when keys are configured in `.env`.

---

## 3. Database Schema & Data Models

### Input Profile Schema (`EnvironmentalProfile`)
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

### Knowledge Item Schema (`KnowledgeItem`)
```json
{
  "id": "FAO-SOC-001",
  "topic": "Soil Organic Carbon and Microbial Diversity in Arid and Semi-Arid Soils",
  "domain": "soil_health",
  "variables": ["soil_organic_carbon", "soil_moisture", "species_richness", "rainfall", "land_use"],
  "scientific_mechanism": "Leguminous root exudates release low-molecular-weight organic carbon compounds...",
  "quantitative_evidence": "Increases soil organic carbon by 15-25% over 2-3 years, improves AWC by 12-18%...",
  "interventions": ["Introduce legume-based cover crops", "Implement minimum tillage"],
  "time_horizon": "medium_term",
  "source": "FAO (Food and Agriculture Organization of the United Nations)",
  "citation": "FAO. 2021. Recarbonizing Global Soils: A technical manual of recommended management practices. Rome, FAO."
}
```

---

## 4. Local Setup & Execution Instructions

1. **Clone the repository:**
   ```bash
   git clone <REPO_URL>
   cd Darukaa_Biodiversity_Ai
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Interactive Dashboard & API:**
   ```bash
   python run.py
   ```
   * Open browser: `http://localhost:8000`
   * API Swagger Docs: `http://localhost:8000/docs`

4. **Run the Automated Demonstration Mode:**
   ```bash
   python run.py --demo
   ```

5. **Run the Test Suite:**
   ```bash
   python -m pytest tests -v
   ```
   *(All 11 tests pass with 100% success rate across clarification, multi-metric reasoning, memory, and RAG retrieval).*

---

## 5. Continuous Integration / Deployment (CI/CD)

The project is structured with production Docker and GitHub Actions CI pipelines:
* **CI Workflow (`.github/workflows/ci.yml`):**
  * Automated testing across Python 3.10, 3.11, 3.12, 3.14 on Ubuntu and Windows.
  * Flake8 linting, type validation with Pydantic, and pytest execution.
* **Deployment Options:**
  * Ready for containerized deployment via Docker / Cloud Run / Hugging Face Spaces.
