import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain import hub

# 1. Setup
st.set_page_config(page_title="Wortex AI", page_icon="🤖")
st.title("🤖 Wortex.ai Agent")

# 2. Key Check
if "GROQ_API_KEY" not in st.secrets:
    st.error("❌ GROQ_API_KEY missing from Streamlit Secrets!")
    st.stop()

# 3. Tool Import (The "Safety Net")
try:
    from mytools.calculator import calculator
    from mytools.list_files import list_files
    from mytools.send_email import send_email
    from mytools.file_creation import create_file
    from mytools.profit_loss_tool import profit_loss_excel_tool
    from mytools.read_file import read_file
    from mytools.whatsapp import send_whatsapp_message
    
    tools = [calculator, list_files, send_email, create_file, 
             profit_loss_excel_tool, read_file, send_whatsapp_message]
except Exception as e:
    st.error(f"⚠️ Code Error in your tools: {e}")
    st.info("Check if your files in the 'mytools' folder have any typos.")
    st.stop()

# 4. Agent Initialization
llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=st.secrets["GROQ_API_KEY"])
prompt = hub.pull("hwchase17/openai-functions-agent")
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 5. Chat UI
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if user_input := st.chat_input("Ask Wortex..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)
    
    with st.chat_message("assistant"):
        response = agent_executor.invoke({"input": user_input})
        st.write(response["output"])
        st.session_state.messages.append({"role": "assistant", "content": response["output"]})
