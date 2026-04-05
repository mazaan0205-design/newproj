import streamlit as st
import os

# 1. Page Configuration
st.set_page_config(page_title="Wortex AI", page_icon="🤖")
st.title("🤖 Wortex.ai Agent")

# 2. Key Check
if "GROQ_API_KEY" not in st.secrets:
    st.error("❌ GROQ_API_KEY missing from Secrets!")
    st.stop()

# 3. Stable Imports (This fixes the 'Traceback' error)
try:
    from langchain_groq import ChatGroq
    from langchain.agents import AgentExecutor, create_openai_functions_agent
    from langchain import hub
    
    # Import your specific tools
    from mytools.whatsapp import send_whatsapp_message
    from mytools.calculator import calculator
    # ... import your other tools here ...

    tools = [send_whatsapp_message, calculator] # Add all your tools to this list

    # 4. Initialize the Agent
    llm = ChatGroq(
        model="llama-3.3-70b-versatile", 
        groq_api_key=st.secrets["GROQ_API_KEY"]
    )
    prompt = hub.pull("hwchase17/openai-functions-agent")
    agent = create_openai_functions_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    st.success("✅ Wortex Engine Online")

except Exception as e:
    st.error(f"⚠️ System Error: {e}")
    st.info("Check your requirements.txt versions.")
    st.stop()

# 5. Simple Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if user_input := st.chat_input("How can Wortex help you today?"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)
    
    with st.chat_message("assistant"):
        response = agent_executor.invoke({"input": user_input})
        st.write(response["output"])
        st.session_state.messages.append({"role": "assistant", "content": response["output"]})
