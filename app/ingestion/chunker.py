from hashlib import sha256
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.ingestion.models import SourceDocument, DocumentChunk


def chunk_document(
    document: SourceDocument,
    chunk_size: int = 500,
    chunk_overlap: int = 75
) -> list[DocumentChunk]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    texts = splitter.split_text(document.content)

    source_path = Path(document.source).expanduser().resolve()
    source_name = source_path.stem
    source_id = sha256(str(source_path).encode("utf-8")).hexdigest()

    chunks = []

    for index, text in enumerate(texts):
        chunk = DocumentChunk(
            chunk_id=f"{source_name}-{source_id}-{index}",
            content=text,
            source=document.source,
            metadata={
                **document.metadata,
                "chunk_index": str(index)
            }
        )

        chunks.append(chunk)

    return chunks
