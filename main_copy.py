import streamlit as st
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="Wortex AI Agent", page_icon="🤖")
st.title("🤖 Wortex.ai Agent")

# --- THE FIX FOR 'NO ATTRIBUTE' ERROR ---
try:
    from langchain_groq import ChatGroq
    import langchainhub as hub
    
    # We use these specific paths to bypass the error in image_ea2623.png
    from langchain.agents import AgentExecutor
    from langchain.agents import create_openai_functions_agent
    
    st.success("✅ Wortex Engine Online")
except Exception as e:
    st.error(f"❌ Core loading error: {e}")
    st.stop()

# --- THE REST OF YOUR LOGIC ---
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    st.error("Missing GROQ_API_KEY in Secrets!")
    st.stop()

llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=api_key)
prompt = hub.pull("hwchase17/openai-functions-agent")

# Starting with no tools to ensure the UI loads first
tools = [] 

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# ... (Insert your Chat UI code here)
