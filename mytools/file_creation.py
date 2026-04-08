from langchain.tools import tool

@tool
def calculator(expression: str):
    """Evaluates mathematical expressions (e.g., '2 + 2' or '50 * 10')."""
    try:
        # Using eval safely for basic math
        result = eval(expression, {"__builtins__": None}, {})
        return f"📊 Result: {result}"
    except Exception as e:
        return f"❌ Calculation Error: {str(e)}"
