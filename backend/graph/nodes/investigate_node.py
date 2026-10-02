import os
from pathlib import Path
from groq import Groq
from graph.state_schema import TicketState

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

demo_app_path = Path(__file__).resolve().parents[3] / "demo_app" / "tasks.py"

def investigate_node(state: TicketState) -> dict:
    ticket_text = state["ticket_text"]

    with open(demo_app_path, "r") as f:
        code_content = f.read()

    prompt = f"""You are a bug investigator. You are given a customer's ticket describing a problem, and the source code of the application.

Carefully read the ticket and the code to determine what is causing the issue described.

Customer ticket: "{ticket_text}"

Source code:
{code_content}

Reply in exactly this format:
Line 1: FOUND or NOT_FOUND
Line 2: if FOUND, a clear one-to-two sentence description of the bug. If NOT_FOUND, leave this line empty.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    answer = response.choices[0].message.content.strip()
    lines = answer.split("\n", 1)

    status = lines[0].strip().upper()
    found_bug = "FOUND" in status and "NOT" not in status
    bug_info = lines[1].strip() if found_bug and len(lines) > 1 else ""

    escalation_reason = "" if found_bug else "stuck"

    return {"found_bug": found_bug, "bug_info": bug_info, "escalation_reason": escalation_reason}