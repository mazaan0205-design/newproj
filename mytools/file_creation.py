from langchain.tools import tool
import os

@tool
def create_file(filename: str, content: str, onDesktop=False):
    """Creates a Python file on the computer with given name and content."""
    
    if(onDesktop):
        # Save to Desktop
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        filename = os.path.join(desktop, f"{filename}")
    
    file_name = filename 
    with open(file_name, "w") as f:
        f.write(content)


    