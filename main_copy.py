import streamlit as st
import os

# --- 1. BASIC UI (This worked in image_102a65.png) ---
st.set_page_config(page_title="Wortex AI Agent", page_icon="🤖")
st.title("🤖 Wortex.ai Agent")

# --- 2. TRY STABLE IMPORTS ---
try:
    from langchain_groq import ChatGroq
    from langchain.agents import AgentExecutor, create_openai_functions_agent
    from langchain import hub
    st.success("✅ Engine components loaded.")
except Exception as e:
    st.error(f"❌ Core loading error: {e}")
    st.stop()

# --- 3. SECRETS CHECK ---
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    st.error("❌ Missing GROQ_API_KEY in Streamlit Secrets!")
    st.stop()

# --- 4. SIMPLE TOOL IMPORTS ---
try:
    # Adding just the essential tools for now to keep it stable
    from mytools.calculator import calculator
    from mytools.whatsapp import send_whatsapp_message
    
    tools = [calculator, send_whatsapp_message]
except Exception as e:
    st.warning(f"⚠️ Some tools failed to load: {e}")
    tools = [] # Continue without tools if they crash

# --- 5. INITIALIZE ---
llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=api_key)
prompt = hub.pull("hwchase17/openai-functions-agent")
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- 6. CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if user_input := st.chat_input("How can I help?"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)
    
    with st.chat_message("assistant"):
        response = agent_executor.invoke({"input": user_input})
        st.write(response["output"])
        st.session_state.messages.append({"role": "assistant", "content": response["output"]})
