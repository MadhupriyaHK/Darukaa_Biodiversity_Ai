# Darukaa.Earth — AI Biodiversity Intelligence Chatbot

An AI-powered environmental intelligence system that provides **evidence-backed biodiversity and ecosystem recommendations** using scientific knowledge, retrieval, multi-metric reasoning, and conversational context.

## Key Features

* **Scientific Knowledge Retrieval** — Retrieves relevant information from a structured environmental knowledge base.
* **Multi-Metric Reasoning** — Connects soil health, water, climate, land use, and biodiversity indicators.
* **Evidence-Backed Recommendations** — Provides recommendations with supporting scientific sources.
* **Conversational Intelligence** — Maintains context and asks clarification questions when information is incomplete.
* **Structured Input** — Supports environmental scenarios through JSON as well as natural-language queries.
* **Causal Reasoning** — Models relationships between environmental variables to explain potential ecological impacts.
* **Interactive Dashboard** — Provides a web interface for environmental analysis and recommendations.

## Architecture

```text
User Query / Structured JSON
            ↓
    Variable Extraction
            ↓
 Conversation & Clarification
            ↓
 Scientific Knowledge Retrieval
            ↓
   Multi-Metric Reasoning
            ↓
 Recommendation Engine
            ↓
 Evidence + Metrics + Explanation
            ↓
      Web Dashboard / API
```

## Knowledge Coverage

The system currently covers:

* Soil health
* Soil organic carbon
* Soil moisture and pH
* Land use and land cover
* Biodiversity indicators
* Climate and rainfall factors
* Water and riparian systems
* Habitat connectivity and corridors
* Human and agricultural impacts

## Tech Stack

**Backend:** Python, FastAPI
**AI/Retrieval:** Embeddings, vector retrieval, scientific knowledge base
**Interface:** HTML, CSS, JavaScript
**Testing:** Pytest
**Deployment:** Docker, GitHub Actions

## Project Structure

```text
Darukaa_Biodiversity_Ai/
├── data/
│   ├── knowledge_base/
│   └── ecological_knowledge_graph.json
├── src/
│   ├── api/
│   ├── conversation/
│   ├── knowledge/
│   ├── llm/
│   ├── models/
│   ├── reasoning/
│   └── ui/
├── tests/
├── submission/
├── Dockerfile
├── requirements.txt
└── run.py
```

## Run Locally

```bash
git clone https://github.com/MadhupriyaHK/Darukaa_Biodiversity_Ai.git
cd Darukaa_Biodiversity_Ai

pip install -r requirements.txt

python run.py
```

Open:

```text
http://localhost:8000
```

API documentation:

```text
http://localhost:8000/docs
```

## Testing

Run the test suite with:

```bash
python -m pytest
```

## Live Demo

Coming soon.

## Challenge

Built for the **Darukaa.Earth AI Biodiversity Intelligence Chatbot Challenge**.
