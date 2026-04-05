import streamlit as st
import os

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Wortex AI Agent", page_icon="🤖")
st.title("🤖 Wortex.ai Agent")

# --- 2. THE STABILIZED IMPORTS ---
try:
    from langchain_groq import ChatGroq
    # This is the modern path that prevents the error in image_1192e0.png
    from langchain.agents import AgentExecutor, create_openai_functions_agent
    from langchain import hub
    st.success("✅ Wortex Engine Loaded Successfully")
except Exception as e:
    st.error(f"❌ Core loading error: {e}")
    st.stop()

# --- 3. KEY CHECK ---
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    st.error("❌ GROQ_API_KEY is missing from Secrets!")
    st.stop()

# --- 4. TOOL IMPORTS ---
try:
    from mytools.calculator import calculator
    from mytools.whatsapp import send_whatsapp_message
    tools = [calculator, send_whatsapp_message]
except Exception as e:
    st.warning(f"⚠️ Some tools skipped: {e}")
    tools = []

# --- 5. AGENT INITIALIZATION ---
llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=api_key)
prompt = hub.pull("hwchase17/openai-functions-agent")
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- 6. CHAT UI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if user_input := st.chat_input("How can Wortex help?"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)
    
    with st.chat_message("assistant"):
        try:
            response = agent_executor.invoke({"input": user_input})
            st.write(response["output"])
            st.session_state.messages.append({"role": "assistant", "content": response["output"]})
        except Exception as e:
            st.error(f"Execution Error: {e}")
