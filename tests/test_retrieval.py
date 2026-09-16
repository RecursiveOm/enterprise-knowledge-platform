from pathlib import Path

from app.core.config import settings
from app.ingestion.pipeline import ingest_text_document
from app.retrieval.retriever import retrieve_documents


def test_semantic_retrieval(tmp_path):
    original_chroma_path = settings.chroma_path

    settings.chroma_path = str(
        tmp_path / "chroma_db"
    )

    try:
        ingest_text_document(
            Path("data/raw/refund_policy.txt"),
            {
                "department": "support",
                "region": "global",
                "version": "1"
            }
        )

        ingest_text_document(
            Path("data/raw/shipping_policy.txt"),
            {
                "department": "operations",
                "region": "global",
                "version": "1"
            }
        )

        ingest_text_document(
            Path("data/raw/security_policy.txt"),
            {
                "department": "security",
                "region": "global",
                "version": "1"
            }
        )

        results = retrieve_documents(
            "How long does my refund take?",
            k=3
        )

        assert len(results) > 0
        assert results[0].source.endswith(
            "refund_policy.txt"
        )

    finally:
        settings.chroma_path = original_chroma_path