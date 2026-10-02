from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from graph.state_schema import TicketState
from graph.nodes.triage_node import triage_node
from graph.nodes.investigate_node import investigate_node
from graph.nodes.fix_node import fix_node
from graph.nodes.validate_node import validate_node
from graph.nodes.human_review_node import human_review_node
from graph.nodes.finalize_node import finalize_node

graph = StateGraph(TicketState)

graph.add_node("triage", triage_node)
graph.add_node("investigate", investigate_node)
graph.add_node("fix", fix_node)
graph.add_node("validate", validate_node)
graph.add_node("human_review", human_review_node)
graph.add_node("finalize", finalize_node)

graph.set_entry_point("triage")

def route_after_triage(state):
    if not state["is_technical"] and state["triage_confidence"] in ("MEDIUM", "LOW"):
        return "human_review"
    elif state["is_technical"]:
        return "investigate"
    else:
        return "finalize"

graph.add_conditional_edges("triage", route_after_triage, {
    "investigate": "investigate",
    "finalize": "finalize",
    "human_review": "human_review",
})

def route_after_investigate(state):
    if state["found_bug"]:
        return "fix"
    else:
        return "human_review"

graph.add_conditional_edges("investigate", route_after_investigate, {
    "fix": "fix",
    "human_review": "human_review",
})

graph.add_edge("fix", "validate")

def route_after_validate(state):
    if state["validation_passed"]:
        return "finalize"
    elif state["attempt_count"] < state["max_attempts"]:
        return "fix"
    else:
        return "human_review"

graph.add_conditional_edges("validate", route_after_validate, {
    "finalize": "finalize",
    "fix": "fix",
    "human_review": "human_review",
})

def route_after_human_review(state):
    if state["human_decision"] == "modify":
        return "fix"
    else:
        return "finalize"

graph.add_conditional_edges("human_review", route_after_human_review, {
    "fix": "fix",
    "finalize": "finalize",
})

graph.add_edge("finalize", END)

checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer)