import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# --------------------------------------------------
# 1. Load environment variables
# --------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-3.5-flash-lite"

# --------------------------------------------------
# 2. Configure the web page
# --------------------------------------------------

st.set_page_config(
    page_title="Student Support Chatbot",
    page_icon="🎓",
    layout="wide"
)

# --------------------------------------------------
# 3. Custom CSS styling
# --------------------------------------------------

st.markdown(
    """
    <style>
    :root {
        --ink: #1b2340;
        --muted: #626b83;
        --paper: #fff8ed;
        --white: #ffffff;
        --forest: #3153d8;
        --forest-dark: #203eaa;
        --mint: #e2f7ef;
        --line: #e5dece;
        --coral: #f0674f;
        --sun: #ffd34f;
        --aqua: #43c7bd;
    }

    .stApp {
        color: var(--ink);
        background-color: var(--paper);
        background-image:
            linear-gradient(rgba(49, 83, 216, 0.045) 1px, transparent 1px),
            linear-gradient(90deg, rgba(240, 103, 79, 0.04) 1px, transparent 1px);
        background-size: 28px 28px;
    }

    header[data-testid="stHeader"] {
        background: rgba(255, 248, 237, 0.92);
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 1120px;
        padding-top: 4rem;
        padding-bottom: 7rem;
    }

    [data-testid="stSidebar"] {
        background: #354bc4;
        border-right: 1px solid #293da9;
    }

    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ffffff;
        font-family: "DM Sans", "Trebuchet MS", sans-serif;
        letter-spacing: 0;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] label {
        color: #edf0ff;
        font-size: 0.92rem;
    }

    [data-testid="stSelectbox"] [role="group"] {
        border: 1px solid #ffe083;
        background: #fff2b8 !important;
        border-radius: 9px;
    }

    [data-testid="stSelectbox"] input[role="combobox"] {
        background: transparent !important;
        color: #273469 !important;
    }

    [data-testid="stSelectbox"] button {
        color: #273469 !important;
    }

    [data-testid="stSidebar"] li::marker {
        color: var(--sun);
    }

    .brand-row {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        margin: 0.2rem 0 1.5rem;
    }

    .brand-mark {
        display: grid;
        width: 42px;
        height: 42px;
        place-items: center;
        border-radius: 12px;
        background: var(--coral);
        color: white;
        font-family: "DM Sans", "Trebuchet MS", sans-serif;
        font-size: 1.1rem;
        font-weight: 800;
    }

    .brand-kicker {
        color: #354bc4;
        font-family: "DM Sans", "Trebuchet MS", sans-serif;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0;
        text-transform: uppercase;
    }

    .brand-detail {
        margin-top: 0.12rem;
        color: var(--muted);
        font-size: 0.86rem;
    }

    .main-title {
        margin: 0;
        color: #243a9f;
        font-family: "DM Sans", "Trebuchet MS", sans-serif;
        font-size: 2.55rem;
        font-weight: 750;
        line-height: 1.1;
    }

    .title-highlight {
        display: inline-block;
        padding: 0 0.18em 0.06em;
        border-radius: 5px;
        background: var(--sun);
        color: #28346f;
    }

    .subtitle {
        margin: 0.6rem 0 1.6rem;
        color: var(--muted);
        font-size: 1.02rem;
    }

    .welcome-box {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        min-height: 76px;
        margin: 0.7rem 0 1rem;
        padding: 0.9rem 1.15rem;
        border: 1px solid #2746bc;
        border-left: 6px solid var(--sun);
        border-radius: 10px;
        background: #3153d8;
        color: #ffffff;
        box-shadow: 0 8px 22px rgba(49, 83, 216, 0.16);
        line-height: 1.45;
    }

    .welcome-copy {
        display: flex;
        flex-direction: column;
        gap: 0.18rem;
    }

    .welcome-greeting {
        color: #ffffff;
        font-size: 1rem;
        font-weight: 750;
    }

    .welcome-subject {
        color: #e3e9ff;
        font-size: 0.9rem;
    }

    .welcome-subject strong {
        color: var(--sun);
    }

    .welcome-note {
        padding: 0.35rem 0.65rem;
        border: 1px solid #f5c946;
        border-radius: 999px;
        background: var(--sun);
        color: #3d351d;
        font-size: 0.78rem;
        font-weight: 700;
        white-space: nowrap;
    }

    div[data-testid="stChatMessage"] {
        width: fit-content;
        max-width: min(82%, 760px);
        margin: 0.65rem 0;
        padding: 0.8rem 1rem;
        border: 1px solid #e8e4dc;
        border-left: 4px solid var(--aqua);
        border-radius: 12px;
        background: var(--white);
        box-shadow: 0 4px 14px rgba(29, 48, 44, 0.04);
    }

    div[data-testid="stChatMessage"][aria-label="Chat message from user"] {
        margin-left: auto;
        border-color: var(--coral);
        background: var(--coral);
        color: white;
    }

    div[data-testid="stChatMessage"][aria-label="Chat message from user"] p,
    div[data-testid="stChatMessage"][aria-label="Chat message from user"] li {
        color: white;
    }

    div[data-testid="stChatMessage"] p {
        color: var(--ink);
        line-height: 1.7;
    }

    div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] > :last-child {
        margin-bottom: 0;
    }

    .stChatFloatingInputContainer {
        border-top: 1px solid var(--line);
        background: rgba(255, 248, 237, 0.96);
        backdrop-filter: blur(12px);
    }

    [data-testid="stBottom"],
    [data-testid="stBottomBlockContainer"] {
        background: transparent;
    }

    [data-testid="stBottom"] > div {
        border-top: 1px solid var(--line);
        background: rgba(255, 248, 237, 0.97) !important;
        backdrop-filter: blur(12px);
    }

    div[data-testid="stChatInput"] {
        border: 1px solid #cfd6fb;
        border-radius: 12px;
        background: var(--white);
        box-shadow: 0 8px 28px rgba(36, 51, 117, 0.16);
    }

    div[data-testid="stChatInput"] > div {
        border-radius: 10px;
        background: var(--white) !important;
    }

    div[data-testid="stChatInput"]:focus-within {
        border-color: var(--forest);
        box-shadow: 0 0 0 3px rgba(49, 83, 216, 0.16);
    }

    div[data-testid="stChatInput"] textarea {
        background: var(--white);
        color: var(--ink);
    }

    div[data-testid="stChatInput"] textarea::placeholder {
        color: #64736d;
        opacity: 1;
    }

    div[data-testid="stChatInput"] button {
        border-radius: 9px;
        background: var(--forest);
        color: white;
    }

    .stButton > button {
        min-height: 2.7rem;
        border: 1px solid #f3a08c;
        border-radius: 9px;
        background: var(--white);
        color: #bd493b;
        font-weight: 650;
        transition: background 140ms ease, border-color 140ms ease;
    }

    .stButton > button:hover {
        border-color: var(--coral);
        background: #fff0e7;
        color: var(--forest-dark);
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.28);
    }

    @media (max-width: 700px) {
        [data-testid="stMainBlockContainer"] {
            padding: 4rem 1rem 6rem;
        }

        .brand-row {
            margin-bottom: 1.1rem;
        }

        .main-title {
            font-size: 2.05rem;
        }

        .welcome-box {
            align-items: flex-start;
            flex-direction: column;
            gap: 0.7rem;
        }

        .welcome-note {
            white-space: normal;
        }

        div[data-testid="stChatMessage"] {
            max-width: 94%;
            padding: 0.65rem 0.8rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# 4. Application heading
# --------------------------------------------------

st.markdown(
    """
    <div class="brand-row">
        <div class="brand-mark">S</div>
        <div>
            <div class="brand-kicker">Student Support</div>
            <div class="brand-detail">Your study room</div>
        </div>
    </div>
    <h1 class="main-title">Make room to <span class="title-highlight">learn.</span></h1>
    <p class="subtitle">A focused place for today's questions.</p>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# 5. Check the API key
# --------------------------------------------------

if not API_KEY:
    st.error(
        "Gemini API key is missing. "
        "Add GEMINI_API_KEY to your .env file."
    )
    st.stop()

# --------------------------------------------------
# 6. Connect to Gemini
# --------------------------------------------------

@st.cache_resource
def get_client(api_key):
    return genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(timeout=30_000)
    )


