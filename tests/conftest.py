"""Shared pytest fixtures for SafeRAG test suite."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

STATE_FILE = Path(__file__).resolve().parents[1] / "data" / "conversation_states.json"


@pytest.fixture(autouse=True)
def clean_pytest_conversation_sessions():
    """Xóa các session bắt đầu bằng 'pytest-' khỏi conversation_states.json trước mỗi test."""
    _remove_pytest_sessions()
    yield
    _remove_pytest_sessions()


def _remove_pytest_sessions() -> None:
    if not STATE_FILE.exists():
        return
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        cleaned = {k: v for k, v in data.items() if not k.startswith("pytest")}
        if len(cleaned) != len(data):
            STATE_FILE.write_text(
                json.dumps(cleaned, ensure_ascii=False, indent=2), encoding="utf-8"
            )
    except Exception:
        pass
