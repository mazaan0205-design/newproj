import streamlit as st
import os

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Wortex AI Agent", page_icon="🤖")
st.title("🤖 Wortex.ai Agent")

# --- 2. THE ULTIMATE STABLE IMPORTS ---
try:
    from langchain_groq import ChatGroq
    import langchainhub as hub
    from langchain.agents.agent import AgentExecutor
    from langchain.agents.openai_functions_agent.base import create_openai_functions_agent
    st.success("✅ Wortex Engine Online")
except Exception:
    try:
        from langchain.agents import AgentExecutor, create_openai_functions_agent
        st.success("✅ Wortex Engine Online (Modern Path)")
    except Exception as e:
        st.error(f"❌ Core loading error: {e}")
        st.stop()

# --- 3. LOGIC SETUP ---
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    st.error("Missing GROQ_API_KEY in Secrets!")
    st.stop()

llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=api_key)
prompt = hub.pull("hwchase17/openai-functions-agent")
tools = [] # Start empty for stable video demo

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- 4. CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Ask Wortex..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response = agent_executor.invoke({"input": user_input})
        st.markdown(response["output"])
        st.session_state.messages.append({"role": "assistant", "content": response["output"]})
