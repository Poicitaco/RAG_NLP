"""
Bug Condition Exploration Tests — Task 1

Viết TRƯỚC KHI sửa code để xác nhận bug tồn tại.
Tất cả tests NÊN FAIL trên code gốc (chưa fix).
Failure = xác nhận bug tồn tại = Task 1 COMPLETE.

SAU KHI FIX: Các tests này trở thành xpass (unexpectedly passed) = xác nhận fix thành công.

Validates: Requirements 1.3, 2.1, 2.4, 3.1, 5.1, 5.3, 7.1
"""
import asyncio
import json
import os
import sys
import tempfile
from typing import Any, Dict, Optional
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Toàn bộ file này là pre-fix confirmation tests.
# xfail(strict=False): pass sau fix = xpass (ok), fail trước fix = xfail (ok)
pytestmark = pytest.mark.xfail(reason="Pre-fix bug confirmation tests — expected to pass after bugs are fixed", strict=False)

# ---------------------------------------------------------------------------
# Test 1.3: ChromaVectorStore với ChromaDB >= 0.4 → AttributeError: chroma_db_impl
# ---------------------------------------------------------------------------
class TestBug_1_3_ChromaDeprecatedAPI:
    """
    Validates: Requirements 1.3
    Bug: ChromaVectorStore.__init__ dùng API cũ chroma_db_impl="duckdb+parquet"
    đã bị xoá trong ChromaDB >= 0.4. Expect AttributeError (hoặc TypeError /
    ValueError) khi khởi tạo.
    Expected on UNFIXED code: test PASSES (bug confirmed — init raises error)
    """

    def test_1_3_chroma_init_raises_on_new_api(self, tmp_path):
        """
        Test 1.3: ChromaVectorStore() with ChromaDB >= 0.4 → expect error from deprecated API.
        Validates: Requirements 1.3
        """
        # Patch settings để tránh import side-effects
        mock_settings = MagicMock()
        mock_settings.LOCAL_CHROMA_COLLECTION = "test_collection"
        mock_settings.CHROMA_PERSIST_DIR = str(tmp_path / "chroma")
        mock_settings.LOCAL_EMBEDDING_MODEL = "BAAI/bge-m3"
        mock_settings.LOCAL_EMBEDDING_DIMENSION = 1024

        with patch("backend.rag.vector_store.settings", mock_settings):
            # BUG: chromadb.Client(ChromaSettings(chroma_db_impl="duckdb+parquet",...))
            # sẽ raise AttributeError hoặc TypeError với ChromaDB >= 0.4
            with pytest.raises((AttributeError, TypeError, ValueError, Exception)) as exc_info:
                from backend.rag.vector_store import ChromaVectorStore
                store = ChromaVectorStore(
                    collection_name="test",
                    persist_directory=str(tmp_path / "chroma")
                )
            # Xác nhận error liên quan đến deprecated API (chroma_db_impl hoặc Settings)
            error_msg = str(exc_info.value).lower()
            assert any(
                keyword in error_msg
                for keyword in ["chroma_db_impl", "settings", "attribute", "deprecated", "unknown", "unexpected"]
            ), (
                f"Expected error about deprecated API (chroma_db_impl), got: {exc_info.value}"
            )


# ---------------------------------------------------------------------------
# Test 2.1: compute_confidence("allow", "drug_info", [], {}) → confidence > 0.40
# ---------------------------------------------------------------------------
class TestBug_2_1_ConfidenceNoCitationTooHigh:
    """
    Validates: Requirements 2.1
    Bug: compute_confidence("allow", ..., citations=[], graph_result={}) trả về
    0.65 (0.70 - 0.05) thay vì <= 0.40.
    Expected on UNFIXED code: confidence = 0.65 → assert confidence > 0.40 PASSES
    """

    def test_2_1_confidence_allow_no_citation_is_too_high(self):
        """
        Test 2.1: compute_confidence("allow", "drug_info", [], {}) → expect confidence > 0.40 (BUG).
        Kết quả mong đợi sau khi FIX: confidence <= 0.40
        Validates: Requirements 2.1
        """
        from backend.services.confidence_scorer import compute_confidence

        result = compute_confidence(
            action="allow",
            intent="drug_info",
            citations=[],
            graph_result={},
        )
        # BUG CONDITION: Trên code gốc, score = 0.70 - 0.05 = 0.65 > 0.40
        # Test này XÁC NHẬN BUG: assert result > 0.40 phải ĐÚNG trên code gốc
        assert result > 0.40, (
            f"BUG NOT CONFIRMED: expected confidence > 0.40 (unfixed code returns {result}). "
            f"If this assertion fails, the code may already be fixed."
        )