try:
    client = get_client(API_KEY)
except Exception as error:
    st.error("Could not initialize Gemini. Check your API setup.")
    print(f"Gemini client initialization error: {type(error).__name__}")
    st.stop()

# --------------------------------------------------
# 7. Student support instructions
# --------------------------------------------------

SYSTEM_INSTRUCTION = """
You are a friendly Student Support Chatbot.

Your goal is to help students learn and study effectively.

Your responsibilities:
- Explain academic concepts in simple language.
- Help with mathematics, science, English, and programming.
- Provide exam preparation tips and revision strategies.
- Create realistic study timetables.
- Generate practice questions and quizzes.
- Explain answers step by step when useful.
- Encourage students who feel nervous about exams.
- Adapt explanations to the student's selected subject.
- Respond in clear, supportive language.
- Never invent official school policies, exam dates, or results.
- If you do not know an answer, be honest.

You are an educational assistant, not an official school authority.
"""

WELCOME_MESSAGE = {
    "role": "assistant",
    "content": (
        "Hello! 👋 Welcome to Student Support Chatbot.\n\n"
        "I'm here to help you learn, revise, and prepare "
        "for exams. What would you like to study today?"
    )
}

# --------------------------------------------------
# 8. Create a new conversation
# --------------------------------------------------

def create_chat():
    return client.chats.create(
        model=MODEL_NAME,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.7
        )
    )


