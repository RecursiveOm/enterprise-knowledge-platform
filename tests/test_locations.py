from pathlib import Path

from app.core.config import PROJECT_ROOT, Settings
from app.ingestion.chunker import chunk_document
from app.ingestion.loader import load_text_document


def test_settings_paths_do_not_depend_on_working_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    settings = Settings(_env_file=None, chroma_path="test_db")
    assert settings.chroma_path == str(PROJECT_ROOT / "test_db")
    assert Path(Settings.model_config["env_file"]) == PROJECT_ROOT / ".env"
    settings.chroma_path = "another_db"
    assert settings.chroma_path == str(PROJECT_ROOT / "another_db")
    settings.chroma_path = str(tmp_path / "absolute_db")
    assert settings.chroma_path == str(tmp_path / "absolute_db")


def test_document_source_is_stable_for_relative_and_absolute_paths(tmp_path, monkeypatch):
    path = tmp_path / "policy.txt"
    path.write_text("Refunds take five days.", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    relative = load_text_document(Path("policy.txt"))
    absolute = load_text_document(path)
    assert relative.source == absolute.source == str(path)
    assert chunk_document(relative)[0].chunk_id == chunk_document(absolute)[0].chunk_id


def test_same_filename_in_different_directories_has_distinct_chunk_ids(tmp_path):
    chunks = []
    for department in ("support", "operations"):
        path = tmp_path / department / "policy.txt"
        path.parent.mkdir()
        path.write_text("Department policy.", encoding="utf-8")
        chunks.append(chunk_document(load_text_document(path))[0])
    assert chunks[0].chunk_id != chunks[1].chunk_id
