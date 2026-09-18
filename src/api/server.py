"""
FastAPI Server for Darukaa.Earth AI Biodiversity Intelligence System.
Exposes REST endpoints for conversational chat, structured JSON profile evaluation,
knowledge base inspection, and session memory management.
"""

import logging
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from src.models.schemas import (
    ChatRequest, ChatResponse, EnvironmentalProfile,
    ReasoningOutput, ClarifyingQuestion
)
from src.knowledge.corpus import KnowledgeCorpus
from src.knowledge.vector_store import ScientificVectorStore
from src.knowledge.retriever import KnowledgeRetriever
from src.reasoning.causal_graph import EcologicalCausalEngine
from src.reasoning.variable_extractor import EnvironmentalVariableExtractor
from src.reasoning.recommendation_engine import RecommendationEngine
from src.conversation.clarification_engine import ClarificationEngine
from src.conversation.memory import MemoryManager
from src.llm.provider import EcologicalSynthesizer
from src.ui.web_interface import get_index_html
from src.config import DEBUG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("darukaa_api")

app = FastAPI(
    title="Darukaa.Earth AI Biodiversity Intelligence API",
    description="Scientific Decision Engine for Ecological and Biodiversity Intelligence",
    version="1.0.0"
)

# CORS middleware for open integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize core scientific engines
corpus = KnowledgeCorpus()
vector_store = ScientificVectorStore(corpus=corpus)
retriever = KnowledgeRetriever(vector_store=vector_store)
causal_engine = EcologicalCausalEngine()
memory_manager = MemoryManager()


@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    """Serves the interactive AI Environmental Scientist Dashboard."""
    return HTMLResponse(content=get_index_html(), status_code=200)


@app.get("/health")
async def health_check():
    """System health check and knowledge status."""
    return {
        "status": "healthy",
        "service": "Darukaa.Earth AI Biodiversity Intelligence",
        "knowledge_items_indexed": len(corpus.all_items()),
        "vector_store_ready": vector_store.embeddings_matrix is not None
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Multi-turn conversational intelligence endpoint.
    Handles text or structured input, checks for missing variables,
    asks clarifying questions when incomplete, and generates multi-metric recommendations.
    """
    session = memory_manager.get_or_create_session(request.session_id)
    existing_vars = session.get_variables()

    # Merge inputs from memory, user text, and optional structured JSON
    active_vars = EnvironmentalVariableExtractor.merge_inputs(
        text=request.message,
        structured_data=request.structured_data,
        existing_variables=existing_vars
    )
    session.update_variables(active_vars)

    user_text = request.message or ""
    if user_text:
        session.add_message("user", user_text)

    # 1. Conversational Completeness Check (Missing Variable Detection)
    completeness = ClarificationEngine.evaluate_completeness(active_vars)

    if completeness["needs_clarification"]:
        clarifying_qs = completeness["questions"]
        q_lines = "\n".join([f"- **{q.question_text}**" for q in clarifying_qs])
        
        reply = (
            "### 🌿 AI Environmental Science Assessment (Initial Intake)\n"
            "To formulate an accurate, evidence-backed scientific recommendation, additional ecological variables are necessary. "
            "Broad recommendations risk failing because restoration strategies depend critically on belowground and climatic feedbacks.\n\n"
            "**Please provide the following environmental parameters:**\n"
            f"{q_lines}\n\n"
            "*(You can provide these either by continuing the conversation or submitting a structured JSON profile.)*"
        )
        
        session.add_message("assistant", reply)
        
        return ChatResponse(
            session_id=session.session_id,
            reply=reply,
            status="clarification_needed",
            variables_in_context=active_vars,
            clarifying_questions=clarifying_qs,
            analysis=None
        )

    # 2. Multi-Metric Causal Reasoning (At least 3 environmental variables present)
    causal_analysis = causal_engine.analyze_multi_metrics(active_vars)

    # 3. Scientific Knowledge Retrieval (RAG)
    retrieval_data = retriever.retrieve(query=user_text, active_variables=active_vars)

    # 4. Evidence-Grounded Recommendation Synthesis
    reasoning_output = RecommendationEngine.build_reasoning_output(
        variables=active_vars,
        causal_analysis=causal_analysis,
        retrieval_result=retrieval_data
    )

    # 5. Scientific Synthesis (Formatted text response)
    final_reply = EcologicalSynthesizer.synthesize_response(
        user_query=user_text,
        reasoning_output=reasoning_output,
        retrieval_data=retrieval_data
    )

    session.add_message("assistant", final_reply)

    return ChatResponse(
        session_id=session.session_id,
        reply=final_reply,
        status="complete",
        variables_in_context=active_vars,
        clarifying_questions=[],
        analysis=reasoning_output
    )


@app.post("/api/analyze", response_model=ReasoningOutput)
async def analyze_structured_profile(profile: EnvironmentalProfile):
    """
    Direct scientific analysis of a structured JSON environmental profile.
    Connects multiple variables and returns evidence-backed recommendations.
    """
    vars_dict = EnvironmentalVariableExtractor.extract_from_profile(profile)
    
    if len(vars_dict) < 3:
        raise HTTPException(
            status_code=400,
            detail="At least 3 environmental variables are required to conduct multi-metric reasoning."
        )

    causal_analysis = causal_engine.analyze_multi_metrics(vars_dict)
    retrieval_data = retriever.retrieve(query="", active_variables=vars_dict)
    
    reasoning_output = RecommendationEngine.build_reasoning_output(
        variables=vars_dict,
        causal_analysis=causal_analysis,
        retrieval_result=retrieval_data
    )
    return reasoning_output


@app.get("/api/knowledge")
async def list_knowledge_items():
    """Lists indexed scientific knowledge items with their citations."""
    return {
        "count": len(corpus.all_items()),
        "studies": corpus.all_items()
    }


@app.post("/api/reset")
async def reset_session(payload: Dict[str, str] = Body(...)):
    """Resets memory for a specific conversation session."""
    sid = payload.get("session_id", "")
    success = memory_manager.reset_session(sid)
    return {"session_id": sid, "reset": success}
