import streamlit as st
import os
import sqlite3 # Standard for simple DB
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
try:
    from langchain_groq import ChatGroq
    from langchain import hub
    from langchain.agents import AgentExecutor, create_tool_calling_agent
    # Added for Memory management
    from langchain_community.chat_message_histories import SQLChatMessageHistory
    st.success("✅ Wortex Engine Online")
except Exception as e:
    st.error(f"❌ Connection Error: {e}")
    st.stop()

# --- 3. LOGIC SETUP ---
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    api_key = os.getenv("GROQ_API_KEY") # Fallback for local testing
    if not api_key:
        st.error("Missing GROQ_API_KEY!")
        st.stop()

llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=api_key)

tools = [
    send_email,
    send_whatsapp_message,
    read_file,
    list_files,
    create_file,
    profit_loss_excel_tool,
    calculator
]

# Pull the prompt
prompt = hub.pull("hwchase17/openai-tools-agent")

# Create the specific Tool Calling Agent
agent = create_tool_calling_agent(llm, tools, prompt)

# Create the executor
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True, 
    handle_parsing_errors=True,
    max_iterations=10
)

# --- 4. MEMORY & CHAT INTERFACE ---
# Use a session ID to keep users separate in the database
session_id = "user_default" # You can replace this with Google Login ID later

# Initialize SQLite Memory
message_history = SQLChatMessageHistory(
    session_id=session_id, connection_string="sqlite:///wortex_memory.db"
)

# Display previous conversation from Session State
if "messages" not in st.session_state:
    # Load from database if session state is empty
    st.session_state.messages = []
    for msg in message_history.messages:
        role = "user" if msg.type == "human" else "assistant"
        st.session_state.messages.append({"role": role, "content": msg.content})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle User Input
if user_input := st.chat_input("Ask Wortex..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Agent Response Logic
    with st.chat_message("assistant"):
        try:
            with st.spinner("Wortex is thinking..."):
                # Pass the chat_history into the invoke call
                response = agent_executor.invoke({
                    "input": user_input,
                    "chat_history": message_history.messages # This feeds the DB memory to the AI
                })
                
                final_answer = response["output"]
                st.markdown(final_answer)
                
                # Save both to Session State (for display) and Database (for persistence)
                st.session_state.messages.append({"role": "assistant", "content": final_answer})
                message_history.add_user_message(user_input)
                message_history.add_ai_message(final_answer)
                
        except Exception as e:
            error_msg = f"❌ Agent Error: {str(e)}"
            st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
