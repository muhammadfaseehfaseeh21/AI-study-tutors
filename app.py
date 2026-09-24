import streamlit as st
from groq import Groq

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
MODEL_NAME = "openai/gpt-oss-120b"

st.set_page_config(
    page_title="AI Study Tutor",
    page_icon="📚",
    layout="wide",
)

# ---------------------------------------------------------
# STYLING (gradient theme, feature cards, styled response box)
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #1f1147 0%, #3b1573 50%, #6b21a8 100%);
        color: #f5f3ff;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2a0e5e 0%, #4c1d95 100%);
    }
    .feature-card {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 10px;
    }
    .response-box {
        background: rgba(255, 255, 255, 0.08);
        border-left: 5px solid #a855f7;
        border-radius: 10px;
        padding: 20px;
        margin-top: 15px;
        line-height: 1.6;
    }
    div.stButton > button {
        background: linear-gradient(90deg, #7c3aed, #a855f7);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6em 1.2em;
        font-weight: 600;
    }
    div.stButton > button:hover {
        background: linear-gradient(90deg, #6d28d9, #9333ea);
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# GROQ CLIENT (API key read from Streamlit Secrets only)
# ---------------------------------------------------------
@st.cache_resource
def get_client():
    api_key = st.secrets["GROQ_API_KEY"]
    return Groq(api_key=api_key)


def ask_tutor(system_prompt: str, user_prompt: str, temperature: float = 0.5) -> str:
    """Send a prompt to the Groq model and return the plain text reply."""
    client = get_client()
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
    )
    return response.choices[0].message.content


# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
st.sidebar.title("📚 AI Study Tutor")
st.sidebar.write("Your personal AI-powered study companion.")

tool = st.sidebar.radio(
    "Choose a tool",
    [
        "🧠 Explain a Concept",
        "❓ Quiz Me",
        "🗂️ Flashcards",
        "📅 Study Plan",
        "💬 Ask a Doubt",
    ],
)

st.sidebar.markdown("---")
st.sidebar.caption(f"Powered by Groq · Model: `{MODEL_NAME}`")

st.title("AI Study Tutor")
st.write("Learn faster with an AI tutor that explains, quizzes, and plans your studies.")

# ---------------------------------------------------------
# TOOL 1: EXPLAIN A CONCEPT
# ---------------------------------------------------------
if tool == "🧠 Explain a Concept":
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("🧠 Explain a Concept")
    topic = st.text_input("What topic or concept do you want explained?")
    level = st.selectbox(
        "Explain it like I'm a...",
        ["Complete Beginner", "High School Student", "College Student", "Expert"],
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Explain", key="explain_btn"):
        if not topic.strip():
            st.warning("Please enter a topic first.")
        else:
            with st.spinner("Thinking..."):
                system_prompt = (
                    "You are a friendly, patient study tutor. Explain concepts clearly, "
                    "using simple language, short paragraphs, and a helpful example. "
                    f"Tailor the explanation for a {level} level."
                )
                answer = ask_tutor(system_prompt, f"Explain this topic: {topic}")
            st.markdown(f'<div class="response-box">{answer}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# TOOL 2: QUIZ ME
# ---------------------------------------------------------
elif tool == "❓ Quiz Me":
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("❓ Quiz Me")
    topic = st.text_input("What topic should the quiz be about?")
    num_q = st.slider("Number of questions", 3, 10, 5)
    difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Generate Quiz", key="quiz_btn"):
        if not topic.strip():
            st.warning("Please enter a topic first.")
        else:
            with st.spinner("Writing quiz questions..."):
                system_prompt = (
                    "You are a study tutor creating a quiz. Write clear multiple-choice "
                    "questions with 4 options each (A-D). After ALL questions, add a section "
                    "titled 'Answer Key' listing the correct letter for each question."
                )
                user_prompt = (
                    f"Create a {difficulty.lower()} difficulty quiz with {num_q} multiple-choice "
                    f"questions about: {topic}"
                )
                answer = ask_tutor(system_prompt, user_prompt)
            st.markdown(f'<div class="response-box">{answer}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# TOOL 3: FLASHCARDS
# ---------------------------------------------------------
elif tool == "🗂️ Flashcards":
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("🗂️ Flashcards")
    topic = st.text_input("What topic do you want flashcards for?")
    num_cards = st.slider("Number of flashcards", 3, 15, 8)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Generate Flashcards", key="flash_btn"):
        if not topic.strip():
            st.warning("Please enter a topic first.")
        else:
            with st.spinner("Making flashcards..."):
                system_prompt = (
                    "You are a study tutor making flashcards. For each flashcard, output in "
                    "this exact format:\n\nCard N\nFront: <short question or term>\n"
                    "Back: <concise answer or definition>\n\nKeep fronts short and backs concise."
                )
                answer = ask_tutor(
                    system_prompt, f"Create {num_cards} flashcards about: {topic}"
                )
            st.markdown(f'<div class="response-box">{answer}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# TOOL 4: STUDY PLAN
# ---------------------------------------------------------
elif tool == "📅 Study Plan":
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("📅 Study Plan")
    subject = st.text_input("Subject or exam you're preparing for")
    days = st.number_input("Number of days until your exam/deadline", min_value=1, max_value=90, value=7)
    hours = st.number_input("Hours you can study per day", min_value=1, max_value=12, value=2)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Create Study Plan", key="plan_btn"):
        if not subject.strip():
            st.warning("Please enter a subject first.")
        else:
            with st.spinner("Building your study plan..."):
                system_prompt = (
                    "You are a study tutor creating a day-by-day study plan. Be realistic, "
                    "break topics into manageable daily chunks, and include short breaks and "
                    "a final revision day if possible. Format clearly with a heading per day."
                )
                user_prompt = (
                    f"Subject: {subject}\nDays available: {days}\nHours per day: {hours}\n"
                    "Create a day-by-day study plan."
                )
                answer = ask_tutor(system_prompt, user_prompt)
            st.markdown(f'<div class="response-box">{answer}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# TOOL 5: ASK A DOUBT (free-form chat)
# ---------------------------------------------------------
elif tool == "💬 Ask a Doubt":
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("💬 Ask a Doubt")
    st.write("Ask any study question, big or small.")
    st.markdown("</div>", unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    question = st.chat_input("Type your question here...")
    if question:
        st.session_state.chat_history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                system_prompt = (
                    "You are a patient, encouraging study tutor. Answer the student's "
                    "question clearly and simply, with an example if it helps."
                )
                answer = ask_tutor(system_prompt, question)
                st.write(answer)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
