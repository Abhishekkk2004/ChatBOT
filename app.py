import streamlit as st
from langchain_ollama import ChatOllama

from langchain_ollama import ChatOllama

from langchain_core.prompts import (
                                        SystemMessagePromptTemplate,
                                        HumanMessagePromptTemplate,
                                        ChatPromptTemplate,
                                        MessagesPlaceholder
                                        )


from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory

from langchain_core.output_parsers import StrOutputParser

st.title("A Local ChatBOT Prototype")
st.write("A project by Abhishek Saha from the learnings made from KGPTakie")

with st.sidebar:
    st.title("A Local ChatBOT Prototype")
    st.write("A project by Abhishek Saha from the learnings made from KGPTakie")

# History Box set-up

def historyBox(session_id):
    return SQLChatMessageHistory(session_id, "sqlite:///chat_history.db")


#Configuring the history part

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

 
#According to roles create a history page, different bubbles for different roles of AI and human

for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

#LLM Set-up

base_url = "http://localhost:11434"
model = 'llama3.2:1b'
llm = ChatOllama(base_url=base_url, model=model)

#Prompt making set-up

system = SystemMessagePromptTemplate.from_template("You are helpful assistant.")
human = HumanMessagePromptTemplate.from_template("{input}")

messages = [system, MessagesPlaceholder(variable_name='history'), human]

prompt = ChatPromptTemplate(messages)

chain = prompt | llm | StrOutputParser()


#Configuring the history chain

runnable_with_history = RunnableWithMessageHistory(chain, historyBox, 
                                                   input_messages_key='input', 
                                                   history_messages_key='history')

def chat_with_llm(session_id, input):
    for output in runnable_with_history.stream({'input': input}, config={'configurable': {'session_id': session_id}}):
        yield output




user_id = st.text_input("Enter your user id", "abhishek")

#Configuring the new conversation part


if st.button("Start New Conversation"):
    st.session_state.chat_history = []
    history = historyBox(user_id) #corresponding to that user-id gets removed
    history.clear()



 

# Recieving Prompt from user 


prompt = st.chat_input("What is up?")

#Configuring the part after recieving the prompt


if prompt:
    st.session_state.chat_history.append({'role': 'user', 'content': prompt})

#Displaying for immediate prompt

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.write_stream(chat_with_llm(user_id, prompt))

    st.session_state.chat_history.append({'role': 'assistant', 'content': response})


# with st.form("llm-form"):
#     text = st.text_area("Enter your question or statement:")
#     submit = st.form_submit_button("Submit")

# def generate_response(input_text):
#     model = ChatOllama(model="llama3.2:1b", base_url="http://localhost:11434/")

#     response = model.invoke(input_text)

#     return response.content

# if "chat_history" not in st.session_state:
#     st.session_state['chat_history'] = []

# if submit and text:
#     with st.spinner("Generating response..."):
#         response = generate_response(text)
#         st.session_state['chat_history'].append({"user": text, "ollama": response})
#         st.write(response)

# st.write("## Chat History")
# for chat in reversed(st.session_state['chat_history']):
#     st.write(f"**🧑 User**: {chat['user']}")
#     st.write(f"**🧠 Assistant**: {chat['ollama']}")
#     st.write("---")