import streamlit as st
import os
from mytools.send_email import send_email
from mytools.whatsapp import send_whatsapp_message
from mytools.read_file import read_file
from mytools.list_files import list_files
from mytools.file_creation import create_file
from mytools.profit_loss_tool import profit_loss_excel_tool
from mytools.calcuator import calculator
# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Wortex AI Agent", page_icon="🤖")
st.title("🤖 Wortex.ai Agent")
# --- 2. THE STABLE LOADER ---
# --- 2. THE STABLE LOADER ---
try:
    from langchain_groq import ChatGroq
    from langchain import hub
    from langchain.agents import AgentExecutor, create_openai_functions_agent
  
    st.success("✅ Wortex Engine Online")
except Exception as e:
    st.error(f"❌ Connection Error: {e}")
    st.stop()

# --- 3. LOGIC SETUP ---
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    st.error("Missing GROQ_API_KEY in Secrets!")
    st.stop()

llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=api_key)
prompt = hub.pull("hwchase17/openai-functions-agent")
tools = [
    send_email, 
    send_whatsapp_message, 
    read_file, 
    list_files, 
    create_file, 
    profit_loss_excel_tool,
    calculator
]# Start empty for stable video demo

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- 4. CHAT INTERFACE ---
# --- 4. CHAT INTERFACE (STARTING FROM LINE 48) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Process new user input
if user_input := st.chat_input("Ask Wortex..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        # The agent_executor.invoke is what actually "thinks" and uses tools
        response = agent_executor.invoke({"input": user_input})
        
        # We extract the 'output' string to show it on screen
        final_answer = response["output"]
        st.markdown(final_answer)
        
    # Save the assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": final_answer})
