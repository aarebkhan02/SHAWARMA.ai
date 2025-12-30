import streamlit as st
from groq import Groq
from pymongo import MongoClient
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SHAWARMAA",
    page_icon="🥙",
    layout="centered"
)

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
client_db = MongoClient(mongo_uri)
db = client_db["shawarmaa_db"]
chats_col = db["chats"]

# ---------------- USER NAME INPUT ----------------
if "username" not in st.session_state:
    st.session_state.username = st.text_input("Enter your name to start the chat:")

if not st.session_state.username:
    st.stop()

username = st.session_state.username

# ---------------- GROQ CLIENT ----------------
groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])

# ---------------- SESSION STATE ----------------
if "conversation" not in st.session_state:
    st.session_state.conversation = [
        {
            "type": "system",
            "system": (
                "You are an AI chatbot named Shawarma. "
                "You are friendly, helpful, and conversational. "
                "You are friendly, helpful, and casual with a desi tone. "
                "If anyone asks your name, you must say your name is Shawarma. "
                "If anyone asks who made you or who created you, you must reply with exactly: Aareb made me."
            )
        }
    ]

# ---------------- USER INPUT ----------------
user_input = st.chat_input("Type your message...")
if user_input:
    st.session_state.conversation.append({"type": "user", "user": user_input})

    # ---------------- GROQ RESPONSE ----------------
    # Convert conversation to Groq format including system
    messages_for_groq = []
    for m in st.session_state.conversation:
        if m["type"] == "user":
            messages_for_groq.append({"role": "user", "content": m["user"]})
        elif m["type"] == "shawarma":
            messages_for_groq.append({"role": "assistant", "content": m["shawarma"]})
        elif m["type"] == "system":
            messages_for_groq.append({"role": "system", "content": m["system"]})

    res = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages_for_groq,
        temperature=0.7,
        max_tokens=200
    )

    assistant_reply = res.choices[0].message.content
    st.session_state.conversation.append({"type": "shawarma", "shawarma": assistant_reply})

    
    chats_col.update_one(
        {"user": username},
        {"$set": {"messages": st.session_state.conversation}},
        upsert=True
    )

    st.rerun()
