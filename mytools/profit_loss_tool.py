from langchain.tools import tool
import pandas as pd
import os

@tool
def profit_loss_excel_tool(file_name: str, incomes: dict, expenses: dict) -> str:
    """
    Creates a real Excel Profit & Loss file on the desktop.
    
    Args:
        file_name: Name of the Excel file (without .xlsx)
        incomes: Dictionary of income sources {name: amount}
        expenses: Dictionary of expense categories {name: amount}
    
    Returns:
        Path to the created Excel file.
    """
    # Prepare data
    data = {"Category": list(incomes.keys()) + list(expenses.keys()) + ["Profit/Loss"],
            "Amount": list(incomes.values()) + list(expenses.values()) +
                      [sum(incomes.values()) - sum(expenses.values())]}
    
    df = pd.DataFrame(data)
    
    # Save to Desktop
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    full_path = os.path.join(desktop, f"{file_name}.xlsx")
    df.to_excel(full_path, index=False)
    
    return f"Excel file created: {full_path}"