def start_new_conversation():
    chat = create_chat()
    st.session_state.chat = chat
    st.session_state.messages = [WELCOME_MESSAGE.copy()]


# --------------------------------------------------
# 9. Sidebar
# --------------------------------------------------

with st.sidebar:
    st.header("Study desk")

    st.write("Set your focus for this session.")

    subject = st.selectbox(
        "Select Subject",
        [
            "General Study Help",
            "Mathematics",
            "Science",
            "Computer Science",
            "English",
            "Exam Preparation",
            "Study Planning"
        ]
    )

    st.divider()

    st.subheader("A few starting points")

    st.markdown(
        """
        - Explain photosynthesis.
        - Teach me Python loops.
        - Create a revision timetable.
        - Give me a mathematics quiz.
        - How can I improve concentration?
        """
    )

    st.divider()

    st.caption("Powered by Python, Streamlit and Gemini AI.")

# --------------------------------------------------
# 10. Initialize session state
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = [WELCOME_MESSAGE.copy()]

if "chat" not in st.session_state:
    try:
        st.session_state.chat = create_chat()
    except Exception as error:
        st.error(
            "Could not create a Gemini conversation. Check your API key, "
            "model access, and internet connection."
        )
        print(f"Gemini conversation error: {type(error).__name__}")
        st.stop()

if "active_subject" not in st.session_state:
    st.session_state.active_subject = subject

# Start a fresh conversation when the subject changes.
if subject != st.session_state.active_subject:
    try:
        start_new_conversation()
        st.session_state.active_subject = subject
    except Exception as error:
        st.error("Could not start a new Gemini conversation. Please try again.")
        print(f"Gemini conversation error: {type(error).__name__}")
        st.stop()

# --------------------------------------------------
# 11. Welcome message
# --------------------------------------------------

st.markdown(
    f"""
    <div class="welcome-box">
        <div class="welcome-copy">
            <span class="welcome-greeting">Welcome, Student! 👋</span>
            <span class="welcome-subject">Current focus: <strong>{subject}</strong></span>
        </div>
        <span class="welcome-note">SESSION READY</span>
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# 12. New chat button
# --------------------------------------------------

if st.button("🔄 Start New Chat", use_container_width=True):
    try:
        start_new_conversation()
    except Exception as error:
        st.error("Could not start a new Gemini conversation. Please try again.")
        print(f"Gemini conversation error: {type(error).__name__}")
    st.rerun()

# --------------------------------------------------
# 13. Display conversation history
# --------------------------------------------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --------------------------------------------------
# 14. Student input
# --------------------------------------------------

prompt = st.chat_input("Type your question here...")

if prompt:
    # Display and save the student's message.
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # --------------------------------------------------
    # 15. Generate a response using Gemini
    # --------------------------------------------------

    with st.chat_message("assistant"):
        with st.spinner("Your AI study assistant is thinking..."):
            try:
                contextual_prompt = (
                    f"The student's selected subject is: {subject}.\n"
                    f"Student's question: {prompt}"
                )

                response = st.session_state.chat.send_message(
                    contextual_prompt
                )

                answer = response.text

                if not answer:
                    answer = (
                        "Sorry, I couldn't generate a response. "
                        "Please try asking your question differently."
                    )

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as error:
                answer = (
                    "I couldn't reach the study assistant just now. "
                    "Please check the connection and try again."
                )
                st.error(
                    "The study assistant couldn't get a response from Gemini. "
                    "Please try again in a moment."
                )
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )
                print(f"Gemini API error: {type(error).__name__}")