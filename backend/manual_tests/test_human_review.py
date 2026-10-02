from graph.nodes.human_review_node import human_review_node

test_state = {
    "ticket_text": "The app crashes every time I try to export my task report.",
    "bug_info": "The export_report function loops one index too far, causing an IndexError.",
    "proposed_fix": "for i in range(len(tasks)): ...",
    "validation_feedback": "IndexError: list index out of range",
}

result = human_review_node(test_state)
print("Human decision:", result["human_decision"])
print("Human feedback:", result["human_feedback"])