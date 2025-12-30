import streamlit as st
from groq import Groq
from pymongo import MongoClient
from datetime import datetime


st.set_page_config(
    page_title="SHAWARMAA",
    page_icon="🥙",
    layout="centered"
)


groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])


mongo_client = MongoClient(st.secrets["MONGODB_URL"])
db = mongo_client["shawarma_db"]
chats = db["chats"]


def save_message(username, role, content):
    chats.insert_one({
        "username": username,
        "role": role,
        "content": content,
        "timestamp": datetime.utcnow()
    })

def load_messages(username):
    return list(
        chats.find({"username": username}).sort("timestamp", 1)
    )

# ---------------- CSS ----------------
st.markdown("""
<style>
body { background-color: #0e0e0e; }

.chat-container {
    display: flex;
    flex-direction: column;
    gap: 14px;
    padding-bottom: 20px;
}

.msg-row { display: flex; width: 100%; }

.user-row { justify-content: flex-end; }
.bot-row { justify-content: flex-start; }

.user-msg {
    background-color: #85409D;
    color: white;
    padding: 14px 18px;
    border-radius: 18px 18px 4px 18px;
    max-width: 72%;
}

.bot-msg {
    background-color: #878787;
    color: white;
    padding: 14px 18px;
    border-radius: 18px 18px 18px 4px;
    max-width: 72%;
}

.header { text-align: center; color: #92487A; }
.sub { text-align: center; color: #aaa; }
</style>
""", unsafe_allow_html=True)


if "username" not in st.session_state:
    st.markdown("##  Welcome to SHAWARMAA")
    name = st.text_input("Enter your name to continue")

    if st.button("Start Chat") and name.strip():
        st.session_state.username = name.strip()
        st.session_state.conversation = [
            {
                "role": "system",
                "content": (
                    f"You are an AI chatbot named Shawarma. "
                    f"The user's name is {st.session_state.username}. "
                    "You are friendly, helpful, and casual. "
                    "If asked who made you, reply exactly: Aareb made me."
                )
            }
        ]
        st.rerun()

    st.stop()


with st.sidebar:
    st.markdown(f"## 🥙 SHAWARMAA")
    st.markdown(f" User: **{st.session_state.username}**")
    st.divider()

    if st.button("Clear Chat"):
        chats.delete_many({"username": st.session_state.username})
        st.session_state.conversation = [
            {
                "role": "system",
                "content": (
                    f"You are an AI chatbot named Shawarma. "
                    f"The user's name is {st.session_state.username}. "
                    "You are friendly, helpful, and casual. "
                    "If asked who made you, reply exactly: Aareb made me."
                )
            }
        ]
        st.rerun()


if "conversation" not in st.session_state:
    saved = load_messages(st.session_state.username)
    if saved:
        st.session_state.conversation = [
            {"role": m["role"], "content": m["content"]} for m in saved
        ]
    else:
        st.session_state.conversation = [
            {
                "role": "system",
                "content": (
                    f"You are an AI chatbot named Shawarma. "
                    f"The user's name is {st.session_state.username}. "
                    "You are friendly, helpful, and casual with a desi tone. "
                    "If asked who made you, reply exactly: Aareb made me."
                )
            }
        ]


st.markdown('<h1 class="header">🥙 SHAWARMAA</h1>', unsafe_allow_html=True)
st.markdown(
    f'<p class="sub">Hello {st.session_state.username} </p>',
    unsafe_allow_html=True
)

st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for msg in st.session_state.conversation:
    if msg["role"] == "user":
        st.markdown(
            f'<div class="msg-row user-row"><div class="user-msg">{msg["content"]}</div></div>',
            unsafe_allow_html=True
        )
    elif msg["role"] == "assistant":
        st.markdown(
            f'<div class="msg-row bot-row"><div class="bot-msg">{msg["content"]}</div></div>',
            unsafe_allow_html=True
        )

st.markdown('</div>', unsafe_allow_html=True)


user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.conversation.append(
        {"role": "user", "content": user_input}
    )
    save_message(st.session_state.username, "user", user_input)

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=st.session_state.conversation,
        temperature=0.7,
        max_tokens=200
    )

    assistant_reply = response.choices[0].message.content

    st.session_state.conversation.append(
        {"role": "assistant", "content": assistant_reply}
    )
    save_message(st.session_state.username, "assistant", assistant_reply)

    st.rerun()
