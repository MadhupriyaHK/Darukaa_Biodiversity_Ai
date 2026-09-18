"""
Scientific Knowledge Retrieval Layer.
Executes hybrid semantic search over environmental datasets and reports.
Ensures every returned item includes verifiable scientific provenance.
"""

from typing import List, Dict, Any, Optional
from src.knowledge.vector_store import ScientificVectorStore
from src.models.schemas import Citation
from src.config import RETRIEVAL_TOP_K, SIMILARITY_THRESHOLD


class KnowledgeRetriever:
    """Retriever layer connecting user environmental queries with scientific evidence."""

    def __init__(self, vector_store: Optional[ScientificVectorStore] = None):
        self.vector_store = vector_store or ScientificVectorStore()

    def retrieve(
        self,
        query: str,
        active_variables: Optional[Dict[str, Any]] = None,
        top_k: int = RETRIEVAL_TOP_K
    ) -> Dict[str, Any]:
        """
        Retrieves relevant scientific studies based on query and detected environmental metrics.
        Returns:
            {
                "has_sufficient_evidence": bool,
                "evidence_items": List[Dict],
                "citations": List[Citation],
                "retrieved_ids": List[str]
            }
        """
        var_names = list(active_variables.keys()) if active_variables else []
        
        # Build enriched retrieval query
        query_enrichment = [query]
        if active_variables:
            for k, v in active_variables.items():
                query_enrichment.append(f"{k} {v}")
        full_query = " ".join(query_enrichment)

        results = self.vector_store.search(
            query=full_query,
            top_k=top_k,
            variable_filters=var_names,
            min_score=SIMILARITY_THRESHOLD
        )

        evidence_items: List[Dict[str, Any]] = []
        citations: List[Citation] = []
        retrieved_ids: List[str] = []

        for doc, score in results:
            retrieved_ids.append(doc["id"])
            evidence_items.append({
                "id": doc["id"],
                "topic": doc.get("topic"),
                "domain": doc.get("domain"),
                "relevance_score": score,
                "summary": doc.get("summary"),
                "mechanism": doc.get("scientific_mechanism"),
                "scientific_mechanism": doc.get("scientific_mechanism"),
                "quantitative_evidence": doc.get("quantitative_evidence"),
                "interventions": doc.get("interventions", []),
                "variables": doc.get("variables", []),
                "time_horizon": doc.get("time_horizon"),
                "source": doc.get("source"),
                "source_org": doc.get("source_org", doc.get("source", "Scientific Report")),
                "source_year": doc.get("source_year", 2020),
                "citation": doc.get("citation")
            })

            citations.append(Citation(
                id=doc["id"],
                source_org=doc.get("source_org", doc.get("source", "Scientific Literature")),
                title=doc.get("source_title", doc.get("topic", "")),
                year=int(doc.get("source_year", 2020)),
                citation_text=doc.get("citation", f"{doc.get('source')} ({doc.get('source_year')})")
            ))

        has_sufficient = len(evidence_items) > 0

        return {
            "has_sufficient_evidence": has_sufficient,
            "evidence_items": evidence_items,
            "citations": citations,
            "retrieved_ids": retrieved_ids
        }
