import chromadb

from app.core.config import settings


COLLECTION_NAME = "enterprise_knowledge"


def get_collection():
    client = chromadb.PersistentClient(
        path=settings.chroma_path
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    return collection