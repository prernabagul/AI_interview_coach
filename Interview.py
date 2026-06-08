
import streamlit as st
import google.generativeai as genai
from resume_parser import extract_resume_text
from database import (
    create_db,
    save_interviews,
    get_interviews,
    total_interviews
)

from dotenv import load_dotenv
import os 

create_db() 
# -----------------------------
# Gemini Configuration
# -----------------------------
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

st.write("API loaded:", API_KEY is not None)
st.write("First 5 chars:", API_KEY[:5] if API_KEY else "None")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-3.1-flash-lite")

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🎯 AI Interview Coach")

role = st.selectbox(
    "Select Job Role",
    [
        "Data Analyst",
        "Python Developer",
        "AI Engineer",
        "Web Developer",
        "Software Engineer",
        "average score"
    ]
)

total = total_interviews()

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Total Interviews",
        total
    )

with col2:
    difficulty = st.selectbox(
    "Select Difficulty",
    ["Easy", "Medium", "Hard"]
)

uploaded_resume = st.file_uploader(
    "Upload Your Resume",
    type=["pdf"]
)
resume_text = ""

if uploaded_resume:
    resume_text = extract_resume_text(uploaded_resume)

    st.success("Resume uploaded successfully!")
# -----------------------------
# Generate Question
# -----------------------------
if st.button("Generate Questions"):

  prompt = f"""
  You are a professional interviewer.

  Job Role:
  {role}

  Candidate Resume:
  {resume_text}

  Generate 5 interview questions.

  Difficulty Level:
  {difficulty}

  If difficulty is Easy:
  - Ask basic concepts and definitions.

  If difficulty is Medium:
  - Ask practical and project-based questions.

  If difficulty is Hard:
  - Ask advanced scenario-based and problem-solving questions.

  If resume information exists,
  generate questions based on the resume.

  Otherwise generate general interview questions.

  Return them as a numbered list.
  Return only the questions.
  """
  try:
    response = model.generate_content(prompt)

    st.session_state.questions = [
        q.strip()
        for q in response.text.split("\n")
        if q.strip()
    ]

  except Exception as e:
    st.error(f"Gemini Error: {e}")

# Display Questions

if "questions" in st.session_state:

    answers = []

    st.subheader("Interview Questions")

    for i, question in enumerate(st.session_state.questions):

        st.write(question)

        answer = st.text_area(
            f"Answer {i+1}",
            key=f"answer_{i}"
        )

        answers.append(answer)

    submit = st.button("Submit Interview")

    # -----------------------------
    # Evaluate Answer
    # -----------------------------
    if st.button("Evaluate Answer"):

        evaluation_prompt = f"""
        You are an experienced interviewer.

        Interview Question:
        {st.session_state.questions}

        Candidate Answer:
        {answer}

        Evaluate:

        1. Technical Accuracy (out of 10)
        2. Clarity (out of 10)
        3. Completeness (out of 10)

        Then provide:
        - Strengths
        - Areas for Improvement
        - Overall Feedback

        Format the response neatly.
        """

        evaluation = model.generate_content(
            evaluation_prompt
        )

        st.subheader("Feedback")

        st.write(evaluation.text)

        save_interviews(
             role,
             evaluation.text
        )
        st.success("Interview saved!")

st.header("Interview History")

history = get_interviews()

for row in history:

    st.write(
        f"Interview ID: {row[0]}"
    )

    st.write(
        f"Role: {row[1]}"
    )

    st.write(
        row[3]
    )

    st.divider()