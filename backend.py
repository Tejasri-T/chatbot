
from concurrent.futures import thread
from os import name

from langgraph.graph import StateGraph,START,END
from typing import Literal, TypedDict,Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import BaseMessage,SystemMessage, HumanMessage
from openai import BaseModel
import sqlite3

load_dotenv()

llm = ChatGoogleGenerativeAI(model = "gemini-3.5-flash-lite")

class ChatState(TypedDict):
    
    messages: Annotated[list[BaseMessage],add_messages]
    # name:str
 

#--------------Name Bot------------------------

class NameState(TypedDict):
    messages:list
    name:str
   
class NameSchema(BaseModel):
    name: str
    
structured_llm = llm.with_structured_output(NameSchema)
    
def name_node(state:NameState,config):
    
    cursor.execute("""
            SELECT thread_id, chat_name
            FROM chat_threads
        """)
    past_names = [row[0] for row in cursor.fetchall()]
    
    response = structured_llm.invoke(f"Give a small chat name for the chat based on the conversation: {state['messages']}, other than titles of previous chats : {past_names}")
    
    chat_name = response.name
    thread_id = config["configurable"]["thread_id"]
    
    cursor.execute("""
        INSERT OR REPLACE INTO chat_threads
        (thread_id, chat_name)
        VALUES (?, ?)
    """, (str(thread_id), chat_name))

    conn.commit()
    
    return {"name":chat_name}


#------------------------chatbot----------------------------

def chat_node(state : ChatState):
    
    messages = state['messages']
    
    
    response = llm.invoke(messages)
    
    return {'messages' : [response]}

# def name_condition(state: ChatState)->Literal['name_node','chat_node']:
    
#     if len(state['messages'])<3:
#         return 'name_node'
#     else:
#         return 'chat_node'


#----------Database connection-------------
conn = sqlite3.connect(database='chatbot.db',check_same_thread=False)

# Create naming database
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_threads (
        thread_id TEXT PRIMARY KEY,
        chat_name TEXT
    )
""")

conn.commit()



#------------check pointer--------------------
# checkpointer = MemorySaver()
checkpointer = SqliteSaver(conn = conn)

graph = StateGraph(ChatState)

graph.add_node("chat_node",chat_node)

graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)

chatbot = graph.compile(checkpointer = checkpointer)

#-------namebot---------------------
name_checkpointer = MemorySaver()
name_graph = StateGraph(NameState)

name_graph.add_node("name_node",name_node)

name_graph.add_edge(START,"name_node")
name_graph.add_edge("name_node",END)

namebot = name_graph.compile(checkpointer = name_checkpointer)





def retrieve_all_threads():
    
    all_threads = {
        checkpoint.config['configurable']['thread_id']
        for checkpoint in checkpointer.list(None)
    }

    if not all_threads:
        return {}

    placeholders = ",".join("?" for _ in all_threads)

    cursor.execute(
        f"""
        SELECT thread_id, chat_name
        FROM chat_threads
        WHERE thread_id IN ({placeholders})
        """,
        tuple(all_threads)
    )

    return dict(cursor.fetchall())

def get_name(thread_id):
    
    cursor.execute("""
        SELECT chat_name
        FROM chat_threads
        WHERE thread_id = ?
    """, (thread_id,))

    result = cursor.fetchone()
    # print(result)
    return result[0] if result else None


if __name__ == '__main__':

    CONFIG = {'configurable' : {'thread_id' : 'thread_4'}}
    
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
        
    # response =chatbot.invoke(
    #     {"messages": [HumanMessage(content="Hey, did i greet you?")]},
    #     config=CONFIG
    # )
    # response = namebot.invoke(
    #             {"messages":"Hey add some random numbers"},
    #             config=CONFIG
    #             )
    response = retrieve_all_threads()
    print(response)
    