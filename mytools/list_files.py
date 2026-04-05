from langchain.tools import tool
import os

@tool
def list_files(path: str = ".") -> str:
    """Lists all files in the specified path."""

    files = [
        f for f in os.listdir(path)
        if os.path.isfile(os.path.join(path, f))
    ]

    return ", ".join(files)