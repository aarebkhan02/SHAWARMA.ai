import streamlit as st
from groq import Groq
import os


client = Groq(api_key=os.environ["GROQ_API_KEY"])



# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SHAWARMAA",
    page_icon="🥙",
    layout="centered"
)




# ---------------- CSS ----------------
st.markdown("""
<style>
body {
    background-color: #0e0e0e;
}

.chat-container {
    display: flex;
    flex-direction: column;
    gap: 14px;
    padding-bottom: 20px;
}

.msg-row {
    width: 100%;
    display: flex;
}

.user-row {
    justify-content: flex-end;
}

.bot-row {
    justify-content: flex-start;
}

.user-msg {
    background-color: #85409D;
    color: white;
    padding: 14px 18px;
    border-radius: 18px 18px 4px 18px;
    max-width: 72%;
    font-size: 15px;
    line-height: 1.4;
    word-wrap: break-word;
}

.bot-msg {
    background-color: #878787;
    color: white;
    padding: 14px 18px;
    border-radius: 18px 18px 18px 4px;
    max-width: 72%;
    font-size: 15px;
    line-height: 1.4;
    word-wrap: break-word;
}

.header {
    text-align: center;
    color: #92487A;
    margin-bottom: 4px;
}

.sub {
    text-align: center;
    color: #aaa;
    margin-bottom: 25px;
}
</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("## 🥙 SHAWARMAA")
    st.markdown("Friendly AI chatbot")
    st.divider()
    if st.button("Clear Chat"):
        st.session_state.conversation = [
            {"role": "system", "content": "you are a firendly AI assistant"}
        ]
        st.rerun()

# SESSION STATE
if "conversation" not in st.session_state:
    st.session_state.conversation = [
        {"role": "system", "content": "you are a firendly AI assistant"}
    ]

# HEADER
st.markdown('<h1 class="header">🥙 SHAWARMA</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub">Your friendly AI assistant</p>', unsafe_allow_html=True)

# CHAT
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for msg in st.session_state.conversation:
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div class="msg-row user-row">
                <div class="user-msg">{msg["content"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    elif msg["role"] == "assistant":
        st.markdown(
            f"""
            <div class="msg-row bot-row">
                <div class="bot-msg">{msg["content"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- INPUT ----------------
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.conversation.append(
        {"role": "user", "content": user_input}
    )

    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=st.session_state.conversation,
        temperature=0.7,
        max_tokens=200
    )

    assistant_reply = res.choices[0].message.content

    st.session_state.conversation.append(
        {"role": "assistant", "content": assistant_reply}
    )

    st.rerun()
