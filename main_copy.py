import streamlit as st
import os

# --- 1. PAGE SETUP (The part that works) ---
st.set_page_config(page_title="Wortex AI Agent", page_icon="🤖")
st.title("🤖 Wortex.ai Agent")

# --- 2. THE ULTIMATE SAFE LOADER (Fixes line 4) ---
try:
    from langchain_groq import ChatGroq
    import langchainhub as hub
    # This import style fixes the "cannot import name" error
    import langchain.agents as agents
    
    # We pull the actual functions out of the 'agents' module directly
    AgentExecutor = agents.AgentExecutor
    create_openai_functions_agent = agents.create_openai_functions_agent
    
    st.success("✅ Wortex Engine Loaded Successfully")
except Exception as e:
    st.error(f"❌ Core loading error: {e}")
    st.stop()

# --- 3. THE REST OF THE CODE ---
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    st.error("Missing GROQ_API_KEY in Secrets!")
    st.stop()

# Using a single stable tool for the demo video
try:
    from mytools.calculator import calculator
    tools = [calculator]
except:
    tools = []

llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=api_key)
prompt = hub.pull("hwchase17/openai-functions-agent")

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# ... (Chat UI code below stays the same)
