# import streamlit as st
# from groq import Groq
# import os


# client = Groq(api_key=os.environ["GROQ_API_KEY"])



# # PAGE CONFIG
# st.set_page_config(
#     page_title="SHAWARMAA",
#     page_icon="🥙",
#     layout="centered"
# )





# st.markdown("""
# <style>
# body {
#     background-color: #0e0e0e;
# }

# .chat-container {
#     display: flex;
#     flex-direction: column;
#     gap: 14px;
#     padding-bottom: 20px;
# }

# .msg-row {
#     width: 100%;
#     display: flex;
# }

# .user-row {
#     justify-content: flex-end;
# }

# .bot-row {
#     justify-content: flex-start;
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

# .header {
#     text-align: center;
#     color: #92487A;
#     margin-bottom: 4px;
# }

# .sub {
#     text-align: center;
#     color: #aaa;
#     margin-bottom: 25px;
# }
# </style>
# """, unsafe_allow_html=True)

# # SIDEBAR
# with st.sidebar:
#     st.markdown("## 🥙 SHAWARMAA")
#     st.markdown("Friendly AI chatbot")
#     st.divider()

#     if st.button("Clear Chat"):
#         st.session_state.conversation = [
#             {
#                 "role": "system",
#                 "content": (
#                     "You are an AI chatbot named Shawarma. "
#                     "You are friendly, helpful, and conversational. "
#                     "You are friendly, helpful, and casual with a friendly tone."
#                     "If anyone asks your name, you must say your name is Shawarma. "
#                     "If anyone asks who made you or who created you, "
#                     "you must reply with exactly: Aareb made me."

#                 )
#             }
#         ]
#         st.rerun()


# # SESSION STATE
# if "conversation" not in st.session_state:
#     st.session_state.conversation = [
#     {
#         "role": "system",
#         "content": (
#             "You are an AI chatbot named Shawarma. "
#             "You are friendly, helpful, and conversational. "
#             "You are friendly, helpful, and casual  with a friendly tone."
#             "If anyone asks your name, you must say your name is Shawarma. "
#             "If anyone asks who made you or who created you, "
#             "you must reply with exactly: Aareb made me."

#         )
#     }
# ]


# # HEADER
# st.markdown('<h1 class="header">🥙 SHAWARMAA</h1>', unsafe_allow_html=True)
# st.markdown('<p class="sub">Your friendly AI assistant</p>', unsafe_allow_html=True)

# # CHAT
# st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# for msg in st.session_state.conversation:
#     if msg["role"] == "user":
#         st.markdown(
#             f"""
#             <div class="msg-row user-row">
#                 <div class="user-msg">{msg["content"]}</div>
#             </div>
#             """,
#             unsafe_allow_html=True
#         )

#     elif msg["role"] == "assistant":
#         st.markdown(
#             f"""
#             <div class="msg-row bot-row">
#                 <div class="bot-msg">{msg["content"]}</div>
#             </div>
#             """,
#             unsafe_allow_html=True
#         )

# st.markdown('</div>', unsafe_allow_html=True)

# # INPUT
# user_input = st.chat_input("Type your message...")

# if user_input:
#     st.session_state.conversation.append(
#         {"role": "user", "content": user_input}
#     )

#     res = client.chat.completions.create(
#         model="llama-3.1-8b-instant",
#         messages=st.session_state.conversation,
#         temperature=0.7,
#         max_tokens=200
#     )

#     assistant_reply = res.choices[0].message.content

#     st.session_state.conversation.append(
#         {"role": "assistant", "content": assistant_reply}
#     )

#     st.rerun()



import streamlit as st
from groq import Groq
from tavily import TavilyClient
import os

# from dotenv import load_dotenv
# load_dotenv() 

client = Groq(api_key=os.environ["GROQ_API_KEY"])
tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

# PAGE CONFIG
st.set_page_config(
    page_title="SHAWARMAA",
    page_icon="🥙",
    layout="centered"
)

st.markdown("""
<style>
body { background-color: #0e0e0e; }
.chat-container { display: flex; flex-direction: column; gap: 14px; padding-bottom: 20px; }
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
    margin-top: 12px;  /* gap between user and AI */
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

.header { text-align: center; color: #92487A; }
.sub { text-align: center; color: #aaa; margin-bottom: 25px; }
.sub1 { text-align: center; color: #aaa; }
</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("## 🥙 SHAWARMAA")
    st.markdown("Friendly AI chatbot")
    st.divider()

    if st.button("Clear Chat"):
        st.session_state.conversation = [{
            "role": "system",
            "content": (
                "You are an AI chatbot named Shawarma. "
                "You are friendly, helpful, and conversational. "
                "You are friendly, helpful, and casual with a friendly tone. "
                "If anyone asks your name, you must say your name is Shawarma. "
                "If anyone asks who made you or who created you, "
                "you must reply with exactly: Aareb made me."
                "If the user says goodbye, bye, end the conversation, or anything similar, "
                "you must respond with a short paragraph goodbye message that includes a fun shawarma-related reference, "
            )
        }]
        st.rerun()

# SESSION STATE
if "conversation" not in st.session_state:
    st.session_state.conversation = [{
        "role": "system",
        "content": (
            "You are an AI chatbot named Shawarma. "
            "You are friendly, helpful, and conversational. "
            "You are friendly, helpful, and casual with a friendly tone. "
            "If anyone asks your name, you must say your name is Shawarma. "
            "If anyone asks who made you or who created you, "
            "you must reply with exactly: Aareb made me."
            "If the user says goodbye, bye, end the conversation, or anything similar, "
            "you must respond with a short paragraph goodbye message that includes a fun shawarma-related reference, "
        )

    }]

# HEADER
st.markdown('<h1 class="header">🥙 SHAWARMAA</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub1">With an extra A :)</p>', unsafe_allow_html=True)
st.markdown('<p class="sub">Your friendly AI assistant</p>', unsafe_allow_html=True)

# CHAT UI
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for msg in st.session_state.conversation:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="msg-row user-row">
            <div class="user-msg">{msg["content"]}</div>
        </div>""", unsafe_allow_html=True)

    elif msg["role"] == "assistant":
        st.markdown(f"""
        <div class="msg-row bot-row">
            <div class="bot-msg">{msg["content"]}</div>
        </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 🔎 TAVILY SEARCH FUNCTION
def search_web(query):
    try:
        response = tavily.search(
            query=query,
            search_depth="advanced",
            max_results=5
        )
        results = []
        for r in response["results"]:
            results.append(f"{r['title']} - {r['url']}\n{r['content']}")
        return "\n\n".join(results)
    except:
        return "Sorry I dont know :("

# INPUT
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.conversation.append({"role": "user", "content": user_input})

    # Decide if search needed
    keywords = ["latest", "news", "today", "current", "now", "price", "who won", "update","time"]
    if any(word in user_input.lower() for word in keywords):
        web_data = search_web(user_input)
    else:
        web_data = "No web search needed."

    enhanced_messages = st.session_state.conversation.copy()
    enhanced_messages.append({
        "role": "system",
        "content": f"Here is latest information from the web:\n{web_data}"
    })

    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=enhanced_messages,
        temperature=0.7,
        max_tokens=200
    )

    assistant_reply = res.choices[0].message.content
    st.session_state.conversation.append({"role": "assistant", "content": assistant_reply})

    st.rerun()

