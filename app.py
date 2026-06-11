import os
import re
import streamlit as st
from groq import Groq

GROQ_API_KEY = os.environ.get("fb_ai")

if not GROQ_API_KEY:
    st.error("Groq API Key not found. Please add it as a Space Secret named 'fb_ai'.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

st.markdown("""
<style>
.header {
    background: linear-gradient(90deg, #1a1a2e, #16213e);
    padding: 1.5rem 2rem;
    border-radius: 12px;
    margin-bottom: 1.5rem;
    text-align: center;
}
.header h1 { color: #e0e0ff; margin: 0; font-size: 2rem; }
.header p  { color: #a0a0cc; margin: 0.4rem 0 0; font-size: 1rem; }
</style>
<div class="header">
  <h1>🤖 AI Question Generator</h1>
  <p>Enter any topic and generate AI-based questions instantly.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Settings")
    topic = st.text_input("Enter Topic", placeholder="Example: Artificial Intelligence")
    num_questions = st.slider("Number of Questions", min_value=1, max_value=20, value=5, step=1)
    difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"], index=1)
    question_type = st.selectbox("Question Type", ["MCQs", "True/False", "Short Descriptive"])
    generate_btn = st.button("Generate Questions", use_container_width=True)

def generate_questions(topic, num_questions, difficulty, question_type):
    if question_type == "MCQs":
        type_instructions = """
    - Each question must have exactly 4 options labeled A), B), C), D).
    - Clearly mark the correct answer at the end of each question like: ✅ Correct Answer: B)
    - Make sure distractors (wrong options) are plausible but clearly incorrect.
        """
    elif question_type == "True/False":
        type_instructions = """
    - Each question must be a statement that is either True or False.
    - Clearly mark the correct answer at the end of each question like: ✅ Answer: True / False
    - Statements should be unambiguous and factual.
        """
    elif question_type == "Short Descriptive":
        type_instructions = """
    - Each question should require a short written answer (2-5 sentences).
    - Questions should be open-ended and thought-provoking.
    - Provide a brief model answer after each question like: 💡 Model Answer: ...
        """
    else:
        type_instructions = ""

    prompt = f"""
    Generate {num_questions} high-quality {difficulty} level {question_type} questions about the topic: "{topic}".

    Instructions:
    - Questions should be clear and educational.
    - Number them properly (1., 2., 3. ...).
    - Avoid repeating questions.
    - Cover important aspects of the topic.
    {type_instructions}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an expert teacher and question paper setter."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    output = response.choices[0].message.content.strip()
    return re.sub(r'\n{3,}', '\n\n', output)

if generate_btn:
    if not topic.strip():
        st.warning("Please enter a topic.")
    else:
        with st.spinner("Generating questions..."):
            try:
                result = generate_questions(topic, num_questions, difficulty, question_type)
                st.text_area("Generated Questions", value=result, height=500)
            except Exception as e:
                st.error(f"Error: {str(e)}")
