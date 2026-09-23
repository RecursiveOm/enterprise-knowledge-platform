from pathlib import Path

from app.ingestion.loader import load_text_document
from app.ingestion.chunker import chunk_document


def test_document_ingestion():

    path = Path(__file__).resolve().parents[1] / Path(
        "data/raw/refund_policy.txt"
    )

    document = load_text_document(
        path,
        metadata={
            "department": "support",
            "region": "global"
        }
    )

    chunks = chunk_document(
        document,
        chunk_size=120,
        chunk_overlap=20
    )

    assert document.source == str(path)

    assert (
        document.metadata["department"]
        == "support"
    )

    assert len(chunks) > 1

    assert (
        chunks[0].source
        == str(path)
    )

    assert (
        chunks[0].metadata["department"]
        == "support"
    )

    assert (
        chunks[0].metadata["chunk_index"]
        == "0"
    )
