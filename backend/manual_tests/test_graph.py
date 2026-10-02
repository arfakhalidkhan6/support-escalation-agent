from dotenv import load_dotenv
load_dotenv()

from graph.graph import app

test_state = {
    "ticket_text": "The app crashes every time I try to export my task report.",
    "attempt_count": 0,
    "max_attempts": 2,
    "proposed_fix": "",
    "validation_feedback": "",
}

result = app.invoke(test_state)

print("Status:", result["status"])
print("Customer message:", result["customer_message"])