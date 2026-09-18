"""
TEST 5: Scientific evidence retrieval (RAG pipeline).
Verifies that knowledge from the authentic corpus (FAO, IPCC, IUCN) is retrieved and cited accurately.
"""

from src.knowledge.corpus import KnowledgeCorpus
from src.knowledge.vector_store import ScientificVectorStore
from src.knowledge.retriever import KnowledgeRetriever


def test_corpus_contains_authentic_literature():
    corpus = KnowledgeCorpus()
    assert len(corpus.all_items()) >= 6
    
    orgs = [item.get("source_org", item.get("source", "")) for item in corpus.all_items()]
    assert any("FAO" in o for o in orgs)
    assert any("IPCC" in o for o in orgs)
    assert any("IUCN" in o for o in orgs)


def test_vector_store_retrieves_relevant_evidence():
    vector_store = ScientificVectorStore()
    results = vector_store.search("legume cover crops soil organic carbon moisture", top_k=2)
    assert len(results) > 0
    top_doc, score = results[0]
    assert score > 0.1
    assert "FAO" in top_doc["id"] or "AGRO" in top_doc["id"]


def test_retriever_pipeline_provenance():
    retriever = KnowledgeRetriever()
    res = retriever.retrieve(
        query="hedgerows and pollinator corridors for fragmented habitats",
        active_variables={"habitat_diversity": "low", "species_richness": "low"}
    )
    assert res["has_sufficient_evidence"] is True
    assert len(res["evidence_items"]) > 0
    assert len(res["citations"]) > 0
    first_citation = res["citations"][0]
    assert first_citation.citation_text is not None and len(first_citation.citation_text) > 5
