import streamlit as st
from model.llama_model import LlamaQA
from utils.bot_utils import clean_question

bot_model = LlamaQA()

if 'conversation' not in st.session_state:
    st.session_state.conversation = []

st.title('Llama Chat Bot')
st.write("What's on your mind Nishchal?")

question = st.text_input("Enter question")

if st.button("Send"):
    if question:
        clean_up_question  = clean_question(question)
        
        st.session_state.conversation.append(f"Nishchal: {clean_q}")

        conversation_history = "\n".join(st.session_state.conversation)

        answer = bot_model.get_answer(conversation_history)
        
        st.session_state.conversation.append(f"Bot: {answer}")
        
        st.write('$$$Conversation$$$')
        for line in st.session_state.conversation:
            st.write(line)
    else:
        st.write("Enter question")