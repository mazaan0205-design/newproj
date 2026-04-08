import streamlit as st
import os

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Wortex AI Agent", page_icon="🤖")
st.title("🤖 Wortex.ai Agent")

# --- THE EMERGENCY STABLE LOADER ---
try:
    from langchain_groq import ChatGroq
    import langchainhub as hub
    
    # We load from the base 'agent' file directly to avoid the init.py error
    import langchain.agents.agent as agent_base
    import langchain.agents.openai_functions_agent.base as func_agent_base
    
    AgentExecutor = agent_base.AgentExecutor
    create_openai_functions_agent = func_agent_base.create_openai_functions_agent
    
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
