import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain import hub

# 1. PAGE SETUP
st.set_page_config(page_title="Wortex AI Agent", page_icon="🤖")
st.title("🤖 Wortex.ai Agent")

# 2. THE DEBUG CHECK (ADD THIS AT THE TOP)
if "GROQ_API_KEY" in st.secrets:
    st.success("✅ Secrets are loaded correctly!")
    api_key = st.secrets["GROQ_API_KEY"]
else:
    st.error("❌ Secrets are EMPTY! Please go to Settings > Secrets and add GROQ_API_KEY.")
    st.info("Make sure the name in Secrets is exactly: GROQ_API_KEY")
    st.stop() # This stops the app here so you don't get a confusing crash later

# 3. IMPORT YOUR TOOLS
# (Make sure these files exist in your 'mytools' folder on GitHub)
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
except ImportError as e:
    st.error(f"Error importing tools: {e}")
    st.stop()

# 4. INITIALIZE BRAIN & AGENT
llm = ChatGroq(
    model="llama-3.3-70b-versatile", 
    temperature=0, 
    groq_api_key=api_key
)

# Pull the prompt from LangChain Hub
prompt = hub.pull("hwchase17/openai-functions-agent")

# Create the agent
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 5. CHAT HISTORY (MEMORY)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. USER INPUT (The chat bar)
if user_input := st.chat_input("Ask me anything..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Agent is working..."):
            try:
                response = agent_executor.invoke({"input": user_input})
                final_answer = response["output"]
                st.markdown(final_answer)
                st.session_state.messages.append({"role": "assistant", "content": final_answer})
            except Exception as e:
                st.error(f"Agent Error: {e}")
