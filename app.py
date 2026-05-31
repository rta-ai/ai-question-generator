import os
import re
import gradio as gr
from groq import Groq

# ---------------------------
# Load API Key from Environment (HF Secrets)
# ---------------------------
GROQ_API_KEY = os.environ.get("fb_ai")

if not GROQ_API_KEY:
    raise ValueError("Groq API Key not found. Please add it as a Space Secret named 'fb_ai'.")

# ---------------------------
# Initialize Groq Client
# ---------------------------
client = Groq(api_key=GROQ_API_KEY)

# ---------------------------
# AI Question Generator Function
# ---------------------------
def generate_questions(topic, num_questions, difficulty, question_type):
    try:
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
        output = re.sub(r'\n{3,}', '\n\n', output)
        return output

    except Exception as e:
        return f"Error: {str(e)}"

# ---------------------------
# Gradio Interface
# ---------------------------
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🤖 AI Question Generator")
    gr.Markdown("Enter any topic and generate AI-based questions instantly.")

    with gr.Row():
        topic = gr.Textbox(
            label="Enter Topic",
            placeholder="Example: Artificial Intelligence"
        )

    with gr.Row():
        num_questions = gr.Slider(
            minimum=1,
            maximum=20,
            value=5,
            step=1,
            label="Number of Questions"
        )

        difficulty = gr.Dropdown(
            choices=["Easy", "Medium", "Hard"],
            value="Medium",
            label="Difficulty Level"
        )

        question_type = gr.Dropdown(
            choices=["MCQs", "True/False", "Short Descriptive"],
            value="MCQs",
            label="Question Type"
        )

    generate_btn = gr.Button("Generate Questions")

    output = gr.Textbox(
        label="Generated Questions",
        lines=15
    )

    generate_btn.click(
        fn=generate_questions,
        inputs=[topic, num_questions, difficulty, question_type],
        outputs=output
    )

demo.launch()