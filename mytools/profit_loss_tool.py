import pandas as pd
from langchain.tools import tool

@tool
def profit_loss_excel_tool(data: list, filename: str = "profit_loss.xlsx"):
    """
    Creates an Excel sheet for Profit and Loss data.
    Input 'data' should be a list of dictionaries like [{'Category': 'Sales', 'Amount': 5000}].
    """
    try:
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        return f"✅ Excel sheet '{filename}' created successfully."
    except Exception as e:
        return f"❌ Excel Error: {str(e)}"
