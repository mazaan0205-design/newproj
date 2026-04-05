import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage

# 1. Load the .env file
load_dotenv()

# 2. Grab the key from the .env "container"
api_key = os.getenv("GROQ_API_KEY")

# 3. Import your tools
from mytools.calcuator import calculator
from mytools.list_files import list_files
from mytools.send_email import send_email
from mytools.file_creation import create_file
from mytools.profit_loss_tool import profit_loss_excel_tool
from mytools.whatsapp import send_whatsapp_message
from mytools.read_file import read_file

tools = [calculator, list_files, send_email, create_file, 
         profit_loss_excel_tool, read_file,send_whatsapp_message]

# 4. Initialize LLM (This is where the key is sent to Groq)
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    groq_api_key=api_key
)

memory = InMemorySaver()

# 5. Create Agent
agent = create_agent(llm, tools)

# 6. Chat Loop
config = {"configurable": {"thread_id": "user_1"}}
print("--- Chatbot Started ---")

while True:
    user_input = input("\nUser: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    try:
        for event in agent.stream({"messages": [HumanMessage(content=user_input)]}, config):
            for value in event.values():
                if "messages" in value:
                    print(f"Assistant: {value['messages'][-1].content}")
    except Exception as e:
        print(f"❌ Error: {e}")