import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPTS

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))




st.title("💬 Gemini Conversational LLM")
st.write("Chat with AI in different modes: Professional, Creative, or Technical.")
st.divider()

mode = st.sidebar.radio("Choose Assistant Mode:", list(SYSTEM_PROMPTS.keys()))
system_prompt = SYSTEM_PROMPTS[mode]
st.subheader("Conversation")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat = genai.GenerativeModel("gemini-1.5-flash").start_chat(
        history=[{"role": "user", "parts": [system_prompt]}]
    )
if "current_mode" not in st.session_state:
    st.session_state.current_mode = mode

if st.session_state.current_mode != mode:
    st.session_state.current_mode = mode
    st.session_state.messages.append(
        {"role": "system", "content": f"✅ You selected **{mode}** mode."}
    )

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:

        response = st.session_state.chat.send_message(f"{system_prompt}\nUser: {user_input}")
        reply = response.text

        st.session_state.messages.append({"role": "assistant", "content": reply})

    except Exception as e:
        reply = f"⚠️ Error: {e}"
        st.session_state.messages.append({"role": "assistant", "content": reply})


for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])


if st.sidebar.button("📥 Export Chat"):
    chat_text = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.messages])
    with open("chat_history.txt", "w", encoding="utf-8") as f:
        f.write(chat_text)
    st.sidebar.success("Chat exported as chat_history.txt ✅")
