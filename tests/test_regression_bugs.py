"""
Regression tests xác nhận các bugs tồn tại trong SafeRAG Pharma.

Mỗi test FAIL trước khi fix, PASS sau khi fix.
"""
import re
import inspect
import textwrap
import pytest


# ---------------------------------------------------------------------------
# Bug 1: confidence_scorer — should_warn=True làm TĂNG score (sai logic)
# ---------------------------------------------------------------------------
def test_should_warn_should_decrease_confidence():
    """BUG EXISTS: should_warn=True cộng thêm 0.08 vào score thay vì trừ đi."""
    from backend.services.confidence_scorer import compute_confidence

    score_with_warn = compute_confidence(
        "allow", "drug_info", [{"id": "S1"}], {"should_warn": True}
    )
    score_without_warn = compute_confidence(
        "allow", "drug_info", [{"id": "S1"}], {"should_warn": False}
    )
    # BUG EXISTS: hiện tại score_with_warn > score_without_warn vì `score += 0.08`
    assert score_with_warn < score_without_warn, (
        "should_warn=True phải GIẢM confidence, không phải tăng"
    )


# ---------------------------------------------------------------------------
# Bug 2: confidence_scorer — citation_count==0 chỉ giảm 0.05, phải cap ≤ 0.40
# ---------------------------------------------------------------------------
def test_zero_citations_should_cap_score_at_040():
    """BUG EXISTS: citation_count==0 chỉ trừ 0.05, không cap ≤ 0.40."""
    from backend.services.confidence_scorer import compute_confidence

    # allow base=0.70, không citation → phải cap ≤ 0.40
    # BUG EXISTS: trả về 0.70 - 0.05 = 0.65 (> 0.40)
    score = compute_confidence("allow", "drug_info", [], {})
    assert score <= 0.40, (
        f"Không có citation phải cap score ≤ 0.40, nhưng nhận được {score}"
    )


# ---------------------------------------------------------------------------
# Bug 3: chat.py — duration_ms hardcode 150
# ---------------------------------------------------------------------------
def test_duration_ms_is_not_hardcoded():
    """BUG EXISTS: duration_ms được gán cứng là 150 thay vì đo thực tế."""
    import os
    chat_path = os.path.join(
        os.path.dirname(__file__), "..", "backend", "api", "routes", "chat.py"
    )
    with open(chat_path, encoding="utf-8") as f:
        source = f.read()

    # BUG EXISTS: dòng `"duration_ms": 150` tồn tại trong source
    assert '"duration_ms": 150' not in source, (
        'duration_ms hardcode 150 vẫn còn trong chat.py — phải đo thời gian thực tế'
    )


# ---------------------------------------------------------------------------
# Bug 4: chat_history_service — không có file locking (race condition)
# ---------------------------------------------------------------------------
def test_chat_history_service_uses_file_locking():
    """BUG EXISTS: _save_history / _load_history không dùng bất kỳ file locking nào."""
    from backend.services import chat_history_service as mod

    source = inspect.getsource(mod)
    has_lock = any(
        token in source
        for token in ("filelock", "FileLock", "fcntl", "msvcrt", "portalocker", "threading.Lock")
    )
    # BUG EXISTS: không có cơ chế locking → race condition khi ghi đồng thời
    assert has_lock, (
        "ChatHistoryService không có file locking — dễ xảy ra race condition"
    )


# ---------------------------------------------------------------------------
# Bug 5: llm_answer_service._gemini_generate — UnboundLocalError khi all retries fail
# ---------------------------------------------------------------------------
def test_gemini_generate_data_initialized_before_loop():
    """BUG EXISTS: biến `data` chỉ được gán bên trong try-block; nếu tất cả retry
    đều raise exception (không phải 429) thì `data` chưa được gán → UnboundLocalError
    khi truy cập `data.get("candidates")` sau vòng lặp."""
    from backend.services.llm_answer_service import LLMAnswerService

    # inspect.getsource trả về source có indent → cần dedent trước khi phân tích
    raw = inspect.getsource(LLMAnswerService._gemini_generate)
    source = textwrap.dedent(raw)
    lines = source.splitlines()

    data_init_line = None
    for_loop_line = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        # Tìm `data = {}` hoặc `data = None` — khởi tạo TRƯỚC vòng lặp
        if data_init_line is None and re.match(r'^data\s*=\s*(\{\}|None)', stripped):
            data_init_line = i
        if for_loop_line is None and re.match(r'^for\s+attempt\s+in\s+range', stripped):
            for_loop_line = i

    # BUG EXISTS: data_init_line là None (không có) HOẶC xuất hiện sau for_loop_line
    assert data_init_line is not None and (
        for_loop_line is None or data_init_line < for_loop_line
    ), "Biến `data` phải được khởi tạo TRƯỚC vòng for-retry để tránh UnboundLocalError"


