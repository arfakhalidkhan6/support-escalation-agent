from dotenv import load_dotenv
load_dotenv()

from graph.nodes.fix_node import fix_node

test_state = {
    "attempt_count": 0,
    "bug_info": "The export_report function loops one index too far (range(len(tasks)+1)), causing an IndexError when accessing tasks[i] on the last iteration.",
    "proposed_fix": "",
    "validation_feedback": "",
}

result = fix_node(test_state)
print("Proposed fix:")
print(result["proposed_fix"])