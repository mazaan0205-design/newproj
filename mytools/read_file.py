from langchain.tools import tool
import os

# ... your existing create_file function ...

@tool
def read_file(filename: str) -> str:
    """Reads the content of a file and returns it as a string."""
    try:
        # If you want to support reading from Desktop by default, 
        # you could mirror your path logic from create_file here.
        with open(filename, "r") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return f"Error: The file '{filename}' was not found."
    except Exception as e:
        return f"Error reading file: {str(e)}"