# ---------------------------------------------------------------------------
# Bug 6: llm_intent_planner — regex tuổi không match '3 tháng tuổi' / '18 tháng'
# ---------------------------------------------------------------------------
def test_age_regex_matches_month_age_expressions():
    """BUG EXISTS: r'\\b(?:[0-9]{1,2})\\s*tuoi\\b' không khớp '3 tháng tuổi'
    hay '18 tháng' vì thiếu nhánh xử lý đơn vị 'tháng'.

    Sau khi fix, pattern phải match các biểu thức tháng tuổi và
    string cũ không được tồn tại trong source nữa.
    """
    from backend.services.llm_intent_planner_service import LLMIntentPlanner

    source = inspect.getsource(LLMIntentPlanner._fallback_plan)

    # BUG EXISTS nếu pattern cũ vẫn tồn tại (chỉ check 'tuoi', bỏ qua 'thang')
    old_broken_pattern = r'\b(?:[0-9]{1,2})\s*tuoi\b'
    assert old_broken_pattern not in source, (
        f"Pattern regex cũ vẫn còn trong source — bug chưa fix: "
        f"'{old_broken_pattern}' không match '3 tháng tuổi'"
    )

    # Sau khi fix, pattern mới phải match các biểu thức tháng tuổi
    match = re.search(r're\.search\(r"([^"]+)"', source)
    assert match is not None, "Không tìm thấy re.search(...) pattern trong _fallback_plan"

    current_pattern = match.group(1)
    month_cases = ["3 thang tuoi", "18 thang", "be 6 thang tuoi"]
    for case in month_cases:
        assert re.search(current_pattern, case) is not None, (
            f"Pattern hiện tại '{current_pattern}' vẫn không match '{case}'"
        )


# ---------------------------------------------------------------------------
# Bug 7: guardrails — câu hỏi kháng sinh general query
# ---------------------------------------------------------------------------
def test_general_antibiotic_question_not_blocked():
    """Kháng sinh là HIGH_RISK_TERMS (thuốc kê đơn) nên luôn block.
    Câu general query về kháng sinh + pregnancy vẫn phải block đúng."""
    from backend.safety.guardrails import evaluate_query_safety, SafetyLevel

    # Câu có pregnancy + kháng sinh → phải block (safety-critical)
    r1 = evaluate_query_safety(
        "kháng sinh amoxicillin hoạt động như thế nào cho phụ nữ mang thai?",
        context={}
    )
    assert r1.level == SafetyLevel.HIGH, "pregnancy + kháng sinh phải bị block"

    # Câu general về paracetamol (không high_risk) → allow
    r2 = evaluate_query_safety("Paracetamol là gì và tác dụng như thế nào?", context={})
    assert r2.should_answer is True, "câu general về paracetamol phải allow"


# ---------------------------------------------------------------------------
# Bug 8: orchestrator — log exception thiếu exc_info=True (mất traceback)
# ---------------------------------------------------------------------------
def test_orchestrator_exception_log_has_exc_info():
    """BUG EXISTS: app_logger.error('Lỗi trong orchestrator: {e}') không có
    exc_info=True nên traceback bị mất trong log."""
    from backend.agents import orchestrator as mod

    source = inspect.getsource(mod)

    # Tìm lệnh log lỗi trong orchestrator exception handler
    error_log_pattern = re.compile(
        r'app_logger\.error\s*\([^)]*orchestrator[^)]*\)',
        re.DOTALL
    )
    match = error_log_pattern.search(source)
    assert match is not None, "Không tìm thấy dòng log lỗi orchestrator trong source"

    log_call = match.group(0)
    # BUG EXISTS: exc_info không có trong log call → traceback bị mất
    assert "exc_info" in log_call, (
        f"app_logger.error trong orchestrator thiếu exc_info=True — traceback sẽ bị mất.\n"
        f"Dòng hiện tại: {log_call!r}"
    )
