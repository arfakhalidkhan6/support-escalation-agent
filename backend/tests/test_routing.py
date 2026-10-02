from graph.graph import (
    route_after_triage,
    route_after_investigate,
    route_after_validate,
    route_after_human_review,
)

def test_route_after_triage_technical():
    state = {"is_technical": True, "triage_confidence": "HIGH"}
    assert route_after_triage(state) == "investigate"

def test_route_after_triage_non_technical_high_confidence():
    state = {"is_technical": False, "triage_confidence": "HIGH"}
    assert route_after_triage(state) == "finalize"

def test_route_after_triage_non_technical_low_confidence():
    state = {"is_technical": False, "triage_confidence": "LOW"}
    assert route_after_triage(state) == "human_review"

def test_route_after_investigate_found_bug():
    state = {"found_bug": True}
    assert route_after_investigate(state) == "fix"

def test_route_after_investigate_no_bug():
    state = {"found_bug": False}
    assert route_after_investigate(state) == "human_review"

def test_route_after_validate_passed():
    state = {"validation_passed": True, "attempt_count": 1, "max_attempts": 2}
    assert route_after_validate(state) == "finalize"

def test_route_after_validate_failed_attempts_remain():
    state = {"validation_passed": False, "attempt_count": 0, "max_attempts": 2}
    assert route_after_validate(state) == "fix"

def test_route_after_validate_failed_max_attempts():
    state = {"validation_passed": False, "attempt_count": 2, "max_attempts": 2}
    assert route_after_validate(state) == "human_review"

def test_route_after_human_review_modify():
    state = {"human_decision": "modify"}
    assert route_after_human_review(state) == "fix"

def test_route_after_human_review_reject():
    state = {"human_decision": "reject"}
    assert route_after_human_review(state) == "finalize"