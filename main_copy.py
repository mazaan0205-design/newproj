import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain import hub

# --- THE UI THAT WAS WORKING ---
st.set_page_config(page_title="Wortex AI Agent", page_icon="🤖")
st.title("🤖 Wortex.ai Agent")

# --- SECRETS CHECK ---
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    st.error("❌ Missing GROQ_API_KEY in Secrets!")
    st.stop()

# --- TOOL IMPORTS ---
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
except Exception as e:
    st.error(f"⚠️ Tool Error: {e}")
    st.stop()

# --- THE AGENT BRAIN ---
llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=api_key)
prompt = hub.pull("hwchase17/openai-functions-agent")

# This specific line is the one that worked in Python 3.12
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Ask Wortex..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            response = agent_executor.invoke({"input": user_input})
            st.markdown(response["output"])
            st.session_state.messages.append({"role": "assistant", "content": response["output"]})
        except Exception as e:
            st.error(f"Logic Error: {e}")
