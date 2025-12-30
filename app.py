import streamlit as st
from groq import Groq
from pymongo import MongoClient
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="SHAWARMAA", page_icon="🥙", layout="centered")

# ---------------- CSS ----------------
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

# ---------------- DATABASE ----------------
mongo_uri = st.secrets["MONGODB_URL"]
db_client = MongoClient(mongo_uri)
db = db_client["shawarmaa_db"]
chats_col = db["chats"]

# ---------------- USERNAME ----------------
if "username" not in st.session_state:
    st.session_state.username = st.text_input("Enter your name to start:")

if not st.session_state.username:
    st.stop()

username = st.session_state.username

# ---------------- GROQ CLIENT ----------------
groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])

# ---------------- SESSION STATE ----------------
if "conversation" not in st.session_state:
    # Load previous conversation if exists
    user_data = chats_col.find_one({"user": username})
    if user_data:
        st.session_state.conversation = user_data["messages"]
    else:
        st.session_state.conversation = [
            {"type": "system", "system": (
                "You are an AI chatbot named Shawarma. "
                "Friendly, helpful, casual with desi tone. "
                "If anyone asks your name, reply 'Shawarma'. "
                "If anyone asks who made you, reply 'Aareb made me'."
            )}
        ]

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## 🥙 SHAWARMAA")
    st.markdown("Friendly AI chatbot")
    st.divider()
    if st.button("Clear Chat"):
        st.session_state.conversation = [st.session_state.conversation[0]]  # keep system prompt
        chats_col.update_one(
            {"user": username},
            {"$set": {"messages": st.session_state.conversation}},
            upsert=True
        )
        st.rerun()

# ---------------- HEADER ----------------
st.markdown('<h1 class="header">🥙 SHAWARMAA</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub">Your friendly AI assistant</p>', unsafe_allow_html=True)

# ---------------- CHAT DISPLAY ----------------
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.conversation:
    if msg["type"] == "user":
        st.markdown(f'<div class="msg-row user-row"><div class="user-msg">{msg["user"]}</div></div>', unsafe_allow_html=True)
    elif msg["type"] == "shawarma":
        st.markdown(f'<div class="msg-row bot-row"><div class="bot-msg">{msg["shawarma"]}</div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- USER INPUT ----------------
user_input = st.chat_input("Type your message...")
if user_input:
    # Add user message
    st.session_state.conversation.append({"type": "user", "user": user_input})

    # Prepare Groq messages
    groq_messages = []
    for m in st.session_state.conversation:
        if m["type"] == "system":
            groq_messages.append({"role": "system", "content": m["system"]})
        elif m["type"] == "user":
            groq_messages.append({"role": "user", "content": m["user"]})
        elif m["type"] == "shawarma":
            groq_messages.append({"role": "assistant", "content": m["shawarma"]})

    # Get AI response
    res = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=groq_messages,
        temperature=0.7,
        max_tokens=200
    )
    assistant_reply = res.choices[0].message.content
    st.session_state.conversation.append({"type": "shawarma", "shawarma": assistant_reply})

    # Save to MongoDB
    chats_col.update_one(
        {"user": username},
        {"$set": {"messages": st.session_state.conversation}},
        upsert=True
    )

    st.rerun()
