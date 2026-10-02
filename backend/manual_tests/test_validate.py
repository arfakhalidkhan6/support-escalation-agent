from dotenv import load_dotenv
load_dotenv()

from graph.nodes.validate_node import validate_node

test_state = {
    "proposed_fix": '''tasks = []

def add_task(name):
    tasks.append(name)

def delete_task(name):
    tasks.remove(name)

def export_report():
    for i in range(len(tasks)):
        print(f"Task {i+1}: {tasks[i]}")

# Test it manually
add_task("Buy groceries")
add_task("Clean house")
add_task("Finish assignment")
export_report()
'''
}

result = validate_node(test_state)
print("Validation passed:", result["validation_passed"])
print("Feedback:", result["validation_feedback"])