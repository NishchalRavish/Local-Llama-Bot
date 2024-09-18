import streamlit as st
import requests
import json

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

st.title('llama 3 - 8B Bot')
st.write('Interact with llama 3 locally!')

if "messages" not in st.session_state:
    st.session_state.messages = []

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









# if "messages" not in st.session_state:
#     st.session_state.messages = []
    
# def get_bot_response(user_message):
#     url = "http://localhost:11434/chat"
#     headers = {"Content-Type": "application/json"}
#     payload = {
#         "model": "llama3",
#         "prompt": user_message
#     }
    
#     response = requests.post(url, json=payload, headers=headers)
    
#     if response.status_code == 200:
#         return response.json().get("response")
#     else:
#         return "Error: Unable to Connect to Bot"

# for message in st.session_state.messages:
#     if message['role'] == "user":
#         st.markdown(f"**You:** {message['content']}")
#     else:
#         st.markdown(f"**Bot:** {message['content']}")

# user_input = st.text_input("You", key="user_input")

# if st.button("Send") and user_input:
#     st.session_state.messages.append({"role":"user","content":user_input})
#     response = get_bot_response(user_input)
#     st.session_state.messages.append({"role":"bot","content":response})
#     st.write(st.session_state)
    
#     st.session_state.user_input=""