"""
Clarification Engine for Conversational Intelligence.
Evaluates input completeness, detects missing environmental parameters,
and generates targeted, scientifically grounded clarifying questions.
"""

from typing import Dict, Any, List
from src.models.schemas import ClarifyingQuestion
from src.config import MINIMUM_VARIABLES_FOR_RECOMMENDATION


class ClarificationEngine:
    """Detects missing ecological variables and requests targeted user details."""

    CRITICAL_QUESTIONS = {
        "soil_organic_carbon": {
            "text": "What is the topsoil organic carbon (SOC) percentage (e.g., 0.3%, 1.2%, or qualitative low/depleted)?",
            "reason": "Soil organic carbon determines water infiltration, microbial biomass, and structural aggregate stability."
        },
        "rainfall": {
            "text": "What is your local rainfall pattern or annual precipitation (e.g., low / semi-arid, moderate, or erratic)?",
            "reason": "Water availability dictates which plant guilds, cover crops, or tree species can survive without supplemental irrigation."
        },
        "land_use": {
            "text": "What is the primary land use or cropping practice (e.g., monoculture wheat, continuous cereal, pasture, or fallow)?",
            "reason": "Understanding the disturbance regime and vegetative cover identifies whether soil compaction or floral gaps drive the decline."
        },
        "soil_ph": {
            "text": "Do you know the soil pH (e.g., acidic <5.5, neutral 6.5, or alkaline >8.0)?",
            "reason": "Extreme pH limits nutrient bioavailability (phosphorus/aluminum) and symbiotic Rhizobia fixation."
        },
        "soil_moisture": {
            "text": "What is the typical soil moisture status in the root zone (e.g., dry, low, or seasonally saturated)?",
            "reason": "Soil moisture governs mycorrhizal fungal networks and soil invertebrate survival."
        },
        "pollution": {
            "text": "Is there significant synthetic pesticide, herbicide, or chemical fertilizer usage?",
            "reason": "Agrochemical burdens directly suppress soil meso-fauna and non-target wild pollinators."
        }
    }

    @classmethod
    def evaluate_completeness(cls, variables: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determines if there are enough variables (at least 3) to perform multi-metric reasoning.
        If not, generates targeted clarifying questions.
        """
        # Filter out purely spatial tags from metric count
        ecological_vars = {
            k: v for k, v in variables.items()
            if k not in ["region", "geo_coordinates"] and v is not None
        }

        num_vars = len(ecological_vars)
        needs_clarification = num_vars < MINIMUM_VARIABLES_FOR_RECOMMENDATION

        questions: List[ClarifyingQuestion] = []
        
        if needs_clarification:
            # Prioritize most critical missing variables
            priority_order = ["soil_organic_carbon", "rainfall", "land_use", "soil_ph", "soil_moisture"]
            
            for var_name in priority_order:
                if var_name not in ecological_vars:
                    q_info = cls.CRITICAL_QUESTIONS[var_name]
                    questions.append(ClarifyingQuestion(
                        variable=var_name,
                        question_text=q_info["text"],
                        ecological_importance=q_info["reason"]
                    ))
                    # Pick top 2-3 most essential questions to keep conversational focus
                    if len(questions) >= 3:
                        break

        return {
            "needs_clarification": needs_clarification,
            "variable_count": num_vars,
            "questions": questions
        }
