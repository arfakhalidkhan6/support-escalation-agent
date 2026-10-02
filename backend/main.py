from dotenv import load_dotenv
load_dotenv()

import uuid
from fastapi import FastAPI
from langgraph.types import Command
from schemas.ticket import TicketRequest
from graph.graph import app as graph_app

app = FastAPI(title="Support Escalation Agent")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/ticket")
def submit_ticket(ticket: TicketRequest):
    ticket_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": ticket_id}}

    state = {
        "ticket_text": ticket.message,
        "attempt_count": 0,
        "max_attempts": 2,
    }
    result = graph_app.invoke(state, config=config)
    return format_result(result, ticket_id)


@app.post("/review/{ticket_id}")
def submit_review(ticket_id: str, answer: dict):
    config = {"configurable": {"thread_id": ticket_id}}
    result = graph_app.invoke(Command(resume=answer), config=config)
    return format_result(result, ticket_id)


def format_result(result, ticket_id):
    if "__interrupt__" in result:
        return {
            "status": "pending_review",
            "ticket_id": ticket_id,
            "review": result["__interrupt__"][0].value,
        }
    return {"status": result["status"], "customer_message": result["customer_message"]}