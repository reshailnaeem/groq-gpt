import os
import urllib.parse
from typing import Generator

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# Function to generate responses
def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# Function to clear chat history
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

st.set_page_config(
    page_title="Assistant",
    page_icon="🤖🧠💬",
)

st.subheader('💬 GroqGPT')

# Sidebar settings
with st.sidebar:
    st.title('💬 GroqGPT')
    st.caption('🤖🧠💬')
    st.subheader('Parameters')
    temperature = st.slider('temperature', min_value=0.01, max_value=1.0, value=0.6, step=0.01)
    top_p = st.slider('top_p', min_value=0.01, max_value=1.0, value=0.8, step=0.01)
    max_tokens = st.slider('max_tokens', min_value=700, max_value=7000, value=3500, step=50)

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
  
st.sidebar.button('Clear chat history', on_click=clear_chat_history)

if prompt := st.chat_input("Enter your prompt here..."):

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user", avatar='👨‍💻'):
        st.markdown(prompt)

    # Display assistant response in chat message container
    try:
        chat_completion = client.chat.completions.create(
            model='gemma2-9b-it',
            messages=[
                # System prompt
                {
                    "role": "system",
                    "content": "You are an advanced and versatile chatbot with extensive knowledge across a wide range of topics. Your primary objectives are to provide accurate and relevant information, assist with problem-solving, and engage users in meaningful and contextually appropriate conversations. Admit when you don't know something."
                },
                # Human input
                *[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
                ]
            ],
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            stream=True
        )
        # Use the generator function with st.write_stream
        with st.chat_message("assistant", avatar="🤖"):
            chat_responses_generator = generate_chat_responses(chat_completion)
            full_response = st.write_stream(chat_responses_generator)
    except Exception as e:
        st.error(e, icon="🚨")

    # Append the full response to session_state.messages
    if isinstance(full_response, str):
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response})
    else:
        # Handle the case where full_response is not a string
        combined_response = "\n".join(str(item) for item in full_response)
        st.session_state.messages.append(
            {"role": "assistant", "content": combined_response})
        
# Button to save chat history
if st.sidebar.button('Save chat history'):
    chat_history = st.session_state.messages
    chat_history_text = '\n'.join([f"{m['role']}: {m['content']}" for m in chat_history])
    st.markdown(
        f'<a href="data:text/plain;charset=utf-8,{urllib.parse.quote(chat_history_text)}" download="chat_history.txt">Download chat history</a>',
        unsafe_allow_html=True
    )