import os
from langchain.tools import tool

@tool
def create_file(filename: str, content: str):
    """Creates a new file with the specified content."""
    try:
        with open(filename, 'w') as f:
            f.write(content)
        return f"✅ File '{filename}' created successfully."
    except Exception as e:
        return f"❌ File Creation Error: {str(e)}"
