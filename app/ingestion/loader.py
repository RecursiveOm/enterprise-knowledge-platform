from pathlib import Path

from app.ingestion.models import SourceDocument


def load_text_document(
    path: Path,
    metadata: dict[str, str] | None = None
) -> SourceDocument:

    path = Path(path).expanduser().resolve()

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {path}"
        )

    if path.suffix.lower() != ".txt":
        raise ValueError(
            f"Only .txt files are supported: {path}"
        )

    if metadata is None:
        metadata = {}

    text = path.read_text(
        encoding="utf-8"
    )

    return SourceDocument(
        content=text,
        source=str(path),
        metadata=metadata
    )
