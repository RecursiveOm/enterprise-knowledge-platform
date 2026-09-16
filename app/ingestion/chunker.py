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

    source_name = Path(document.source).stem

    chunks = []

    for index, text in enumerate(texts):
        chunk = DocumentChunk(
            chunk_id=f"{source_name}-{index}",
            content=text,
            source=document.source,
            metadata={
                **document.metadata,
                "chunk_index": str(index)
            }
        )

        chunks.append(chunk)

    return chunks