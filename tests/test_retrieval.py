from pathlib import Path

from app.core.config import settings
from app.ingestion.pipeline import ingest_text_document
from app.retrieval.retriever import retrieve_documents


DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"


def test_semantic_retrieval(
    tmp_path
):

    original_chroma_path = (
        settings.chroma_path
    )

    settings.chroma_path = str(
        tmp_path / "chroma_db"
    )

    try:

        ingest_text_document(
            DATA_DIR / "refund_policy.txt",
            {
                "department": "support",
                "region": "global",
                "version": "1"
            }
        )

        ingest_text_document(
            DATA_DIR / "shipping_policy.txt",
            {
                "department": "operations",
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

        filtered_results = retrieve_documents(
            "How long does delivery take?",
            k=3,
            filters={
                "department": "operations"
            }
        )

        assert len(filtered_results) > 0

        assert filtered_results[0].source.endswith(
            "shipping_policy.txt"
        )

        for result in filtered_results:

            assert (
                result.metadata["department"]
                == "operations"
            )

    finally:

        settings.chroma_path = (
            original_chroma_path
        )
