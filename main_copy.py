import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_openai_functions_agent

# THIS IS THE FIX FOR THE ERROR IN IMAGE_EA1AE2.PNG
import langchainhub as hub 

# --- PAGE SETUP ---
st.set_page_config(page_title="Wortex AI Agent", page_icon="🤖")
st.title("🤖 Wortex.ai Agent")

# --- REST OF YOUR CODE ---
try:
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
    else:
        st.error("Missing GROQ_API_KEY")
        st.stop()

    llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=api_key)
    
    # This will now work because of 'import langchainhub as hub'
    prompt = hub.pull("hwchase17/openai-functions-agent")
    
    # COMMENT OUT the WhatsApp tool for the demo to avoid extra errors
    # from mytools.whatsapp import send_whatsapp_message
    from mytools.calculator import calculator
    
    tools = [calculator] # Add other tools only if they are working locally
    
    agent = create_openai_functions_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    st.success("✅ Wortex Engine Loaded")

except Exception as e:
    st.error(f"Core loading error: {e}")
