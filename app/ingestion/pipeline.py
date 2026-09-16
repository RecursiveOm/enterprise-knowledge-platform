from pathlib import Path

from app.ingestion.loader import load_text_document
from app.ingestion.chunker import chunk_document
from app.ingestion.indexer import index_chunks


def ingest_text_document(
    path: Path,
    metadata: dict[str, str] | None = None
) -> int:

    document = load_text_document(
        path=path,
        metadata=metadata
    )

    chunks = chunk_document(document)

    indexed_count = index_chunks(chunks)

    return indexed_count