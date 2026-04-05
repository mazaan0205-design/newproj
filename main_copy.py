import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain import hub

# Page Config
st.set_page_config(page_title="Wortex AI", page_icon="🤖")
st.title("🤖 Wortex.ai Agent")

# Get API Key
api_key = st.secrets.get("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY not found in Secrets!")
    st.stop()

# Import Tools
from mytools.calculator import calculator
from mytools.list_files import list_files
from mytools.send_email import send_email
from mytools.file_creation import create_file
from mytools.profit_loss_tool import profit_loss_excel_tool
from mytools.read_file import read_file
from mytools.whatsapp import send_whatsapp_message 

tools = [calculator, list_files, send_email, create_file, 
         profit_loss_excel_tool, read_file, send_whatsapp_message]

# Initialize Brain & Agent (Updated Import Logic)
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, groq_api_key=api_key)
prompt = hub.pull("hwchase17/openai-functions-agent")

# Fix: Use create_tool_calling_agent instead of the deprecated one
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Session State for History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if user_input := st.chat_input("How can I help?"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            response = agent_executor.invoke({"input": user_input})
            final_text = response["output"]
            st.markdown(final_text)
            st.session_state.messages.append({"role": "assistant", "content": final_text})
