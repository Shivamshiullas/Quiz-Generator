import streamlit as st
from gemini_api import ask_gemini_mcq_generation

st.set_page_config(page_title="Quiz Generator", layout="centered")

st.markdown(
    """
    <style>
    .stApp { background-color: #0b0b0b; color: #f1f1f1; }
    .question-box { background-color: #121212; padding: 12px; border-radius: 8px; margin-bottom: 12px; border: 1px solid #222; }
    .result-correct { color: #7CFC00; font-weight: 600; }
    .result-wrong { color: #ff6b6b; font-weight: 600; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Quiz Generator")
st.write("Upload a .txt file containing notes.")
if "quiz" not in st.session_state:
    st.session_state.quiz = None
if "source_name" not in st.session_state:
    st.session_state.source_name = None

uploaded_file = st.file_uploader("Upload file(.txt)",type=["txt"])

if uploaded_file is not None:
    raw_text = uploaded_file.getvalue().decode("utf-8", errors="ignore")
    if st.session_state.source_name != uploaded_file.name or st.session_state.quiz is None:
        with st.spinner("Generating quiz questions"):
            quiz = ask_gemini_mcq_generation(raw_text)
        for q in quiz:
            q["options"] = ["All of these"] + q["options"]

        st.session_state.quiz = quiz
        st.session_state.source_name = uploaded_file.name
if st.session_state.quiz:
    quiz = st.session_state.quiz
    st.success(f"Quiz generated from: **{st.session_state.source_name}**")
    st.write("---")

    for i, q in enumerate(quiz):
        with st.container():
            st.markdown(
                f"<div class='question-box'><strong>Q{i+1}.</strong> {q['question']}</div>",
                unsafe_allow_html=True
            )
            st.radio(
                label=f"Choose answer for Q{i+1}",
                options=q["options"],
                index=0,
                key=f"answer_{i}"
            )

    st.write("---")
    if st.button("Submit"):
        score = 0
        st.write("Results")

        for i, q in enumerate(quiz):
            user_input = st.session_state.get(f"answer_{i}", "")
            correct = q["answer"]

            if user_input == "All of these" or not user_input:
                st.markdown(
                    f"Q{i+1}: <span class='result-wrong'>Not answered</span>",
                    unsafe_allow_html=True
                )
                continue
            if user_input.strip().lower() == correct.strip().lower():
                score += 1
                st.markdown(
                    f"Q{i+1}: <span class='result-correct'>Correct Answer</span> — Your answer: {user_input}",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"Q{i+1}: <span class='result-wrong'>Wrong Answer</span> — Your answer: {user_input} — Correct answer: {correct}",
                    unsafe_allow_html=True
                )

        st.info(f"**Total Score: {score} / {len(quiz)}**")

else:
    st.info("Upload a .txt file to generate a quiz.")
