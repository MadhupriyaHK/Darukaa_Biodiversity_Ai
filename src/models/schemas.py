"""
Pydantic data models for structured inputs, scientific recommendations,
causal chains, conversation payloads, and knowledge retrieval items.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class GeoCoordinates(BaseModel):
    latitude: float = Field(..., ge=-90.0, le=90.0, description="Latitude in decimal degrees")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="Longitude in decimal degrees")


class EnvironmentalProfile(BaseModel):
    """
    Structured environmental dataset schema supporting all parameters in Darukaa Challenge.
    """
    soil_ph: Optional[float] = Field(None, ge=0.0, le=14.0, description="Soil pH level (e.g., 6.5)")
    soil_organic_carbon: Optional[float] = Field(None, ge=0.0, le=100.0, description="Soil Organic Carbon percentage (e.g., 0.3 for 0.3%)")
    soil_moisture: Optional[str] = Field(None, description="Soil moisture status (e.g., 'low', 'moderate', 'high')")
    rainfall: Optional[str] = Field(None, description="Precipitation profile (e.g., 'low', 'moderate', 'erratic')")
    temperature: Optional[str] = Field(None, description="Temperature regime (e.g., 'high', 'moderate', 'extreme')")
    land_use: Optional[str] = Field(None, description="Land management practice (e.g., 'monoculture wheat', 'pasture')")
    species_richness: Optional[str] = Field(None, description="Biodiversity species richness (e.g., 'low', 'moderate')")
    habitat_diversity: Optional[str] = Field(None, description="Habitat heterogeneity (e.g., 'low', 'fragmented')")
    pollution: Optional[str] = Field(None, description="Pollution / agrochemical load (e.g., 'high', 'none')")
    deforestation: Optional[str] = Field(None, description="Deforestation / canopy loss (e.g., 'moderate', 'none')")
    region: Optional[str] = Field(None, description="Geographic or climatic biome (e.g., 'semi-arid', 'temperate')")
    geo_coordinates: Optional[GeoCoordinates] = Field(None, description="Optional geo-coordinates for spatial grounding")

    def count_present_variables(self) -> int:
        """Counts how many environmental variables have non-null values."""
        exclude = {"region", "geo_coordinates"}
        count = 0
        for k, v in self.model_dump().items():
            if k not in exclude and v is not None:
                count += 1
        return count

    def get_present_variables(self) -> Dict[str, Any]:
        """Returns dictionary of provided environmental variables."""
        return {k: v for k, v in self.model_dump().items() if v is not None}


class Citation(BaseModel):
    id: str
    source_org: str
    title: str
    year: int
    citation_text: str


class RecommendationItem(BaseModel):
    """
    Mandatory recommendation schema matching Darukaa PDF requirements:
    1. What to do
    2. Why it works (scientific mechanism)
    3. Which environmental metric(s) improve
    4. Time horizon (short, medium, long)
    5. Quantitative improvement estimates
    6. Scientific evidence & citation
    7. Confidence level
    """
    what_to_do: str = Field(..., description="Actionable, non-obvious biodiversity intervention")
    why_it_works: str = Field(..., description="Underlying scientific, biochemical, or ecological mechanism")
    impacted_metrics: List[str] = Field(..., description="List of environmental metrics improved")
    quantitative_estimate: str = Field(..., description="Evidence-grounded quantitative improvement metrics")
    time_horizon: str = Field(..., description="'short_term' (0-1 yr), 'medium_term' (2-5 yrs), or 'long_term' (5+ yrs)")
    confidence: str = Field("high", description="'high', 'medium', or 'low'")
    citations: List[Citation] = Field(default_factory=list, description="Direct references to scientific literature")


class ClarifyingQuestion(BaseModel):
    variable: str
    question_text: str
    ecological_importance: str


class ReasoningOutput(BaseModel):
    """
    Structured environmental scientist analysis.
    """
    status: str = Field("complete", description="'clarification_needed' or 'complete'")
    environmental_summary: str
    variables_analyzed: Dict[str, Any]
    causal_relationships: List[str] = Field(default_factory=list, description="Causal chains linking >= 3 variables")
    ecological_stress_level: str = Field("moderate", description="Compound stress rating")
    recommendations: List[RecommendationItem] = Field(default_factory=list)
    clarifying_questions: List[ClarifyingQuestion] = Field(default_factory=list)
    retrieved_evidence_ids: List[str] = Field(default_factory=list)


class ChatMessage(BaseModel):
    role: str = Field(..., description="'user' or 'assistant'")
    content: str


class ChatRequest(BaseModel):
    message: Optional[str] = Field(None, description="Natural-language message")
    structured_data: Optional[EnvironmentalProfile] = Field(None, description="Optional structured JSON input")
    session_id: Optional[str] = Field(None, description="Session ID for multi-turn conversation memory")


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    status: str  # 'clarification_needed' or 'complete'
    variables_in_context: Dict[str, Any]
    clarifying_questions: List[ClarifyingQuestion] = Field(default_factory=list)
    analysis: Optional[ReasoningOutput] = None
