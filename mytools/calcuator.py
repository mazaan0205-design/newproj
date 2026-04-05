from langchain.tools import tool

@tool
def calculator(a,b, operation):
    """Performs addition and subtraction over numbers."""
    if operation == 'addition':
        return a + b
    elif operation == 'subtraction':
        return a - b 