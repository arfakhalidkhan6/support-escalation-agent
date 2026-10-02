from graph.state_schema import TicketState

def finalize_node(state: TicketState) -> dict:
    is_technical = state.get("is_technical", False)
    validation_passed = state.get("validation_passed", False)
    human_decision = state.get("human_decision", "")
    escalation_reason = state.get("escalation_reason", "")

    if not is_technical:
        status = "resolved_non_technical"
        customer_message = "Thanks for reaching out! Your request has been received, and our support team will get back to you shortly."

    elif human_decision == "reject" and escalation_reason == "stuck":
        status = "escalated_unresolved"
        customer_message = "Thanks for reporting this. We weren't able to reproduce the issue on our end, so we've forwarded your case to our team for a closer look."

    elif human_decision == "reject":
        status = "escalated"
        customer_message = "Thanks for reporting this. Our team has reviewed your issue, and a support specialist will follow up with you shortly to resolve it."

    elif validation_passed:
        status = "resolved_automatically"
        customer_message = "Good news — we identified the issue you reported and resolved it. You shouldn't run into this problem again. Thanks for letting us know!"

    else:
        status = "unresolved"
        customer_message = "Thanks for reporting this. Our team is looking into it and will follow up shortly."

    return {"status": status, "customer_message": customer_message}