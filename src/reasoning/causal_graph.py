"""
Multi-Metric Causal Reasoning Engine.
Interweaves at least three environmental variables to establish causal relationships:
Input variables -> Variable interactions -> Ecological impact -> Restoration pathway.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from src.config import GRAPH_FILE


class EcologicalCausalEngine:
    """Evaluates compound multi-metric interactions and triggers causal chains."""

    def __init__(self, graph_path: Path = GRAPH_FILE):
        self.graph_path = Path(graph_path)
        self.graph_data: Dict[str, Any] = {}
        self.load_graph()

    def load_graph(self) -> None:
        if self.graph_path.exists():
            try:
                with open(self.graph_path, "r", encoding="utf-8") as f:
                    self.graph_data = json.load(f)
            except Exception as e:
                self.graph_data = {"causal_chains": []}
        else:
            self.graph_data = {"causal_chains": []}

    def analyze_multi_metrics(self, variables: Dict[str, Any]) -> Dict[str, Any]:
        """
        Connects multiple variables together into an ecological reasoning pathway.
        Evaluates at least 3 environmental variables simultaneously.
        """
        active_causal_chains: List[Dict[str, Any]] = []
        synthesized_explanations: List[str] = []
        compound_stress_factors: List[str] = []
        priority_knowledge_ids: List[str] = []

        soc = variables.get("soil_organic_carbon")
        rainfall = variables.get("rainfall")
        land_use = str(variables.get("land_use", "")).lower()
        ph = variables.get("soil_ph")
        moisture = variables.get("soil_moisture")
        temp = variables.get("temperature")
        species_richness = variables.get("species_richness")
        habitat_diversity = variables.get("habitat_diversity")
        pollution = variables.get("pollution")
        deforestation = variables.get("deforestation")

        # 1. Tri-Metric Synergy: Low SOC + Low Rainfall / Moisture + Monoculture Land Use
        if (soc is not None and soc <= 0.8) and \
           (rainfall in ["low", "very_low"] or moisture in ["low", "very_low"]) and \
           ("monoculture" in land_use or land_use == "industrial cropland"):
            
            chain_desc = (
                "Multi-Variable Nexus [Soil Organic Carbon ({soc}%) + Rainfall ({rainfall}) + Land Use ({land_use})]:\n"
                "  1. Soil Health: Depleted SOC impairs crumb structure and lowers available water holding capacity.\n"
                "  2. Water Dynamics: Scant precipitation on unmulched soil causes rapid capillary evaporation and surface crusting.\n"
                "  3. Vegetation Architecture: Monoculture cropping creates uniform shallow rooting and seasonal bare-ground exposure.\n"
                "  4. Habitat Quality: Absence of continuous floral bloom or shelter leads to severe microbial and pollinator mortality.\n"
                "  5. Compound Ecological Impact: Deep decoupling of the carbon-water-biodiversity cycle."
            ).format(soc=soc, rainfall=rainfall or moisture, land_use=land_use)
            
            synthesized_explanations.append(chain_desc)
            compound_stress_factors.append("Arid Monoculture Soil-Water Collapse")
            priority_knowledge_ids.extend(["FAO-SOC-001", "IPCC-AGRO-001", "AGRO-INTER-002", "GSBI-BIO-001"])

        # 2. Tri-Metric Synergy: Pollution + Habitat Diversity + Species Richness
        if (pollution in ["moderate", "high", "severe"]) and \
           (habitat_diversity in ["low", "homogenous", "fragmented"]) and \
           (species_richness in ["low", "critically_low"]):

            chain_desc = (
                "Multi-Variable Nexus [Agrochemical Pollution ({pollution}) + Habitat Fragmentation ({habitat_diversity}) + Species Richness ({species_richness})]:\n"
                "  1. Chemical Stress: High pesticide or nitrate runoff damages soil microarthropods and aquatic bio-indicators.\n"
                "  2. Structural Barrier: Fragmented landscape devoid of hedgerows eliminates buffer filtration and thermal refugia.\n"
                "  3. Population Collapse: Keystone pollinators and beneficial predators cannot escape pesticide exposure zones, driving local extirpation."
            ).format(pollution=pollution, habitat_diversity=habitat_diversity, species_richness=species_richness)

            synthesized_explanations.append(chain_desc)
            compound_stress_factors.append("Chemical Contamination & Habitat Fragmentation")
            priority_knowledge_ids.extend(["UNEP-RIP-001", "IUCN-CORR-001", "IUCN-POLL-002"])

        # 3. Tri-Metric Synergy: Temperature + Rainfall + Deforestation
        if (temp in ["high", "extreme"]) and \
           (rainfall in ["low", "very_low"] or moisture in ["low", "very_low"]) and \
           (deforestation in ["moderate", "severe", "historical"]):

            chain_desc = (
                "Multi-Variable Nexus [Thermal Stress ({temp}) + Rainfall Deficit ({rainfall}) + Canopy Loss ({deforestation})]:\n"
                "  1. Thermal Forcing: Canopy loss increases solar irradiance, elevating topsoil temperatures by 4-8°C.\n"
                "  2. Moisture Depletion: High vapor pressure deficits drive rapid desiccation of organic residues.\n"
                "  3. Desertification Loop: Hydrophobic crusting induces severe runoff erosion during sporadic storms, preventing spontaneous re-seeding."
            ).format(temp=temp, rainfall=rainfall or moisture, deforestation=deforestation)

            synthesized_explanations.append(chain_desc)
            compound_stress_factors.append("Thermal Desertification & Microclimate Degradation")
            priority_knowledge_ids.extend(["UNEP-DEFOR-002", "IPCC-AGRO-001", "IPCC-WATER-002"])

        # 4. General Multi-Metric Synthesis (when 3+ variables are present but don't match specific predefined archetypes)
        if len(synthesized_explanations) == 0 and len(variables) >= 3:
            var_keys = [k for k in variables.keys() if k not in ["region", "geo_coordinates"]]
            chain_desc = (
                f"Multi-Variable Nexus [{' + '.join(var_keys[:4])}]:\n"
                f"  • Cross-Coupling: Interactions between {var_keys[0]} ({variables.get(var_keys[0])}) "
                f"and {var_keys[1]} ({variables.get(var_keys[1])}) directly govern {var_keys[2]} ({variables.get(var_keys[2])}).\n"
                f"  • Causal Trajectory: Biological and hydrological feedbacks amplify environmental pressure on native biota.\n"
                f"  • Target Leverage: Integrated restoration targeting both belowground soil biotic networks and aboveground vegetative diversity."
            )
            synthesized_explanations.append(chain_desc)
            compound_stress_factors.append("Multi-Variable Ecological Imbalance")
            priority_knowledge_ids.extend(["FAO-SOC-001", "IPCC-AGRO-001", "IUCN-CORR-001"])

        return {
            "compound_stress_factors": compound_stress_factors,
            "causal_chains": synthesized_explanations,
            "priority_knowledge_ids": list(set(priority_knowledge_ids)),
            "variable_count": len(variables)
        }
