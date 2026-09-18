"""
Environmental Variable Extractor.
Parses natural-language user queries and structured JSON dictionaries to identify
known environmental parameters and metrics.
"""

import re
from typing import Dict, Any, Optional
from src.models.schemas import EnvironmentalProfile
from src.models.environmental_metrics import normalize_metric_value


class EnvironmentalVariableExtractor:
    """Extracts, standardizes, and validates environmental variables from text or JSON."""

    @staticmethod
    def extract_from_text(text: str) -> Dict[str, Any]:
        """
        Uses pattern matching and domain dictionaries to detect environmental metrics from text.
        """
        extracted: Dict[str, Any] = {}
        text_lower = text.lower()

        # 1. Soil Organic Carbon (SOC)
        soc_match = re.search(r"(?:soil\s*organic\s*carbon|soc|organic\s*carbon)\s*(?:is|:|=|\s+)?\s*([0-9]+(?:\.[0-9]+)?)\s*%", text_lower)
        if not soc_match:
            soc_match = re.search(r"(?:soil\s*organic\s*carbon|soc)\s*(?:is|:|=|\s+)?\s*([0-9]+(?:\.[0-9]+)?)", text_lower)
        if soc_match:
            extracted["soil_organic_carbon"] = float(soc_match.group(1))

        # 2. Soil pH
        ph_match = re.search(r"(?:soil\s*)?ph\s*(?:is|:|=|\s+)?\s*([0-9]+(?:\.[0-9]+)?)", text_lower)
        if ph_match:
            val = float(ph_match.group(1))
            if 0.0 <= val <= 14.0:
                extracted["soil_ph"] = val

        # 3. Rainfall / Precipitation
        if re.search(r"\b(?:low|scarce|minimal|deficient|erratic|dry|drought)\s*(?:rainfall|precipitation|rain)\b", text_lower) or \
           re.search(r"\b(?:rainfall|precipitation|rain)\s*(?:is|level is|pattern is|:|=|\s+)?\s*(low|very low|scarce|erratic|dry|minimal)\b", text_lower) or \
           re.search(r"\breceives?\s*(?:little|minimal|low)\s*(?:rainfall|rain)\b", text_lower):
            extracted["rainfall"] = "low"
        elif re.search(r"\b(?:moderate|normal|adequate)\s*(?:rainfall|precipitation|rain)\b", text_lower) or \
             re.search(r"\b(?:rainfall|precipitation|rain)\s*(?:is|level is|pattern is|:|=|\s+)?\s*(moderate|normal|adequate)\b", text_lower):
            extracted["rainfall"] = "moderate"
        elif re.search(r"\b(?:high|heavy|excessive)\s*(?:rainfall|precipitation|rain)\b", text_lower) or \
             re.search(r"\b(?:rainfall|precipitation|rain)\s*(?:is|level is|pattern is|:|=|\s+)?\s*(high|heavy|excessive)\b", text_lower):
            extracted["rainfall"] = "high"

        # 4. Land use / Cropping System
        if "monoculture wheat" in text_lower or ("monoculture" in text_lower and "wheat" in text_lower):
            extracted["land_use"] = "monoculture wheat"
        elif "monoculture corn" in text_lower or "monoculture maize" in text_lower:
            extracted["land_use"] = "monoculture corn"
        elif "monoculture" in text_lower:
            extracted["land_use"] = "monoculture"
        elif "pasture" in text_lower or "grazing" in text_lower:
            extracted["land_use"] = "degraded pasture"
        elif "agroforestry" in text_lower:
            extracted["land_use"] = "agroforestry"

        # 5. Soil Moisture
        if re.search(r"\b(?:low|dry|arid|moisture-stressed|poor)\s*(?:soil\s*moisture|moisture)\b", text_lower) or \
           re.search(r"\b(?:soil\s*moisture|moisture)\s*(?:is|level is|:|=|\s+)?\s*(low|dry|very low|poor|stressed)\b", text_lower):
            extracted["soil_moisture"] = "low"
        elif re.search(r"\b(?:moderate|medium|good)\s*(?:soil\s*moisture|moisture)\b", text_lower) or \
             re.search(r"\b(?:soil\s*moisture|moisture)\s*(?:is|level is|:|=|\s+)?\s*(moderate|medium|good)\b", text_lower):
            extracted["soil_moisture"] = "moderate"

        # 6. Temperature / Climate Regime
        if re.search(r"\b(?:high|extreme|heatwave|hot)\s*(?:temperature|temps?)\b", text_lower) or \
           re.search(r"\b(?:temperature|temps?)\s*(?:is|:|=|\s+)?\s*(high|hot|extreme)\b", text_lower):
            extracted["temperature"] = "high"

        # 7. Species Richness / Biodiversity
        if re.search(r"\b(?:declining|low|depleted|poor|minimal)\s*(?:biodiversity|species\s*richness|wildlife)\b", text_lower) or \
           re.search(r"\bbiodiversity\s*(?:is\s*)?declining\b", text_lower) or \
           re.search(r"\b(?:species\s*richness|biodiversity)\s*(?:is|:|=|\s+)?\s*(low|poor|critically low|depleted)\b", text_lower) or \
           re.search(r"\bvery\s*low\s*biodiversity\b", text_lower):
            extracted["species_richness"] = "low"

        # 8. Habitat Diversity / Fragmentation
        if re.search(r"\b(?:fragmented|homogenous|monotonous|isolated)\s*(?:habitat|landscape)\b", text_lower) or \
           re.search(r"\b(?:habitat\s*diversity|habitat)\s*(?:is|:|=|\s+)?\s*(low|fragmented|poor|homogenous)\b", text_lower):
            extracted["habitat_diversity"] = "low"

        # 9. Pollution
        if re.search(r"\b(?:pesticide|fertilizer|chemical|runoff|toxic|high\s*pollution)\b", text_lower):
            if "severe" in text_lower or "high" in text_lower:
                extracted["pollution"] = "high"
            elif "none" in text_lower or "no pollution" in text_lower:
                extracted["pollution"] = "none"
            else:
                extracted["pollution"] = "moderate"

        # 10. Deforestation
        if re.search(r"\b(?:cleared|deforested|deforestation|tree\s*loss|canopy\s*removal)\b", text_lower):
            extracted["deforestation"] = "moderate"

        # 11. Region / Biome
        if "semi-arid" in text_lower or "semi arid" in text_lower:
            extracted["region"] = "semi-arid"
        elif "arid" in text_lower:
            extracted["region"] = "arid"
        elif "tropical" in text_lower:
            extracted["region"] = "tropical"
        elif "temperate" in text_lower:
            extracted["region"] = "temperate"

        # Normalize extracted values
        return {k: normalize_metric_value(k, v) for k, v in extracted.items()}

    @staticmethod
    def extract_from_profile(profile: EnvironmentalProfile) -> Dict[str, Any]:
        """Extracts and normalizes all non-null fields from an EnvironmentalProfile."""
        raw_dict = profile.get_present_variables()
        return {k: normalize_metric_value(k, v) for k, v in raw_dict.items()}

    @classmethod
    def merge_inputs(
        cls,
        text: Optional[str] = None,
        structured_data: Optional[EnvironmentalProfile] = None,
        existing_variables: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Merges variables from existing conversation memory, new natural-language text,
        and new structured JSON input (structured data takes precedence over text extraction).
        """
        merged = dict(existing_variables or {})

        if text:
            extracted_text = cls.extract_from_text(text)
            merged.update(extracted_text)

        if structured_data:
            extracted_struct = cls.extract_from_profile(structured_data)
            merged.update(extracted_struct)

        return merged
