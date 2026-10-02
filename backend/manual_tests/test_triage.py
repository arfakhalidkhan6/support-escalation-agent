from dotenv import load_dotenv
load_dotenv()

from graph.nodes.triage_node import triage_node

test_state = {"ticket_text": "The app crashes every time I try to export my task report."}
result = triage_node(test_state)

print("Is technical:", result["is_technical"])
print("Confidence:", result["triage_confidence"])