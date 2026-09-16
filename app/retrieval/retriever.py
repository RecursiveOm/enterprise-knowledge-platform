from app.core.vector_store import get_collection
from app.retrieval.models import RetrievalResult


def retrieve_documents(
    query: str,
    k: int = 5,
    filters: dict[str, str] | None = None
) -> list[RetrievalResult]:

    collection = get_collection()

    count = collection.count()

    if count == 0:
        return []

    n_results = min(k, count)
    where_filter = None

    if filters is not None:
        where_filter = filters

    results = collection.query(
    query_texts=[query],
    n_results=n_results,
    where=where_filter,
    include=[
        "documents",
        "metadatas",
        "distances"
    ]
    )

    ids = results["ids"][0]
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    retrieved = []

    for index in range(len(ids)):
        metadata = dict(metadatas[index])

        source = metadata.pop(
            "source",
            ""
        )

        result = RetrievalResult(
            chunk_id=ids[index],
            content=documents[index],
            source=source,
            metadata=metadata,
            distance=distances[index]
        )

        retrieved.append(result)

    return retrieved