# creating data structure for history, id of history elements
history = []
index = 1

# core logic (calculation, get_history, undo)
def calculator(operation, a, b):
    operation = operation.lower()
    global index, history
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        result = "Error: Division by zero" if b == 0 else a / b
    else:
        result = "Invalid operation"

    record = {
        "id": index,
        "operation": operation,
        "a": a,
        "b": b,
        "result": result
    }

    index += 1
    history.append(record)
    return result

def get_history():
    if not history:
        return []
    return history

def undo():
    if history:
        removed = history.pop()
        return removed
    else:
        return None