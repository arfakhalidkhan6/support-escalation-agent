tasks = []

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
