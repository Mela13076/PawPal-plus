# Simple, dependency-free retrieval for a small Markdown knowledge base.
# Retrieval only (no LLM). Returns the most relevant text chunks for a query.

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Optional


@dataclass
class Chunk:
    source: str          # filename
    text: str            # chunk content
    score: float = 0.0   # relevance score (filled during retrieval)


_WORD_RE = re.compile(r"[a-z0-9]+")


def _tokenize(text: str) -> List[str]:
    return _WORD_RE.findall(text.lower())


def _chunk_text(text: str, chunk_size: int = 350, overlap: int = 60) -> List[str]:
    """
    Chunk by words to keep it simple and stable for markdown text.
    chunk_size/overlap are in 'words'.
    """
    words = text.split()
    if not words:
        return []

    chunks: List[str] = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end]).strip()
        if chunk:
            chunks.append(chunk)
        if end == len(words):
            break
        start = max(0, end - overlap)

    return chunks


def load_knowledge_chunks(
    knowledge_dir: str | Path = "knowledge",
    chunk_size: int = 350,
    overlap: int = 60,
) -> List[Chunk]:
    """
    Reads all .md files in knowledge_dir and returns a list of Chunk objects.
    """
    kdir = Path(knowledge_dir)
    if not kdir.exists() or not kdir.is_dir():
        raise FileNotFoundError(f"Knowledge directory not found: {kdir.resolve()}")

    chunks: List[Chunk] = []
    for md_path in sorted(kdir.glob("*.md")):
        text = md_path.read_text(encoding="utf-8", errors="ignore")
        for chunk_text in _chunk_text(text, chunk_size=chunk_size, overlap=overlap):
            chunks.append(Chunk(source=md_path.name, text=chunk_text))

    return chunks


def _score_chunk(query_tokens: List[str], chunk_text: str) -> float:
    """
    Very lightweight keyword scoring:
    - counts token occurrences
    - small bonus for phrase matches (adjacent tokens)
    """
    chunk_lower = chunk_text.lower()

    score = 0.0
    for tok in query_tokens:
        # simple count of substring occurrences
        score += chunk_lower.count(tok)

    # phrase bonus
    if len(query_tokens) >= 2:
        for i in range(len(query_tokens) - 1):
            phrase = f"{query_tokens[i]} {query_tokens[i+1]}"
            if phrase in chunk_lower:
                score += 2.0

    return score


def retrieve_context(
    query: str,
    chunks: List[Chunk],
    k: int = 3,
    min_score: float = 1.0,
) -> List[Tuple[str, str, float]]:
    """
    Returns top-k relevant chunks for a query.

    Output list items: (source_filename, chunk_text, score)
    """
    query_tokens = _tokenize(query)
    if not query_tokens:
        return []

    scored: List[Chunk] = []
    for c in chunks:
        s = _score_chunk(query_tokens, c.text)
        if s >= min_score:
            scored.append(Chunk(source=c.source, text=c.text, score=s))

    scored.sort(key=lambda x: x.score, reverse=True)
    top = scored[:k]
    return [(c.source, c.text, c.score) for c in top]


def build_query_from_tasks(task_descriptions: List[str], species: Optional[str] = None) -> str:
    """
    Helper to build a query string from task descriptions and optional species.
    This makes retrieval more relevant without needing an LLM.
    """
    parts: List[str] = []
    if species:
        parts.append(species)
    parts.extend(task_descriptions)
    parts.append("scheduling conflicts priority routine")
    return " ".join(parts)
