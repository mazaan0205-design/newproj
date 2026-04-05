import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain import hub

# Page Config
st.set_page_config(page_title="Wortex AI", page_icon="🤖")

# DEBUG: Check if Groq Key exists
if "GROQ_API_KEY" not in st.secrets:
    st.error("❌ GROQ_API_KEY is missing from Secrets!")
    st.stop()

api_key = st.secrets["GROQ_API_KEY"]

# 3. IMPORT YOUR TOOLS
try:
    from mytools.calculator import calculator
    from mytools.list_files import list_files
    from mytools.send_email import send_email
    from mytools.file_creation import create_file
    from mytools.profit_loss_tool import profit_loss_excel_tool
    from mytools.read_file import read_file
    from mytools.whatsapp import send_whatsapp_message
    
    tools = [
        calculator, list_files, send_email, create_file, 
        profit_loss_excel_tool, read_file, send_whatsapp_message
    ]
except ImportError as e:
    st.error(f"⚠️ Tool Import Error: {e}. Check if 'mytools' folder has __init__.py")
    st.stop()

# 4. INITIALIZE AGENT
llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=api_key)
prompt = hub.pull("hwchase17/openai-functions-agent")
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# ... (The rest of your chat code from the previous message)
