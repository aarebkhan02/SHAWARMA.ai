import streamlit as st
from groq import Groq
from pymongo import MongoClient


st.set_page_config(
    page_title="SHAWARMAA",
    page_icon="🥙",
    layout="centered"
)


groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])


mongo_client = MongoClient(st.secrets["MONGODB_URL"])
db = mongo_client["shawarma_db"]
users = db["users"]   # one document per user


def get_user(username):
    user = users.find_one({"username": username})
    if not user:
        users.insert_one({
            "username": username,
            "messages": []
        })
        user = users.find_one({"username": username})
    return user

def save_user_message(username, text):
    users.update_one(
        {"username": username},
        {"$push": {"messages": {"type": "user", "user": text}}}
    )

def save_bot_message(username, text):
    users.update_one(
        {"username": username},
        {"$push": {"messages": {"type": "shawarma", "shawarma": text}}}
    )


if "username" not in st.session_state:
    st.markdown("## 👋 Welcome to SHAWARMAA")
    name = st.text_input("Enter your name")

    if st.button("Start Chat") and name.strip():
        st.session_state.username = name.strip()
        get_user(st.session_state.username)
        st.rerun()

    st.stop()

username = st.session_state.username
user_doc = get_user(username)

#  SIDEBAR 
with st.sidebar:
    st.markdown("## 🥙 SHAWARMAA")
    st.markdown(f" **{username}**")
    st.divider()

    if st.button("Clear Chat"):
        users.update_one(
            {"username": username},
            {"$set": {"messages": []}}
        )
        st.rerun()

#  HEADER 
st.markdown("## 🥙 SHAWARMAA")
st.markdown(f"Hello **{username}** ")


for msg in user_doc["messages"]:
    if msg["type"] == "user":
        st.markdown(
            f"<div style='text-align:right;color:white;background:#85409D;padding:10px;border-radius:10px;margin:5px;'>"
            f"{msg['user']}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div style='text-align:left;color:white;background:#878787;padding:10px;border-radius:10px;margin:5px;'>"
            f"{msg['shawarma']}</div>",
            unsafe_allow_html=True
        )

# INPUT 
user_input = st.chat_input("Type your message...")

if user_input:
    # Save user message
    save_user_message(username, user_input)

    # Prepare messages for AI
    chat_for_ai = []
    for m in user_doc["messages"]:
        if m["type"] == "user":
            chat_for_ai.append({"role": "user", "content": m["user"]})
        else:
            chat_for_ai.append({"role": "assistant", "content": m["shawarma"]})

    chat_for_ai.append({"role": "user", "content": user_input})

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=chat_for_ai,
        temperature=0.7,
        max_tokens=200
    )

    bot_reply = response.choices[0].message.content

    # Save bot message
    save_bot_message(username, bot_reply)

    st.rerun()
