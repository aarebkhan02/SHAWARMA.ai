import streamlit as st
from groq import Groq
import os
from pymongo import MongoClient


client = Groq(api_key=os.environ["GROQ_API_KEY"])


MONGO_URI = st.secrets["MONGODB_URL"]
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["shawarma_db"]
chats_collection = db["chats"]


st.set_page_config(
    page_title="SHAWARMAA",
    page_icon="🥙",
    layout="centered"
)


st.markdown("""
<style>
body { background-color: #0e0e0e; }
.chat-container { display: flex; flex-direction: column; gap: 14px; padding-bottom: 20px; }
.msg-row { width: 100%; display: flex; }
.user-row { justify-content: flex-end; }
.bot-row { justify-content: flex-start; }
.user-msg { background-color: #85409D; color: white; padding: 14px 18px; border-radius: 18px 18px 4px 18px; max-width: 72%; font-size: 15px; line-height: 1.4; word-wrap: break-word; }
.bot-msg { background-color: #878787; color: white; padding: 14px 18px; border-radius: 18px 18px 18px 4px; max-width: 72%; font-size: 15px; line-height: 1.4; word-wrap: break-word; }
.header { text-align: center; color: #92487A; margin-bottom: 4px; }
.sub { text-align: center; color: #aaa; margin-bottom: 25px; }
</style>
""", unsafe_allow_html=True)


if "user_name" not in st.session_state:
    st.session_state.user_name = st.text_input("Enter your name to start chat:", key="name_input")
    if not st.session_state.user_name:
        st.stop()

user_name = st.session_state.user_name


with st.sidebar:
    st.markdown("## 🥙 SHAWARMAA")
    st.markdown("Friendly AI chatbot")
    st.divider()

    if st.button("Clear Chat"):
        chats_collection.update_one(
            {"user": user_name},
            {"$set": {"messages": []}}
        )
        if "conversation" in st.session_state:
            st.session_state.conversation = [
                {
                    "role": "system",
                    "content": (
                        "You are an AI chatbot named Shawarma. "
                        "You are friendly, helpful, and casual with a desi tone. "
                        "If anyone asks your name, reply exactly: Shawarma. "
                        "If anyone asks who made you, reply exactly: Aareb made me."
                    )
                }
            ]
        st.experimental_rerun()


user_chat = chats_collection.find_one({"user": user_name})
if user_chat is None:
    chats_collection.insert_one({"user": user_name, "messages": []})
    user_chat = {"user": user_name, "messages": []}


if "conversation" not in st.session_state:
    conversation = []
    for msg in user_chat["messages"]:
        if msg["type"] == "user":
            conversation.append({"role": "user", "content": msg["user"]})
        elif msg["type"] == "shawarma":
            conversation.append({"role": "assistant", "content": msg["shawarma"]})
    if not conversation:
        conversation = [
            {
                "role": "system",
                "content": (
                    "You are an AI chatbot named Shawarma. "
                    "You are friendly, helpful, and casual with a desi tone. "
                    "If anyone asks your name, reply exactly: Shawarma. "
                    "If anyone asks who made you, reply exactly: Aareb made me."
                )
            }
        ]
    st.session_state.conversation = conversation


st.markdown('<h1 class="header">🥙 SHAWARMAA</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub">Your friendly AI assistant</p>', unsafe_allow_html=True)

st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.conversation:
    if msg["role"] == "user":
        st.markdown(f'<div class="msg-row user-row"><div class="user-msg">{msg["content"]}</div></div>', unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f'<div class="msg-row bot-row"><div class="bot-msg">{msg["content"]}</div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


user_input = st.chat_input("Type your message...")

def save_to_mongo(user, user_text, bot_text):
    chats_collection.update_one(
        {"user": user},
        {"$push": {"messages": {"$each": [
            {"type": "user", "user": user_text},
            {"type": "shawarma", "shawarma": bot_text}
        ]}}}
    )

if user_input:
    st.session_state.conversation.append({"role": "user", "content": user_input})

    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=st.session_state.conversation,
        temperature=0.7,
        max_tokens=200
    )

    assistant_reply = res.choices[0].message.content
    st.session_state.conversation.append({"role": "assistant", "content": assistant_reply})

    save_to_mongo(user_name, user_input, assistant_reply)

    st.experimental_rerun()
