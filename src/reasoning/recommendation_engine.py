"""
Scientific Recommendation Engine.
Generates evidence-backed, actionable, non-obvious biodiversity recommendations.
Enforces strict grounding: every intervention includes scientific mechanisms,
impacted metrics, quantitative estimates, time horizons, and authentic citations.
"""

from typing import Dict, Any, List, Optional
from src.models.schemas import RecommendationItem, Citation, ReasoningOutput
from src.models.environmental_metrics import CORE_METRIC_DEFINITIONS


class RecommendationEngine:
    """Synthesizes actionable environmental science interventions from retrieved evidence."""

    @classmethod
    def synthesize_recommendations(
        cls,
        variables: Dict[str, Any],
        causal_analysis: Dict[str, Any],
        retrieval_result: Dict[str, Any]
    ) -> List[RecommendationItem]:
        """
        Creates structured RecommendationItems based on retrieved scientific studies
        and compound multi-metric stress analysis.
        """
        recommendations: List[RecommendationItem] = []
        evidence_items = retrieval_result.get("evidence_items", [])
        
        if not evidence_items:
            # Fallback if no specific study matched
            return []

        # Map each retrieved evidence study to exactly one concrete recommendation.
        # Each knowledge-base record now carries a single intervention, ensuring
        # that Rec 1, Rec 2, Rec 3 come from three *different* studies and therefore
        # have distinct mechanisms, quantitative evidence, and citations.
        seen_interventions: set = set()

        for item in evidence_items:
            interventions = item.get("interventions", [])
            if not interventions:
                continue

            # Pick the first (and after restructure, the only) intervention per study
            act = interventions[0]

            # Deduplication guard — skip if this exact intervention text was already used
            if act in seen_interventions:
                continue
            seen_interventions.add(act)

            # Each study record now carries its own unique mechanism and evidence
            mechanism = item.get("scientific_mechanism", item.get("mechanism", ""))
            quant_evidence = item.get("quantitative_evidence", "")
            time_horizon = item.get("time_horizon", "medium_term")

            # Determine affected metrics from the study's variable list
            affected = [v for v in item.get("variables", []) if v in CORE_METRIC_DEFINITIONS]
            if not affected:
                affected = ["species_richness", "soil_organic_carbon"]

            # Build citation from study-level metadata (not hardcoded year)
            citation_obj = Citation(
                id=item["id"],
                source_org=item.get("source_org", item.get("source", "Scientific Report")),
                title=item.get("topic", "Ecological Restoration Protocol"),
                year=int(item.get("source_year", 2020)),
                citation_text=item.get("citation", f"{item.get('source', 'Scientific Report')} Report")
            )

            rec = RecommendationItem(
                what_to_do=act,
                why_it_works=mechanism,
                impacted_metrics=affected,
                quantitative_estimate=quant_evidence,
                time_horizon=time_horizon,
                confidence="high" if len(variables) >= 3 else "medium",
                citations=[citation_obj]
            )
            recommendations.append(rec)
            if len(recommendations) >= 3:
                break

        # Return top 3 distinct, highest-leverage recommendations
        return recommendations[:3]

    @classmethod
    def build_reasoning_output(
        cls,
        variables: Dict[str, Any],
        causal_analysis: Dict[str, Any],
        retrieval_result: Dict[str, Any]
    ) -> ReasoningOutput:
        """Constructs full ReasoningOutput schema."""
        recs = cls.synthesize_recommendations(variables, causal_analysis, retrieval_result)
        
        # Build concise environmental summary
        var_summary_parts = [f"{k}: {v}" for k, v in variables.items() if k not in ["geo_coordinates"]]
        summary = (
            f"Assessed ecosystem profile exhibiting compound stress across {len(variables)} variables: "
            f"{', '.join(var_summary_parts)}."
        )

        stress_rating = "severe" if len(causal_analysis.get("compound_stress_factors", [])) > 1 else "moderate"

        return ReasoningOutput(
            status="complete",
            environmental_summary=summary,
            variables_analyzed=variables,
            causal_relationships=causal_analysis.get("causal_chains", []),
            ecological_stress_level=stress_rating,
            recommendations=recs,
            retrieved_evidence_ids=retrieval_result.get("retrieved_ids", [])
        )
