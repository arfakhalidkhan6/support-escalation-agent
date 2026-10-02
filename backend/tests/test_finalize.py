from graph.nodes.finalize_node import finalize_node

def test_finalize_non_technical():
    state = {"is_technical": False, "validation_passed": False, "human_decision": ""}
    result = finalize_node(state)
    assert result["status"] == "resolved_non_technical"

def test_finalize_auto_resolved():
    state = {"is_technical": True, "validation_passed": True, "human_decision": ""}
    result = finalize_node(state)
    assert result["status"] == "resolved_automatically"

def test_finalize_rejected_max_retries():
    state = {
        "is_technical": True,
        "validation_passed": False,
        "human_decision": "reject",
        "escalation_reason": "max_retries",
    }
    result = finalize_node(state)
    assert result["status"] == "escalated"

def test_finalize_rejected_stuck():
    state = {
        "is_technical": True,
        "validation_passed": False,
        "human_decision": "reject",
        "escalation_reason": "stuck",
    }
    result = finalize_node(state)
    assert result["status"] == "escalated_unresolved"