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
users = db["users"]   # one document per user


def get_user_doc(username):
    user = users.find_one({"username": username})
    if not user:
        users.insert_one({
            "username": username,
            "conversation": [],
            "createdAt": datetime.utcnow()
        })
        user = users.find_one({"username": username})
    return user

def save_chat_pair(username, user_msg, bot_msg):
    users.update_one(
        {"username": username},
        {
            "$push": {
                "conversation": {
                    "user": user_msg,
                    "bot": bot_msg
                }
            },
            "$set": {"updatedAt": datetime.utcnow()}
        }
    )


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
    st.markdown("## 👋 Welcome to SHAWARMAA")
    name = st.text_input("Enter your name")

    if st.button("Start Chat") and name.strip():
        st.session_state.username = name.strip()
        get_user_doc(st.session_state.username)
        st.session_state.conversation = []
        st.rerun()

    st.stop()

username = st.session_state.username
user_doc = get_user_doc(username)


with st.sidebar:
    st.markdown("## 🥙 SHAWARMAA")
    st.markdown(f"👤 **{username}**")
    st.divider()

    if st.button("Clear Chat"):
        users.update_one(
            {"username": username},
            {"$set": {"conversation": []}}
        )
        st.session_state.conversation = []
        st.rerun()


st.session_state.conversation = []

for pair in user_doc["conversation"]:
    st.session_state.conversation.append(
        {"role": "user", "content": pair["user"]}
    )
    st.session_state.conversation.append(
        {"role": "assistant", "content": pair["bot"]}
    )


st.markdown('<h1 class="header">🥙 SHAWARMAA</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="sub">Hello {username} </p>', unsafe_allow_html=True)

st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for msg in st.session_state.conversation:
    if msg["role"] == "user":
        st.markdown(
            f'<div class="msg-row user-row"><div class="user-msg">{msg["content"]}</div></div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="msg-row bot-row"><div class="bot-msg">{msg["content"]}</div></div>',
            unsafe_allow_html=True
        )

st.markdown('</div>', unsafe_allow_html=True)


user_input = st.chat_input("Type your message...")

if user_input:
    temp_convo = st.session_state.conversation + [
        {"role": "user", "content": user_input}
    ]

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=temp_convo,
        temperature=0.7,
        max_tokens=200
    )

    bot_reply = response.choices[0].message.content

    save_chat_pair(username, user_input, bot_reply)
    st.rerun()
