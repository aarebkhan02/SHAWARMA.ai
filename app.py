# import streamlit as st
# from groq import Groq
# from tavily import TavilyClient
# import os

# # from dotenv import load_dotenv
# # load_dotenv() 

# client = Groq(api_key=os.environ["GROQ_API_KEY"])
# tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

# # PAGE CONFIG
# st.set_page_config(
#     page_title="SHAWARMAA",
#     page_icon="🥙",
#     layout="centered"
# )

# st.markdown("""
# <style>
# body { background-color: #0e0e0e; }
# .chat-container { display: flex; flex-direction: column; gap: 14px; padding-bottom: 20px; }
# .msg-row { 
#     width: 100%; 
#     display: flex; 
#     margin-top: 6px;
# }

# .user-row { 
#     justify-content: flex-end; 
# }

# .bot-row { 
#     justify-content: flex-start; 
#     margin-top: 12px;  /* gap between user and AI */
# }
# .user-msg {
#     background-color: #85409D;
#     color: white;
#     padding: 14px 18px;
#     border-radius: 18px 18px 4px 18px;
#     max-width: 72%;
#     font-size: 15px;
#     line-height: 1.4;
#     word-wrap: break-word;
# }
# .bot-msg {
#     background-color: #878787;
#     color: white;
#     padding: 14px 18px;
#     border-radius: 18px 18px 18px 4px;
#     max-width: 72%;
#     font-size: 15px;
#     line-height: 1.4;
#     word-wrap: break-word;
# }
#             .loading {
#     background-color: #878787;
#     color: white;
#     padding: 14px 18px;
#     border-radius: 18px 18px 18px 4px;
#     max-width: 72%;
#     font-size: 15px;
#     opacity: 0.8;
#     animation: pulse 1s infinite;
# }

# @keyframes pulse {
#     0% { opacity: 0.4; }
#     50% { opacity: 1; }
#     100% { opacity: 0.4; }
# }

# .header { text-align: center; color: #92487A; }
# .sub { text-align: center; color: #aaa; margin-bottom: 25px; }
# .sub1 { text-align: center; color: #aaa; }
# </style>
# """, unsafe_allow_html=True)

# # SIDEBAR
# with st.sidebar:
#     st.markdown("## 🥙 SHAWARMAA")
#     st.markdown("Friendly AI chatbot")
#     st.divider()

#     if st.button("Clear Chat"):
#         st.session_state.conversation = [{
#             "role": "system",
#             "content": (
#                 "You are an AI chatbot named Shawarma. "
#                 "You are friendly, helpful, and conversational. "
#                 "You are friendly, helpful, and casual with a friendly tone. "
#                 "If anyone asks your name, you must say your name is Shawarma. "
#                 "If anyone asks who made you or who created you, "
#                 "you must reply with exactly: Aareb made me."
#                 "If the user says goodbye, bye, end the conversation, or anything similar, "
#                 "you must respond with a short paragraph goodbye message that includes a fun shawarma-related reference, "
#             )
#         }]
#         st.rerun()

# # SESSION STATE
# if "conversation" not in st.session_state:
#     st.session_state.conversation = [{
#         "role": "system",
#         "content": (
#             "You are an AI chatbot named Shawarma. "
#             "You are friendly, helpful, and conversational. "
#             "You are friendly, helpful, and casual with a friendly tone. "
#             "If anyone asks your name, you must say your name is Shawarma. "
#             "If anyone asks who made you or who created you, "
#             "you must reply with exactly: Aareb made me."
#             "If the user says goodbye, bye, end the conversation, or anything similar, "
#             "you must respond with a short paragraph goodbye message that includes a fun shawarma-related reference, "
#         )

#     }]

# # HEADER
# st.markdown('<h1 class="header">🥙 SHAWARMAA</h1>', unsafe_allow_html=True)
# st.markdown('<p class="sub1">With an extra A :)</p>', unsafe_allow_html=True)
# st.markdown('<p class="sub">Your friendly AI assistant</p>', unsafe_allow_html=True)

# # CHAT UI
# st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# for msg in st.session_state.conversation:
#     if msg["role"] == "user":
#         st.markdown(f"""
#         <div class="msg-row user-row">
#             <div class="user-msg">{msg["content"]}</div>
#         </div>""", unsafe_allow_html=True)

#     elif msg["role"] == "assistant":
#         st.markdown(f"""
#         <div class="msg-row bot-row">
#             <div class="bot-msg">{msg["content"]}</div>
#         </div>""", unsafe_allow_html=True)

# st.markdown('</div>', unsafe_allow_html=True)

