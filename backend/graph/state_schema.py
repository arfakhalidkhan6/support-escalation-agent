from typing import TypedDict

class TicketState(TypedDict):
    ticket_text: str
    is_technical: bool
    bug_info: str
    validation_feedback: str
    validation_passed: bool
    proposed_fix: str
    human_decision: str
    max_attempts: int
    attempt_count: int
    human_decision: str
    human_feedback: str
    status: str
    customer_message: str
    triage_confidence: str
    escalation_reason: str