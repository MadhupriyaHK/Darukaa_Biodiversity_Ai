"""
Corpus loader and validator for the scientific knowledge base.
Loads authentic papers, reports, and models from FAO, IPCC, IUCN, etc.
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

from src.config import KNOWLEDGE_DIR

logger = logging.getLogger(__name__)


class KnowledgeCorpus:
    """Manages verified scientific knowledge records."""

    def __init__(self, knowledge_dir: Path = KNOWLEDGE_DIR):
        self.knowledge_dir = Path(knowledge_dir)
        self.items: List[Dict[str, Any]] = []
        self.items_by_id: Dict[str, Dict[str, Any]] = {}
        self.load_corpus()

    def load_corpus(self) -> None:
        """Loads all JSON knowledge base files."""
        self.items.clear()
        self.items_by_id.clear()

        if not self.knowledge_dir.exists():
            logger.warning(f"Knowledge directory {self.knowledge_dir} does not exist.")
            return

        json_files = list(self.knowledge_dir.glob("*.json"))
        for file_path in json_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    records = json.load(f)
                    if isinstance(records, list):
                        for rec in records:
                            rec_id = rec.get("id")
                            if rec_id:
                                rec["file_source"] = file_path.name
                                self.items.append(rec)
                                self.items_by_id[rec_id] = rec
                    logger.info(f"Loaded {len(records)} records from {file_path.name}")
            except Exception as e:
                logger.error(f"Error loading knowledge file {file_path}: {e}")

        logger.info(f"Total scientific knowledge items loaded: {len(self.items)}")

    def get_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        return self.items_by_id.get(item_id)

    def get_by_variable(self, variable_name: str) -> List[Dict[str, Any]]:
        """Returns all knowledge items concerning a specific environmental variable."""
        return [
            item for item in self.items
            if variable_name in item.get("variables", [])
        ]

    def all_items(self) -> List[Dict[str, Any]]:
        return self.items
