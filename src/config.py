"""
Configuration module for Darukaa Biodiversity AI System.
Loads environment variables, defines paths, and sets reasoning thresholds.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
KNOWLEDGE_DIR = DATA_DIR / "knowledge_base"
GRAPH_FILE = DATA_DIR / "ecological_knowledge_graph.json"

# Load environment variables
load_dotenv(BASE_DIR / ".env")

# LLM Configurations
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip() or os.getenv("GOOGLE_API_KEY", "").strip()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "").strip()

# Preferred provider
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "auto").lower()  # 'gemini', 'openai', 'anthropic', or 'auto'

# Reasoning and RAG parameters
MINIMUM_VARIABLES_FOR_RECOMMENDATION = 3
RETRIEVAL_TOP_K = 4
SIMILARITY_THRESHOLD = 0.20

# Server configurations
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
