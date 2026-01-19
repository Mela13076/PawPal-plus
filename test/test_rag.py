import os
import pytest

from rag import load_knowledge_chunks, retrieve_context, build_query_from_tasks
from llm_client import test_gemini_connection


def test_load_knowledge_chunks_nonempty():
    chunks = load_knowledge_chunks("knowledge")
    assert chunks, "Expected knowledge chunks to be loaded."
    assert any(c.source == "dog_care.md" for c in chunks)


def test_retrieve_context_returns_relevant_chunk():
    chunks = load_knowledge_chunks("knowledge")
    results = retrieve_context("feeding routine", chunks, k=3, min_score=1.0)
    assert results, "Expected at least one retrieved chunk."
    assert any("feeding" in text.lower() for _src, text, _score in results)


def test_build_query_from_tasks_includes_keywords():
    query = build_query_from_tasks(["morning walk", "medication"], species="dog")
    assert "dog" in query
    assert "morning walk" in query
    assert "medication" in query


@pytest.mark.skipif(
    not os.getenv("GEMINI_API_KEY"),
    reason="GEMINI_API_KEY not set; skipping live Gemini test.",
)
def test_gemini_connection_smoke():
    response = test_gemini_connection()
    assert response, "Expected a non-empty response from Gemini."
