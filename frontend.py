from huggingface_hub import metadata_eval_result, metadata_save
import streamlit as st 
from backend import chatbot
from langchain_core.messages import HumanMessage

CONFIG = {'configurable' : {'thread_id' : 'thread_1'}}


if 'message_hist' not in st.session_state:
    st.session_state['message_hist'] = []
    
messages = st.session_state['message_hist']

for message in st.session_state['message_hist']:
    with st.chat_message(message['role']):
        st.write(message['content'])
        

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
    with st.chat_message("assistant"):
        ai_message = st.write_stream(
            mesg.content[0]['text'] if mesg.content else "" for mesg, metadata in chatbot.stream(
            {'messages': [HumanMessage(content=user_message)]}, 
            stream_mode="messages",
            config=CONFIG
            )
        )
    messages.append({'role':'assistant','content':ai_message})  
        
        