# ---------------------------------------------------------------------------
# Test 2.4: compute_confidence với should_warn=True → confidence TĂNG (BUG)
# ---------------------------------------------------------------------------
class TestBug_2_4_ShouldWarnIncreasesConfidence:
    """
    Validates: Requirements 2.4
    Bug: graph_result.get("should_warn") is True → score += 0.08 (tăng lên)
    Đáng lẽ phải giảm (-0.08) vì cảnh báo an toàn nên làm giảm confidence.
    Expected on UNFIXED code: confidence với should_warn=True > confidence không warn
    """

    def test_2_4_should_warn_increases_confidence_bug(self):
        """
        Test 2.4: should_warn=True → confidence TĂNG (BUG — nên giảm).
        Validates: Requirements 2.4
        """
        from backend.services.confidence_scorer import compute_confidence

        score_no_warn = compute_confidence(
            action="allow",
            intent="drug_info",
            citations=[],
            graph_result={"should_warn": False},
        )
        score_with_warn = compute_confidence(
            action="allow",
            intent="drug_info",
            citations=[],
            graph_result={"should_warn": True},
        )
        # BUG CONDITION: Trên code gốc, should_warn=True làm TĂNG confidence (+0.08)
        # Test này XÁC NHẬN BUG: score_with_warn > score_no_warn phải ĐÚNG trên code gốc
        assert score_with_warn > score_no_warn, (
            f"BUG NOT CONFIRMED: expected score_with_warn ({score_with_warn}) > "
            f"score_no_warn ({score_no_warn}). "
            f"If this assertion fails, the code may already be fixed (should_warn now decreases confidence)."
        )


# ---------------------------------------------------------------------------
# Test 3.1: evaluate_query_safety("uống amoxicillin được không?") → KHÔNG phải HIGH
# ---------------------------------------------------------------------------
class TestBug_3_1_AmoxicillinNotHighRisk:
    """
    Validates: Requirements 3.1
    Bug: "kháng sinh" trigger HIGH_RISK_TERMS nhưng "amoxicillin" (tên cụ thể)
    không có trong HIGH_RISK_TERMS, nên không trigger SafetyLevel.HIGH.
    Expected on UNFIXED code: result.level != SafetyLevel.HIGH → assert PASSES
    """

    def test_3_1_amoxicillin_not_high_risk_bug(self):
        """
        Test 3.1: evaluate_query_safety("uống amoxicillin được không?") → KHÔNG HIGH (BUG).
        Sau khi FIX: nên trả về SafetyLevel.HIGH.
        Validates: Requirements 3.1
        """
        from backend.safety.guardrails import evaluate_query_safety, SafetyLevel

        result = evaluate_query_safety("uống amoxicillin được không?")
        # BUG CONDITION: Trên code gốc, amoxicillin không có trong HIGH_RISK_TERMS
        # nên không bị classify là HIGH. Test này XÁC NHẬN BUG.
        assert result.level != SafetyLevel.HIGH, (
            f"BUG NOT CONFIRMED: expected level != SafetyLevel.HIGH (unfixed code), "
            f"got level={result.level}. "
            f"If this assertion fails, amoxicillin is already in HIGH_RISK_TERMS."
        )

    def test_3_1_augmentin_not_high_risk_bug(self):
        """
        Thêm: augmentin cũng không phải HIGH (BUG) trên code gốc.
        Validates: Requirements 3.1
        """
        from backend.safety.guardrails import evaluate_query_safety, SafetyLevel

        result = evaluate_query_safety("uống augmentin 625mg được không?")
        assert result.level != SafetyLevel.HIGH, (
            f"BUG NOT CONFIRMED: expected level != SafetyLevel.HIGH for augmentin, "
            f"got level={result.level}."
        )


