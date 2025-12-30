import streamlit as st
from groq import Groq
import os
from pymongo import MongoClient
from datetime import datetime
import uuid

# ---------------- API CLIENTS ----------------
client = Groq(api_key=os.environ["GROQ_API_KEY"])
mongo_client = MongoClient(st.secrets["MONGO_URI"])
db = mongo_client["shawarma_db"]
chats_collection = db["chats"]

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SHAWARMAA",
    page_icon="🥙",
    layout="centered"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
body {background-color: #0e0e0e;}
.chat-container {display: flex; flex-direction: column; gap: 14px; padding-bottom: 20px;}
.msg-row {width: 100%; display: flex;}
.user-row {justify-content: flex-end;}
.bot-row {justify-content: flex-start;}
.user-msg {background-color: #85409D; color: white; padding: 14px 18px; border-radius: 18px 18px 4px 18px; max-width: 72%; font-size: 15px; line-height: 1.4; word-wrap: break-word;}
.bot-msg {background-color: #878787; color: white; padding: 14px 18px; border-radius: 18px 18px 18px 4px; max-width: 72%; font-size: 15px; line-height: 1.4; word-wrap: break-word;}
.header {text-align: center; color: #92487A; margin-bottom: 4px;}
.sub {text-align: center; color: #aaa; margin-bottom: 25px;}
</style>
""", unsafe_allow_html=True)

# ---------------- USER SESSION ----------------
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

user_doc = chats_collection.find_one({"user_id": st.session_state.user_id})
if "conversation" not in st.session_state:
    if user_doc:
        st.session_state.conversation = []
        for msg in user_doc["messages"]:
            if msg["type"] == "user":
                st.session_state.conversation.append({"role":"user","content":msg["user"]})
            else:
                st.session_state.conversation.append({"role":"assistant","content":msg["shawarma"]})
    else:
        st.session_state.conversation = [
            {"role":"system","content":"You are an AI chatbot named Shawarma. You are friendly, helpful, casual. If asked who made you, reply: Aareb made me."}
        ]

# ---------------- HEADER ----------------
st.markdown('<h1 class="header">🥙 SHAWARMAA</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub">Your friendly AI assistant</p>', unsafe_allow_html=True)

# ---------------- CHAT ----------------
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.conversation:
    if msg["role"]=="user":
        st.markdown(f'<div class="msg-row user-row"><div class="user-msg">{msg["content"]}</div></div>', unsafe_allow_html=True)
    elif msg["role"]=="assistant":
        st.markdown(f'<div class="msg-row bot-row"><div class="bot-msg">{msg["content"]}</div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- HELPER ----------------
def save_message(user_id, role, content):
    chats_collection.update_one(
        {"user_id": user_id},
        {"$push": {"messages": {"type": "user" if role=="user" else "shawarma", "user": content if role=="user" else None, "shawarma": content if role=="assistant" else None}}},
        upsert=True
    )

# ---------------- INPUT ----------------
user_input = st.chat_input("Type your message...")
if user_input:
    st.session_state.conversation.append({"role":"user","content":user_input})
    save_message(st.session_state.user_id,"user",user_input)

    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=st.session_state.conversation,
        temperature=0.7,
        max_tokens=200
    )

    assistant_reply = res.choices[0].message.content
    st.session_state.conversation.append({"role":"assistant","content":assistant_reply})
    save_message(st.session_state.user_id,"assistant",assistant_reply)

    st.rerun()

# ---------------- CLEAR CHAT ----------------
with st.sidebar:
    st.markdown("## 🥙 SHAWARMAA")
    st.markdown("Friendly AI chatbot")
    st.divider()
    if st.button("Clear Chat"):
        chats_collection.delete_one({"user_id": st.session_state.user_id})
        st.session_state.conversation = [
            {"role":"system","content":"You are an AI chatbot named Shawarma. You are friendly, helpful, casual. If asked who made you, reply: Aareb made me."}
        ]
        st.rerun()
