import os
from pathlib import Path
from groq import Groq
from graph.state_schema import TicketState

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

demo_app_path = Path(__file__).resolve().parents[3] / "demo_app" / "tasks.py"

def fix_node(state: TicketState) -> dict:
    bug_info = state["bug_info"]
    attempt_count = state["attempt_count"] + 1
    human_feedback = state.get("human_feedback", "")

    with open(demo_app_path, "r") as f:
        code_content = f.read()

    if state["attempt_count"] > 0:
        retry_context = f"""
Previous attempt: {state['proposed_fix']}
Why it failed: {state['validation_feedback']}
Do not repeat this exact mistake — propose a different fix.
"""
    else:
        retry_context = ""

    if human_feedback:
        human_context = f"\nA human reviewer gave this guidance: {human_feedback}\n"
    else:
        human_context = ""

    prompt = f"""You are a code-fixing assistant. You are given a description of a bug and the source code containing it.

Bug: {bug_info}

Code:
{code_content}
{retry_context}{human_context}
Propose a corrected version of the code that fixes this bug.

Reply with only the corrected code, no explanation.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    proposed_fix = response.choices[0].message.content.strip()

    return {"proposed_fix": proposed_fix, "attempt_count": attempt_count}