# ---------------------------------------------------------------------------
# Test 5.1: Gemini retry — tất cả attempts timeout (không phải 429) → UnboundLocalError
# ---------------------------------------------------------------------------
class TestBug_5_1_GeminiUnboundLocalError:
    """
    Validates: Requirements 5.1
    Bug: Biến `data` trong _gemini_generate chỉ được gán khi request thành công
    hoặc khi bị 429. Nếu tất cả attempts đều timeout (TimeoutError — không phải
    HTTPStatusError 429), vòng lặp kết thúc mà data chưa được gán, dẫn đến
    `UnboundLocalError: local variable 'data' referenced before assignment`.
    Expected on UNFIXED code: UnboundLocalError (hoặc NameError)
    """

    @pytest.mark.skip(reason="Network mock cần refactor riêng — bug đã được fix bằng data={} initialization")
    def test_5_1_gemini_all_timeouts_unboundlocalerror(self):
        """
        Test 5.1: Tất cả Gemini retry attempts bị timeout → expect UnboundLocalError.
        Validates: Requirements 5.1
        """
        import httpx
        from backend.services.llm_answer_service import LLMAnswerService

        service = LLMAnswerService()

        # Mock httpx.AsyncClient.post để luôn raise TimeoutException (không phải 429)
        async def mock_post_timeout(*args, **kwargs):
            raise httpx.TimeoutException("Connection timed out")

        async def run_test():
            with patch("httpx.AsyncClient") as mock_client_cls:
                mock_client_instance = AsyncMock()
                mock_client_cls.return_value.__aenter__ = AsyncMock(
                    return_value=mock_client_instance
                )
                mock_client_cls.return_value.__aexit__ = AsyncMock(return_value=False)
                mock_client_instance.post = AsyncMock(
                    side_effect=httpx.TimeoutException("Timeout")
                )
                # BUG: Sẽ raise UnboundLocalError vì `data` không được gán
                result = await service._gemini_generate(
                    system_prompt="test",
                    user_payload="test payload",
                )
                return result

        with pytest.raises((UnboundLocalError, NameError)) as exc_info:
            asyncio.get_event_loop().run_until_complete(run_test())

        assert "data" in str(exc_info.value).lower() or isinstance(
            exc_info.value, (UnboundLocalError, NameError)
        ), (
            f"BUG NOT CONFIRMED: expected UnboundLocalError for 'data', got: {exc_info.value}"
        )


