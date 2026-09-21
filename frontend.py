
import streamlit as st 
from backend import chatbot,namebot
from langchain_core.messages import HumanMessage
import uuid




#---------------------utility functions-------------------------

def generate_thread_id():
    thread_id = uuid.uuid4()
    # st.session_state['chats'][thread_id] = st.session_state['count']
    # st.session_state['count']+=1
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id 
    add_thread(st.session_state['thread_id'])
    st.session_state['message_hist'] = []

def add_thread(thread_id):
    if thread_id not in  st.session_state['chat_threads']:
        st.session_state['chat_threads'][thread_id] = f'new chat {len(st.session_state['chat_threads'])+1}'
        
def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable' : {'thread_id' : thread_id}}).values
    if state:
        messages = state['messages']
    else:
        messages = []
    return messages

#-------------Session state --------------------
if 'message_hist' not in st.session_state:
    st.session_state['message_hist'] = []


# if 'count' not in  st.session_state:
#     st.session_state['count'] = 1
if 'thread_id' not in  st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in  st.session_state:
    st.session_state['chat_threads'] = {}



add_thread(st.session_state['thread_id'])

#-------------------Side bar-------------------------

st.sidebar.title('Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()
    

st.sidebar.header('My Conversation')

for thread_id in reversed(st.session_state['chat_threads'].keys()):
    if st.sidebar.button(st.session_state['chat_threads'][thread_id]):
        st.session_state['thread_id'] = thread_id
        loaded_messages = load_conversation(thread_id)

        temp_messages = []
        
        for msg in loaded_messages:
            if isinstance(msg,HumanMessage):
                role = "Human"
                temp_messages.append({'role':role, 'content':msg.content})
            else:
                role = "assistant"
                temp_messages.append({'role':role, 'content':msg.content[0]['text'] if msg.content else ""})
        
        st.session_state['message_hist'] = (temp_messages)
                



#---------------- Messages --------------------------

messages = st.session_state['message_hist']

for message in st.session_state['message_hist']:
    with st.chat_message(message['role']):
        st.write(message['content'])

#---------------- Chat Interface --------------------------


user_message = st.chat_input("Type your message here...")

if user_message:
    
    messages.append({'role':'user','content':user_message})
    with st.chat_message("user"):
        st.write(user_message)
    
    
    
    # response = chatbot.stream(
    #     {'messages': [HumanMessage(content=user_message)]}, 
    #     stream_mode="messages",
    #     config=CONFIG)
    
    
    
    # messages.append({'role':'assistant','content':ai_message})
    CONFIG = {'configurable' : {'thread_id' : st.session_state['thread_id']}}

    f = False
    with st.chat_message("assistant"):
        if 'new chat' in st.session_state['chat_threads'][st.session_state['thread_id']] and len(st.session_state['message_hist'])<3:
            res = namebot.invoke({'messages':messages,"past":list(st.session_state['chat_threads'].values())})
            st.session_state['chat_threads'][st.session_state['thread_id']] = res['name'] 
            # st.sidebar.write("rerunning")
            f = True
        ai_message = st.write_stream(
            mesg.content[0]['text'] if mesg.content else "" for mesg, metadata in chatbot.stream(
            {'messages': [HumanMessage(content=user_message)]}, 
            stream_mode="messages",
            config=CONFIG
            )
        )
    messages.append({'role':'assistant','content':ai_message})
    
    if f:
        st.rerun()
    
# st.sidebar.write('new chat' in st.session_state['chat_threads'][st.session_state['thread_id']] , len(st.session_state['message_hist'])<3)   
    
        
        
