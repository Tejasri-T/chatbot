from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import BaseMessage,SystemMessage, HumanMessage
from openai import BaseModel

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


class NameState(TypedDict):
    messages:list
    past:list
    name:str
    
class NameSchema(BaseModel):
    name: str
    
structured_llm = llm.with_structured_output(NameSchema)
    
    
def name_node(state:NameState):
    
    response = structured_llm.invoke(f"Give a small chat name for the chat based on the conversation: {state['messages']}, other than titles of previous chats : {state['past']}")
    
    return {'name': response.name}

graph1 = StateGraph(NameState)

graph1.add_node("name_node",name_node)
graph1.add_edge(START,"name_node")
graph1.add_edge("name_node",END)

namebot = graph1.compile()



if __name__ == '__main__':

    CONFIG = {'configurable' : {'thread_id' : 'thread_1'}}
    
    # thread_id = '1'
    # while True:
        
    #     user_message = input('Typed here: ')
        
    #     print("User: ",user_message)
        
    #     if user_message.strip().lower() in ["end","exit","quit","bye"]:
    #         break
        
    #     config = {'configurable' : {'thread_id' : thread_id}}
        
    #     response = chatbot.invoke({'messages': [HumanMessage(content=user_message)]}, config=config)
        
    #     history = response['messages']
    #     print("AI: ",response['messages'][-1].content[0]['text'])
        
    respone =chatbot.invoke(
        {"messages": [HumanMessage(content="hey")]},
        config=CONFIG
    )
    
    print(chatbot.get_state(config=CONFIG).values['messages'])