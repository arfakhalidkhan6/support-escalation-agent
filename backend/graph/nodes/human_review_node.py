from graph.state_schema import TicketState
from langgraph.types import interrupt

def human_review_node(state: TicketState) -> dict:
    escalation_reason = state.get("escalation_reason", "")

    if escalation_reason == "max_retries":
        answer = interrupt({
            "type": "max_retries",
            "ticket_text": state.get("ticket_text", ""),
            "bug_info": state.get("bug_info", ""),
            "proposed_fix": state.get("proposed_fix", ""),
            "validation_feedback": state.get("validation_feedback", ""),
            "options": ["reject", "modify"],
        })
        decision = answer.get("decision", "").strip().lower()
        human_feedback = answer.get("feedback", "")
        return {"human_decision": decision, "human_feedback": human_feedback}

    else:
        answer = interrupt({
            "type": "stuck",
            "ticket_text": state.get("ticket_text", ""),
            "question": "Can you identify the bug yourself?",
        })
        can_identify = answer.get("can_identify", "").strip().lower()
        if can_identify == "yes":
            return {"human_decision": "modify", "bug_info": answer.get("bug_description", "")}
        else:
            return {"human_decision": "reject", "human_feedback": ""}