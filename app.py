import streamlit as st
import requests
import json
from streamlit_lottie import st_lottie
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space

st.set_page_config(page_title="Chatbot", page_icon="🦙", layout="wide")

def chat(messages):
    request = requests.post(
        "http://0.0.0.0:11434/api/chat",
        json={"model": "llama3", "messages": messages, "stream": True},
        stream=True
    )

    request.raise_for_status()
    output = ""

    for line in request.iter_lines():
        body = json.loads(line)
        if "error" in body:
            raise Exception(body["error"])
        if body.get("done") is False:
            message = body.get("message", "")
            content = message.get("content", "")
            output += content
            yield content

    message = {"role": "assistant", "content": output}
    return message

st.title('🦙 Llama 3 - 8B Bot')
st.write('Interact with llama 3 locally!')

with st.sidebar:
    st.title("🦙 Llama 3 Chatbot")
    st.markdown('''
    ## About
    This chatbot is powered by Llama 3 - 8B model:
    - 🧠 Local AI
    - 💬 Interactive Chat
    - 🚀 Fast Responses
    ''')
    st.markdown("### Made by Nishchal")
    

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How can I help you Nishchal?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in chat(st.session_state.messages):
            full_response += response
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})

if st.button("Clear Chat History"):
    st.session_state.messages = []
