import chromadb

from app.core.config import settings
from app.ingestion.models import DocumentChunk


COLLECTION_NAME = "enterprise_knowledge"


def index_chunks(chunks: list[DocumentChunk]) -> int:
    if not chunks:
        return 0

    client = chromadb.PersistentClient(
        path=settings.chroma_path
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    ids = []
    documents = []
    metadatas = []

    for chunk in chunks:
        ids.append(chunk.chunk_id)
        documents.append(chunk.content)

        metadata = {
            **chunk.metadata,
            "source": chunk.source
        }

        metadatas.append(metadata)

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    return len(chunks)  