# #  TAVILY SEARCH FUNCTION
# def search_web(query):
#     try:
#         response = tavily.search(
#             query=query,
#             search_depth="advanced",
#             max_results=5
#         )
#         results = []
#         for r in response["results"]:
#             results.append(f"{r['title']} - {r['url']}\n{r['content']}")
#         return "\n\n".join(results)
#     except:
#         return "Sorry I dont know :("

# # INPUT
# user_input = st.chat_input("Type your message...")

# if user_input:
#     st.session_state.conversation.append({"role": "user", "content": user_input})

#     # Decide if search needed
#     keywords = ["latest", "news", "today", "current", "now", "price", "who won", "update","time"]
#     if any(word in user_input.lower() for word in keywords):
#         web_data = search_web(user_input)
#     else:
#         web_data = "No web search needed."

#     enhanced_messages = st.session_state.conversation.copy()
#     enhanced_messages.append({
#         "role": "system",
#         "content": f"Here is latest information from the web:\n{web_data}"
#     })

#     res = client.chat.completions.create(
#         model="llama-3.1-8b-instant",
#         messages=enhanced_messages,
#         temperature=0.7,
#         max_tokens=200
#     )

#     assistant_reply = res.choices[0].message.content
#     st.session_state.conversation.append({"role": "assistant", "content": assistant_reply})

#     st.rerun()

import streamlit as st
from groq import Groq
from tavily import TavilyClient
import os
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


# =========================
# API CLIENTS
# =========================

client = Groq(api_key=os.environ["GROQ_API_KEY"])
tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


def load_resume():

    reader = PdfReader("Aareb_Resume_With_Links.pdf")

    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text


def chunk_text(text, chunk_size=400):

    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])

    return chunks



@st.cache_resource
def load_rag():

    embed_model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    resume_text = load_resume()

    resume_chunks = chunk_text(resume_text)

    chunk_embeddings = embed_model.encode(
        resume_chunks,
        
    )

    dimension = len(chunk_embeddings[0])

    index = faiss.IndexFlatL2(dimension)

    index.add(chunk_embeddings.astype("float32"))

    return embed_model, index, resume_chunks
embed_model, index, resume_chunks = load_rag()



def search_resume(query, k=1):

    query_embedding = embed_model.encode(
        [query],
        
    )

    distances, indices = index.search(
        query_embedding.astype("float32"),
        k
    )

    # similarity threshold
    if distances[0][0] > 2.0:
        return ""

    results = []

    for idx in indices[0]:
        results.append(resume_chunks[idx])

    return "\n".join(results)


resume_keywords = [ "aareb", "resume", "skills", "projects", "internship", "experience", "education", "who made you", "developer", "creator" ]

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="SHAWARMAA",
    page_icon="🥙",
    layout="centered"
)

# =========================
# CUSTOM CSS
# =========================

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
    margin-top: 6px;
}

.user-row {
    justify-content: flex-end;
}

.bot-row {
    justify-content: flex-start;
    margin-top: 12px;
}

.user-msg {
    background-color: #85409D;
    color: white;
    padding: 14px 18px;
    border-radius: 18px 18px 4px 18px;
    max-width: 72%;
    font-size: 15px;
    line-height: 1.5;
    word-wrap: break-word;
}

.bot-msg {
    background-color: #878787;
    color: white;
    padding: 14px 18px;
    border-radius: 18px 18px 18px 4px;
    max-width: 72%;
    font-size: 15px;
    line-height: 1.5;
    word-wrap: break-word;
}

.loading {
    background-color: #878787;
    color: white;
    padding: 14px 18px;
    border-radius: 18px 18px 18px 4px;
    max-width: 72%;
    font-size: 15px;
    opacity: 0.8;
    animation: pulse 1s infinite;
}

@keyframes pulse {
    0% { opacity: 0.4; }
    50% { opacity: 1; }
    100% { opacity: 0.4; }
}

.header {
    text-align: center;
    color: #92487A;
}

.sub {
    text-align: center;
    color: #aaa;
    margin-bottom: 25px;
}

