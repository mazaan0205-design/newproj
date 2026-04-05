import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain import hub

# 1. Page Configuration
st.set_page_config(page_title="AI Agent Portfolio", page_icon="🤖")
st.title("🤖 My Professional AI Agent")
st.markdown("---")

# 2. Get API Key from Secrets (Fixes the GroqError)
api_key = st.secrets.get("GROQ_API_KEY")

if not api_key:
    st.error("⚠️ GROQ_API_KEY not found in Streamlit Secrets!")
    st.stop()

# 3. Import Your Tools
from mytools.calcuator import calculator
from mytools.list_files import list_files
from mytools.send_email import send_email
from mytools.file_creation import create_file
from mytools.profit_loss_tool import profit_loss_excel_tool
from mytools.read_file import read_file
from mytools.whatsapp import send_whatsapp_message  # Now using Twilio!

tools = [
    calculator, 
    list_files, 
    send_email, 
    create_file, 
    profit_loss_excel_tool, 
    read_file, 
    send_whatsapp_message
]

# 4. Initialize Brain & Agent
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, groq_api_key=api_key)
prompt = hub.pull("hwchase17/openai-functions-agent")
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 5. Session State for Chat History (Web Memory)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. The Chat Input (Replaces your old input() trap)
if user_input := st.chat_input("Ask me to send an email, WhatsApp, or create a file..."):
    # Add user message to state and display
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate Agent Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = agent_executor.invoke({"input": user_input})
                final_response = response["output"]
                st.markdown(final_response)
                st.session_state.messages.append({"role": "assistant", "content": final_response})
            except Exception as e:
                st.error(f"An error occurred: {e}")
