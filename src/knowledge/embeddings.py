"""
Text Vectorizer and Embedding Engine.
Implements normalized subword/word n-gram TF-IDF vectorization with Cosine Similarity.
Provides high-precision scientific term matching and dense semantic projection.
"""

import re
import math
from typing import List, Dict, Tuple
import numpy as np


class ScientificEmbedder:
    """
    Computes vector embeddings for scientific queries and knowledge chunks.
    Combines unigrams and bigrams with inverse document frequency (IDF) weighting.
    """

    def __init__(self):
        self.vocabulary: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}
        self.fitted: bool = False

    def _tokenize(self, text: str) -> List[str]:
        """Tokenizes scientific text into normalized words and bigrams."""
        text_clean = text.lower()
        # Replace non-alphanumeric with spaces, retaining scientific symbols where useful
        text_clean = re.sub(r"[^\w\s-]", " ", text_clean)
        words = [w for w in text_clean.split() if len(w) > 1]
        
        # Unigrams
        tokens = list(words)
        
        # Bigrams for scientific phrases (e.g. "soil organic", "organic carbon", "cover crops")
        for i in range(len(words) - 1):
            tokens.append(f"{words[i]}_{words[i+1]}")
            
        return tokens

    def fit(self, documents: List[str]) -> "ScientificEmbedder":
        """Calculates vocabulary and document frequencies."""
        doc_count = len(documents)
        df: Dict[str, int] = {}

        for doc in documents:
            tokens = set(self._tokenize(doc))
            for t in tokens:
                df[t] = df.get(t, 0) + 1

        # Build vocabulary for tokens appearing in at least 1 doc
        self.vocabulary = {token: idx for idx, token in enumerate(sorted(df.keys()))}
        
        # Calculate smooth IDF: ln((1 + N) / (1 + df)) + 1
        self.idf = {
            token: math.log((1.0 + doc_count) / (1.0 + freq)) + 1.0
            for token, freq in df.items()
        }
        self.fitted = True
        return self

    def transform(self, texts: List[str]) -> np.ndarray:
        """Transforms a list of texts into L2-normalized TF-IDF embedding vectors."""
        if not self.fitted:
            raise RuntimeError("Embedder must be fitted before calling transform().")

        dim = len(self.vocabulary)
        vectors = np.zeros((len(texts), dim), dtype=np.float32)

        for i, text in enumerate(texts):
            tokens = self._tokenize(text)
            tf: Dict[str, int] = {}
            for t in tokens:
                if t in self.vocabulary:
                    tf[t] = tf.get(t, 0) + 1

            for token, count in tf.items():
                idx = self.vocabulary[token]
                tf_weight = 1.0 + math.log(count)
                vectors[i, idx] = tf_weight * self.idf[token]

            # L2 Normalize vector
            norm = np.linalg.norm(vectors[i])
            if norm > 0:
                vectors[i] /= norm

        return vectors

    def embed_query(self, query: str) -> np.ndarray:
        """Transforms a single query into an L2-normalized vector."""
        return self.transform([query])[0]

    @staticmethod
    def cosine_similarity(vec_a: np.ndarray, matrix_b: np.ndarray) -> np.ndarray:
        """Computes cosine similarity between a single vector and a matrix of vectors."""
        # Since vectors are already L2 normalized, dot product equals cosine similarity
        return np.dot(matrix_b, vec_a)
