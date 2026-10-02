import os
from groq import Groq
from graph.state_schema import TicketState

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def triage_node(state: TicketState) -> dict:
    ticket_text = state["ticket_text"]

    prompt = f"""You are a support ticket classifier.

TECHNICAL = the software is broken, crashing, erroring, or behaving incorrectly.
NON-TECHNICAL = account access, billing, or how-to questions — nothing is actually broken.

Examples:
"I forgot my password" -> NON-TECHNICAL
"The app crashes when I export a report" -> TECHNICAL
"I was charged twice this month" -> NON-TECHNICAL

Ticket: "{ticket_text}"

Reply in exactly this format:
Line 1: TECHNICAL or NON-TECHNICAL
Line 2: confidence as HIGH, MEDIUM, or LOW
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    answer = response.choices[0].message.content.strip()
    lines = answer.split("\n")

    classification = lines[0].strip().upper()
    is_technical = "TECHNICAL" in classification and "NON" not in classification

    confidence = lines[1].strip().upper() if len(lines) > 1 else "MEDIUM"

    escalation_reason = "stuck" if (not is_technical and confidence in ("MEDIUM", "LOW")) else ""

    return {"is_technical": is_technical, "triage_confidence": confidence, "escalation_reason": escalation_reason}