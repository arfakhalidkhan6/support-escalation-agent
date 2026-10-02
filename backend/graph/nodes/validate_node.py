import subprocess
import shutil
from pathlib import Path
from graph.state_schema import TicketState

demo_app_path = Path(__file__).resolve().parents[3] / "demo_app" / "tasks.py"
temp_path = demo_app_path.parent / "tasks_temp.py"

def validate_node(state: TicketState) -> dict:
    proposed_fix = state["proposed_fix"]

    with open(temp_path, "w") as f:
        f.write(proposed_fix)

    result = subprocess.run(
        ["python", str(temp_path)],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        shutil.copy(temp_path, demo_app_path)
        return {"validation_passed": True, "validation_feedback": ""}
    else:
        if state["attempt_count"] >= state["max_attempts"]:
            escalation_reason = "max_retries"
        else:
            escalation_reason = ""
        return {
            "validation_passed": False,
            "validation_feedback": result.stderr.strip(),
            "escalation_reason": escalation_reason,
        }