import streamlit as st
from groq import Groq
import os
from pymongo import MongoClient
from datetime import datetime

# ---------- MONGO DB SETUP ----------
mongo_client = MongoClient(st.secrets["MONGODB_URL"])
db = mongo_client["shawarma_db"]
users_collection = db["users"]

# ---------- GET USER NAME ----------
if "username" not in st.session_state:
    st.session_state.username = st.text_input("Enter your name to start:", "")

if not st.session_state.username:
    st.stop()

username = st.session_state.username

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="SHAWARMAA",
    page_icon="🥙",
    layout="centered"
)

# ---------- GROQ CLIENT ----------
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# ---------- CSS ----------
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

# ---------- LOAD OR INIT USER CONVERSATION ----------
user_data = users_collection.find_one({"username": username})
if not user_data:
    st.session_state.conversation = [
        {"type": "system", "content": "You are Shawarma, a friendly AI chatbot. Be casual and desi."}
    ]
    users_collection.insert_one({"username": username, "conversation": st.session_state.conversation})
else:
    st.session_state.conversation = user_data["conversation"]

# ---------- HEADER ----------
st.markdown('<h1 class="header">🥙 SHAWARMAA</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub">Your friendly AI assistant</p>', unsafe_allow_html=True)

# ---------- CHAT DISPLAY ----------
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.conversation:
    if msg["type"] == "user":
        st.markdown(f'<div class="msg-row user-row"><div class="user-msg">{msg["user"]}</div></div>', unsafe_allow_html=True)
    elif msg["type"] == "shawarma":
        st.markdown(f'<div class="msg-row bot-row"><div class="bot-msg">{msg["shawarma"]}</div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------- INPUT ----------
user_input = st.chat_input("Type your message...")

if user_input:
    # Save user message
    st.session_state.conversation.append({"type": "user", "user": user_input})
    users_collection.update_one(
        {"username": username},
        {"$push": {"conversation": {"type": "user", "user": user_input}}}
    )

    # Get AI response
    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role":"system","content":"You are Shawarma, friendly AI."}] + [{"role":"user","content": user_input}],
        temperature=0.7,
        max_tokens=200
    )

    assistant_reply = res.choices[0].message.content

    # Save assistant message
    st.session_state.conversation.append({"type": "shawarma", "shawarma": assistant_reply})
    users_collection.update_one(
        {"username": username},
        {"$push": {"conversation": {"type": "shawarma", "shawarma": assistant_reply}}}
    )

    st.rerun()
