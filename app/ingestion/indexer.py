from app.core.vector_store import get_collection
from app.ingestion.models import DocumentChunk


def index_chunks(
    chunks: list[DocumentChunk]
) -> int:

    if not chunks:
        return 0

    collection = get_collection()

    ids = []
    documents = []
    metadatas = []

    for chunk in chunks:

        ids.append(
            chunk.chunk_id
        )

        documents.append(
            chunk.content
        )

        metadata = {
            **chunk.metadata,
            "source": chunk.source
        }

        metadatas.append(
            metadata
        )

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    return len(chunks)