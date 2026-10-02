from dotenv import load_dotenv
load_dotenv()

from graph.nodes.investigate_node import investigate_node

test_state = {"ticket_text": "The app crashes every time I try to export my task report."}
result = investigate_node(test_state)

print("Found bug:", result["found_bug"])
print("Bug info:", result["bug_info"])