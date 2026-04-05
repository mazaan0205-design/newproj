import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain import hub

# 1. PAGE SETUP
st.set_page_config(page_title="Wortex AI Agent", page_icon="🤖")
st.title("🤖 Wortex.ai Agent")

# 2. THE KEY CHECK
# This ensures the app doesn't crash if your Secrets are missing
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    st.error("❌ GROQ_API_KEY is missing from Streamlit Secrets!")
    st.stop()

# 3. IMPORT YOUR TOOLS
# We use a try-except block so you can see exactly which tool file has a mistake
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
    st.info("Check the 'mytools' folder on GitHub for typos in your filenames.")
    st.stop()

# 4. INITIALIZE THE BRAIN (LLM)
llm = ChatGroq(
    model="llama-3.3-70b-versatile", 
    temperature=0, 
    groq_api_key=api_key
)

# 5. INITIALIZE THE AGENT
# Pull the modern 'tools-agent' prompt from LangChain Hub
try:
    prompt = hub.pull("hwchase17/openai-tools-agent")
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    st.success("✅ Wortex Engine Online (Python 3.12)")
except Exception as e:
    st.error(f"❌ Agent Setup Error: {e}")
    st.stop()

# 6. CHAT HISTORY (MEMORY)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. USER INPUT & EXECUTION
if user_input := st.chat_input("How can Wortex help you today?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response using the Agent
    with st.chat_message("assistant"):
        with st.spinner("Wortex is thinking..."):
            try:
                # The agent decides which tool to use and gives the answer
                response = agent_executor.invoke({"input": user_input})
                final_answer = response["output"]
                st.markdown(final_answer)
                st.session_state.messages.append({"role": "assistant", "content": final_answer})
            except Exception as e:
                st.error(f"Agent Execution Error: {e}")
