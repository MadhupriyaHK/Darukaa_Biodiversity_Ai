"""
Environmental Metrics definitions, acceptable units, and ecological thresholds.
"""

from typing import Dict, Any, Optional

# Core environmental metrics explicitly defined in the Darukaa challenge PDF
CORE_METRIC_DEFINITIONS: Dict[str, Dict[str, Any]] = {
    "soil_ph": {
        "domain": "soil_health",
        "description": "Soil pH level (acidity / alkalinity)",
        "unit": "pH scale (0-14)",
        "healthy_range": (6.0, 7.5),
        "critical_acidic": 5.5,
        "critical_alkaline": 8.2
    },
    "soil_organic_carbon": {
        "domain": "soil_health",
        "description": "Soil Organic Carbon (SOC) percentage in topsoil",
        "unit": "%",
        "healthy_threshold": 1.5,
        "critical_threshold": 0.6,
        "severely_depleted": 0.4
    },
    "soil_moisture": {
        "domain": "soil_health",
        "description": "Soil moisture status in root zone",
        "unit": "qualitative or volumetric %",
        "valid_levels": ["very_low", "low", "moderate", "high", "waterlogged"]
    },
    "land_use": {
        "domain": "land_cover",
        "description": "Current agricultural or land management system",
        "unit": "classification",
        "common_types": [
            "monoculture wheat", "monoculture cereal", "monoculture corn", "monoculture soy",
            "industrial cropland", "degraded pasture", "rotational grazing", "agroforestry", "poly-culture"
        ]
    },
    "species_richness": {
        "domain": "biodiversity_indicators",
        "description": "Observed or relative number of distinct plant/insect/wildlife species",
        "unit": "qualitative or count/m²",
        "valid_levels": ["critically_low", "low", "moderate", "high", "biodiverse"]
    },
    "habitat_diversity": {
        "domain": "biodiversity_indicators",
        "description": "Structural heterogeneity of vegetation, canopy strata, and microhabitats",
        "unit": "qualitative",
        "valid_levels": ["homogenous", "low", "moderate", "heterogeneous", "complex"]
    },
    "rainfall": {
        "domain": "climate",
        "description": "Annual or seasonal precipitation pattern",
        "unit": "qualitative or mm/year",
        "valid_levels": ["very_low", "low", "moderate", "high", "erratic"]
    },
    "temperature": {
        "domain": "climate",
        "description": "Thermal profile and seasonal heat extremes",
        "unit": "qualitative or °C",
        "valid_levels": ["low", "moderate", "high", "extreme"]
    },
    "pollution": {
        "domain": "human_impact",
        "description": "Agrochemical, pesticide, or heavy metal contamination burden",
        "unit": "qualitative index",
        "valid_levels": ["none", "low", "moderate", "high", "severe"]
    },
    "deforestation": {
        "domain": "human_impact",
        "description": "Degree of tree canopy removal, land clearing, or vegetation stripping",
        "unit": "qualitative index",
        "valid_levels": ["none", "low", "moderate", "severe", "historical"]
    },
    "region": {
        "domain": "spatial_context",
        "description": "Climatic or geographic biome (e.g., semi-arid, temperate, tropical, sub-tropical)",
        "unit": "ecoregion"
    },
    "geo_coordinates": {
        "domain": "spatial_context",
        "description": "Latitude and longitude coordinates for spatial verification",
        "unit": "decimal degrees"
    }
}


def normalize_metric_value(metric_name: str, value: Any) -> Any:
    """Normalizes string or numeric values for uniform reasoning."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return round(float(value), 3)
    if isinstance(value, str):
        val_clean = value.strip().lower()
        if metric_name == "region":
            return val_clean
        if metric_name == "land_use":
            if "monoculture" in val_clean and "wheat" in val_clean:
                return "monoculture wheat"
            return val_clean

        # Level Normalization mappings for qualitative variables
        synonyms = {
            "very low": "very_low",
            "critically low": "critically_low",
            "dry": "low",
            "arid": "low",
            "drought": "very_low",
            "hot": "high",
            "extremely hot": "extreme",
            "minimal": "low",
            "poor": "low",
            "none": "none",
            "zero": "none",
            "severe": "severe",
            "high": "high",
            "medium": "moderate",
            "mod": "moderate"
        }
        return synonyms.get(val_clean, val_clean)
    return value
