"""
In-memory Vector Store for scientific knowledge retrieval.
Supports vector similarity search, metadata filtering, and thresholding.
"""

from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from src.knowledge.embeddings import ScientificEmbedder
from src.knowledge.corpus import KnowledgeCorpus


class ScientificVectorStore:
    """Indexed vector store for environmental literature."""

    def __init__(self, corpus: Optional[KnowledgeCorpus] = None):
        self.corpus = corpus or KnowledgeCorpus()
        self.embedder = ScientificEmbedder()
        self.doc_records: List[Dict[str, Any]] = []
        self.embeddings_matrix: Optional[np.ndarray] = None
        self.build_index()

    def build_index(self) -> None:
        """Indexes all knowledge base chunks."""
        self.doc_records = self.corpus.all_items()
        if not self.doc_records:
            return

        # Prepare searchable text representation for each document
        documents: List[str] = []
        for doc in self.doc_records:
            parts = [
                doc.get("topic", ""),
                doc.get("domain", ""),
                " ".join(doc.get("variables", [])),
                doc.get("summary", ""),
                doc.get("scientific_mechanism", ""),
                doc.get("quantitative_evidence", ""),
                " ".join(doc.get("interventions", [])),
                doc.get("source", ""),
                doc.get("source_title", "")
            ]
            documents.append(" ".join(parts))

        # Fit embedder and transform all documents
        self.embedder.fit(documents)
        self.embeddings_matrix = self.embedder.transform(documents)

    def search(
        self,
        query: str,
        top_k: int = 4,
        variable_filters: Optional[List[str]] = None,
        min_score: float = 0.05
    ) -> List[Tuple[Dict[str, Any], float]]:
        """
        Searches the index for documents matching the query.
        Applies variable overlap boosting and returns sorted (doc, score) pairs.
        """
        if self.embeddings_matrix is None or len(self.doc_records) == 0:
            return []

        query_vec = self.embedder.embed_query(query)
        similarities = self.embedder.cosine_similarity(query_vec, self.embeddings_matrix)

        results: List[Tuple[Dict[str, Any], float]] = []

        for idx, doc in enumerate(self.doc_records):
            base_score = float(similarities[idx])
            
            # Hybrid boost if document covers user's specified environmental variables
            boost = 0.0
            if variable_filters:
                doc_vars = set(doc.get("variables", []))
                overlap = len(doc_vars.intersection(set(variable_filters)))
                if overlap > 0:
                    boost = 0.15 * overlap

            final_score = base_score + boost

            if final_score >= min_score:
                results.append((doc, round(final_score, 4)))

        # Sort descending by score
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
