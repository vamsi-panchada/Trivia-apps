import streamlit as st
import datetime as dt
from openai import OpenAI

st.title("📖 Hindu Sanatana Dharma Trivia in Telugu 🇮🇳")

if "api_key" not in st.session_state:
    st.session_state.api_key = None

api_key = st.text_input("Enter your OpenAI API Key", type="password")

if api_key:
    st.session_state.api_key = api_key
    st.success("API Key loaded successfully! You can start the quiz now. 🎉")
else:
    st.warning("Please enter your OpenAI API key to continue.")
    st.stop()

system_prompt = f"""You are a knowledgeable expert in Hindu Sanatana Dharma, including the Bhagavad Gita, Ramayana, Mahabharata, Vedas, Puranas, and other Hindu scriptures. Your task is to conduct an engaging and interactive trivia session in pure Telugu for a participant named Kumari.  

Follow these guidelines:  
- Ask one question at a time in a friendly and conversational manner.
- Provide options to the relevant question as well  
- Ensure the questions are thought-provoking yet suitable for Kumari's level of understanding.  
- Provide insightful explanations after each answer to enhance learning.  
- Maintain a respectful and warm tone, encouraging curiosity and discussion.  
- Ensure accuracy and authenticity while referencing Hindu scriptures.  

Today's date: {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"""

def gen_text(messages):
    client = OpenAI(api_key=st.session_state.api_key)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.2,
        top_p=0.7,
        max_tokens=1024,
        stream=True
    )
    return completion


if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
    
    initial_placeholder = st.empty()
    initial_response = ""
    for chunk in gen_text(st.session_state.messages):
        if chunk.choices[0].delta.content:
            initial_response += chunk.choices[0].delta.content
            # initial_placeholder.markdown(initial_response + "▌")
    # initial_placeholder.markdown(initial_response)

    st.session_state.messages.append({"role": "assistant", "content": initial_response})

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Hi Kumari!"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for chunk in gen_text(st.session_state.messages):
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})