from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import BaseMessage,SystemMessage, HumanMessage

load_dotenv()

llm = ChatGoogleGenerativeAI(model = "gemini-3.5-flash-lite")

class ChatState(TypedDict):
    
    messages: Annotated[list[BaseMessage],add_messages]
   

def chat_node(state : ChatState):
    
    messages = state['messages']
    
    response = llm.invoke(messages)
    
    return {'messages' : [response]}

#check pointer 
checkpointer = MemorySaver()

graph = StateGraph(ChatState)

graph.add_node("chat_node",chat_node)
graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)

chatbot = graph.compile(checkpointer = checkpointer)



if __name__ == '__main__':

    thread_id = '1'
    while True:
        
        user_message = input('Typed here: ')
        
        print("User: ",user_message)
        
        if user_message.strip().lower() in ["end","exit","quit","bye"]:
            break
        
        config = {'configurable' : {'thread_id' : thread_id}}
        
        response = chatbot.invoke({'messages': [HumanMessage(content=user_message)]}, config=config)
        
        history = response['messages']
        print("AI: ",response['messages'][-1].content[0]['text'])
        