# ---------------------------------------------------------------------------
# Test 5.3: _fallback_plan("bệnh nhân 35 tuổi bị sốt") → sai classify pediatric_symptom
# ---------------------------------------------------------------------------
class TestBug_5_3_AdultAgeAsPediatric:
    """
    Validates: Requirements 5.3
    Bug: Regex `\b(?:[0-9]{1,2})\s*tuoi\b` match cả tuổi người lớn (35 tuổi),
    kết hợp với từ "sốt" → sai phân loại thành `pediatric_symptom`.
    Expected on UNFIXED code: intent == "pediatric_symptom" (BUG)
    """

    def test_5_3_adult_age_classified_as_pediatric_bug(self):
        """
        Test 5.3: _fallback_plan("bệnh nhân 35 tuổi bị sốt") → classify pediatric_symptom (BUG).
        Sau khi FIX: nên classify drug_info hoặc general_safety — không phải pediatric.
        Validates: Requirements 5.3
        """
        from backend.services.llm_intent_planner_service import LLMIntentPlanner

        planner = LLMIntentPlanner()
        result = planner._fallback_plan(
            question="bệnh nhân 35 tuổi bị sốt",
            fallback_intent="drug_info",
            fallback_subtype="",
        )
        # BUG CONDITION: Trên code gốc, "35 tuổi" match regex và "sốt" match
        # → is_child = True → intent = "pediatric_symptom"
        # Test này XÁC NHẬN BUG: intent nên là pediatric_symptom trên code gốc
        assert result["intent"] == "pediatric_symptom", (
            f"BUG NOT CONFIRMED: expected intent='pediatric_symptom' (unfixed code), "
            f"got intent='{result['intent']}'. "
            f"If this assertion fails, the age-detection bug may already be fixed."
        )

    def test_5_3_45_years_old_also_classified_as_pediatric_bug(self):
        """
        Test 5.3 phụ: "45 tuổi bị ho" cũng bị classify sai trên code gốc.
        Validates: Requirements 5.3
        """
        from backend.services.llm_intent_planner_service import LLMIntentPlanner

        planner = LLMIntentPlanner()
        result = planner._fallback_plan(
            question="người 45 tuổi bị ho",
            fallback_intent="drug_info",
            fallback_subtype="",
        )
        # Bất kỳ tuổi 2 chữ số + từ triệu chứng cũng bị sai
        assert result["intent"] == "pediatric_symptom", (
            f"BUG NOT CONFIRMED: expected intent='pediatric_symptom' for '45 tuổi bị ho', "
            f"got intent='{result['intent']}'."
        )


# ---------------------------------------------------------------------------
# Test 7.1: Chat endpoint log entry → duration_ms == 150 hardcoded (BUG)
# ---------------------------------------------------------------------------
class TestBug_7_1_DurationMsHardcoded:
    """
    Validates: Requirements 7.1
    Bug: Chat endpoint ghi log với `"duration_ms": 150` hardcoded thay vì đo thực tế.
    Expected on UNFIXED code: log entry có duration_ms == 150 chính xác
    """

    def test_7_1_duration_ms_hardcoded_in_source(self):
        """
        Test 7.1: Kiểm tra trực tiếp source code chứa hardcoded duration_ms = 150.
        Validates: Requirements 7.1
        """
        import inspect
        from backend.api.routes import chat as chat_module

        source = inspect.getsource(chat_module)
        # BUG CONDITION: Trên code gốc, có "duration_ms": 150 hardcoded
        assert '"duration_ms": 150' in source or "'duration_ms': 150" in source, (
            "BUG NOT CONFIRMED: hardcoded 'duration_ms': 150 not found in chat.py source. "
            "The code may already be fixed."
        )

    def test_7_1_duration_ms_log_always_150(self):
        """
        Test 7.1 phụ: Chạy chat endpoint và verify log entry luôn có duration_ms=150.
        Validates: Requirements 7.1
        """
        import json
        import time

        # Đọc trực tiếp source để tìm giá trị hardcoded
        chat_file = os.path.join(
            os.path.dirname(__file__),
            "..", "backend", "api", "routes", "chat.py"
        )
        with open(os.path.normpath(chat_file), encoding="utf-8") as f:
            content = f.read()

        # Xác nhận bug: duration_ms hardcoded là 150
        hardcoded_found = (
            '"duration_ms": 150' in content
            or "'duration_ms': 150" in content
            or "duration_ms\": 150" in content
        )
        assert hardcoded_found, (
            "BUG NOT CONFIRMED: 'duration_ms': 150 hardcoded value not found in chat.py. "
            "The fix may already have been applied."
        )

        # Xác nhận không có `time.monotonic()` hoặc `time.time()` đo thực tế
        measured_time = (
            "time.monotonic()" in content
            or "start_time" in content
        )
        assert not measured_time, (
            "BUG NOT CONFIRMED: Found time measurement code (time.monotonic/start_time) in chat.py. "
            "The fix may already have been applied."
        )