.sub1 {
    text-align: center;
    color: #aaa;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.markdown("## 🥙 SHAWARMAA")
    st.markdown("Friendly AI chatbot")
    st.divider()

    if st.button("Clear Chat"):

        st.session_state.conversation = [
            {
                "role": "system",
                "content": (
                    "You are Shawarma, a friendly AI chatbot. "
                    "Keep responses short, conversational, and helpful. "
                    "If asked your name, say your name is Shawarma. "
                    "If asked about Aareb, use the provided resume context only. "
                    "If asked who made you, reply exactly: Aareb made me."
                )
            }
        ]

        st.rerun()

# =========================
# SESSION STATE
# =========================

if "conversation" not in st.session_state:

    st.session_state.conversation = [
        {
            "role": "system",
            "content": (
                "You are Shawarma, a friendly AI chatbot. "
                "Keep responses short, conversational, and helpful. "
                "If asked your name, say your name is Shawarma. "
                "If asked about Aareb, use the provided resume context only. "
                "If asked who made you, reply exactly: Aareb made me."
            )
        }
    ]

# =========================
# HEADER
# =========================

st.markdown(
    '<h1 class="header">🥙 SHAWARMAA</h1>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub1">With an extra A :)</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub">Your friendly AI assistant</p>',
    unsafe_allow_html=True
)

# =========================
# CHAT DISPLAY
# =========================

st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for msg in st.session_state.conversation:

    if msg["role"] == "user":

        st.markdown(f"""
        <div class="msg-row user-row">
            <div class="user-msg">{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)

    elif msg["role"] == "assistant":

        st.markdown(f"""
        <div class="msg-row bot-row">
            <div class="bot-msg">{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# FAST TAVILY SEARCH
# =========================

@st.cache_data(ttl=300)
def search_web(query):

    try:

        response = tavily.search(
            query=query,
            search_depth="basic",
            max_results=2
        )

        results = []

        for r in response["results"]:

            results.append(
                f"{r['title']}\n{r['content']}"
            )

        return "\n\n".join(results)

    except Exception:

        return ""

# =========================
# SEARCH DETECTION
# =========================

search_keywords = [
    "latest",
    "news",
    "today",
    "current",
    "now",
    "price",
    "weather",
    "score",
    "match",
    "who won",
    "update",
    "stock",
    "bitcoin",
    "time"
]

# =========================
# USER INPUT
# =========================

user_input = st.chat_input("Type your message...")

if user_input:

    # =========================
    # SAVE USER MESSAGE
    # =========================

    st.session_state.conversation.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # SHOW USER MESSAGE INSTANTLY

    st.markdown(f"""
    <div class="msg-row user-row">
        <div class="user-msg">{user_input}</div>
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # SEARCH DETECTION
    # =========================

    query_lower = user_input.lower()

    # WEB SEARCH CHECK

    needs_search = any(
        word in query_lower
        for word in search_keywords
    )

    # RESUME SEARCH CHECK

    needs_resume = any(
        word in query_lower
        for word in resume_keywords
    )

    # =========================
    # GET WEB DATA
    # =========================

    web_data = ""

    if needs_search:
        web_data = search_web(user_input)

    # =========================
    # GET RESUME DATA
    # =========================

    resume_data = ""

    if needs_resume:
        resume_data = search_resume(user_input)

    # =========================
    # CREATE MESSAGES
    # =========================

    enhanced_messages = [
        {
            "role": "system",
            "content": (
                "You are Shawarma, a fast, friendly AI chatbot. "
                "Keep responses concise and conversational. "
                "If asked your name, say your name is Shawarma. "
                "If asked who made you, reply exactly: Aareb made me."
            )
        }
    ]

    # ADD CHAT HISTORY

    for msg in st.session_state.conversation:

        if msg["role"] != "system":
            enhanced_messages.append(msg)

    # =========================
    # ADD WEB CONTEXT
    # =========================

    if web_data:

        enhanced_messages.append(
            {
                "role": "system",
                "content": (
                    f"""
Latest web information:

{web_data}

Use this information if relevant.
"""
                )
            }
        )

    # =========================
    # ADD RESUME CONTEXT
    # =========================

    if resume_data:

        enhanced_messages.append(
            {
                "role": "system",
                "content": (
                    f"You are answering questions about Aareb.\n\n"
                    f"Use ONLY the resume information below.\n\n"
                    f"DO NOT invent or assume anything.\n\n"
                    f"If the answer is not clearly present, "
                    f"reply with: "
                    f"'I could not find that information.'\n\n"
                    f"Resume Information:\n{resume_data}"
                )
            }
        )

    # =========================
    # LOADING ANIMATION
    # =========================

    loading_placeholder = st.empty()

    loading_placeholder.markdown("""
    <div class="msg-row bot-row">
        <div class="loading">Typing...</div>
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # STREAMING RESPONSE
    # =========================

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=enhanced_messages,
        temperature=0.5,
        max_tokens=120,
        stream=True
    )

    # REMOVE LOADING

    loading_placeholder.empty()

    # =========================
    # LIVE RESPONSE UI
    # =========================

    response_placeholder = st.empty()

    full_response = ""

    for chunk in response:

        content = chunk.choices[0].delta.content

        if content:

            full_response += content

            response_placeholder.markdown(f"""
            <div class="msg-row bot-row">
                <div class="bot-msg">{full_response}</div>
            </div>
            """, unsafe_allow_html=True)

    # =========================
    # SAVE ASSISTANT RESPONSE
    # =========================

    st.session_state.conversation.append(
        {
            "role": "assistant",
            "content": full_response
        }
    )

    