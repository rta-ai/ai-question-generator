import os
import re
import json
import tempfile
import streamlit.components.v1 as components
import streamlit as st
from groq import Groq
from fpdf import FPDF
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ─── Page Config ────────────────────────────────────────────
st.set_page_config(
    page_title="AI Question Generator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Full Custom CSS ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

/* ── Global ── */
*, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #f5f0ff 0%, #fff0f5 50%, #f0f8ff 100%);
}

/* ── Hide Streamlit Branding ── */
#MainMenu {display: none !important;}
footer {display: none !important;}
[data-testid="stToolbar"] {display: none !important;}

/* ── Hero Header ── */
.hero {
    background: linear-gradient(135deg, #667eea 0%, #f093fb 50%, #f5576c 100%);
    padding: 2.5rem 2rem;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
    animation: shimmer 4s infinite;
}

@keyframes shimmer {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.hero h1 {
    color: white !important;
    font-size: 2.8rem !important;
    font-weight: 700 !important;
    margin: 0 !important;
    text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    letter-spacing: -0.5px;
}

.hero p {
    color: rgba(255,255,255,0.9) !important;
    font-size: 1.1rem !important;
    margin: 0.5rem 0 0 0 !important;
    font-weight: 400;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2d1b69 0%, #11998e 100%) !important;
    border-right: none !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div:not([data-testid="collapsedControl"]) > p {
    color: white !important;
}

[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stTextInput label {
    color: rgba(255,255,255,0.9) !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stSelectbox select {
    background: rgba(255,255,255,0.15) !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    border-radius: 10px !important;
    color: white !important;
}

/* ── Sidebar Logo Area ── */
.sidebar-logo {
    text-align: center;
    padding: 1.5rem 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.2);
    margin-bottom: 1.5rem;
}

.sidebar-logo h2 {
    color: white !important;
    font-size: 1.3rem !important;
    font-weight: 600 !important;
    margin: 0.5rem 0 0 0;
}

.sidebar-logo p {
    color: rgba(255,255,255,0.7) !important;
    font-size: 0.8rem !important;
    margin: 0;
}

/* ── Generate Button ── */
.stButton > button {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
    color: white !important;
    border: none !important;
    padding: 0.8rem 2rem !important;
    border-radius: 50px !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    width: 100% !important;
    letter-spacing: 0.5px !important;
    box-shadow: 0 8px 25px rgba(245, 87, 108, 0.4) !important;
    transition: all 0.3s ease !important;
    margin-top: 1rem !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 35px rgba(245, 87, 108, 0.5) !important;
}

/* ── Stats Cards ── */
.stats-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
}

.stat-card {
    flex: 1;
    background: white;
    border-radius: 16px;
    padding: 1.2rem;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    border-top: 4px solid;
}

.stat-card.purple { border-color: #667eea; }
.stat-card.pink   { border-color: #f093fb; }
.stat-card.red    { border-color: #f5576c; }
.stat-card.teal   { border-color: #11998e; }

.stat-card .stat-number {
    font-size: 1.8rem;
    font-weight: 700;
    color: #2d1b69;
}

.stat-card .stat-label {
    font-size: 0.75rem;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 0.2rem;
}

/* ── Output Card ── */
.output-card {
    background: white;
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 10px 40px rgba(0,0,0,0.08);
    border-left: 5px solid #667eea;
    margin-top: 1rem;
    line-height: 1.8;
    color: #1a1a1a !important;
}

/* ── Generated Questions Text ── */
.stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown ol, .stMarkdown ul,
[data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
    color: #1a1a1a !important;
}

.output-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 2px dashed #f0f0f0;
}

.output-header h3 {
    color: #2d1b69;
    margin: 0;
    font-size: 1.1rem;
}

/* ── Tab Styling ── */
.stTabs [data-baseweb="tab-list"] {
    background: white;
    border-radius: 50px;
    padding: 0.3rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    gap: 0.2rem;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 50px !important;
    padding: 0.5rem 1.5rem !important;
    font-weight: 500 !important;
    color: #666 !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #667eea, #f5576c) !important;
    color: white !important;
}

/* ── History Cards ── */
.history-card {
    background: white;
    border-radius: 12px;
    padding: 1rem 1.5rem;
    margin-bottom: 0.8rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
    border-left: 4px solid #667eea;
}

/* ── Empty State ── */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: #aaa;
}

.empty-state .icon {
    font-size: 4rem;
    margin-bottom: 1rem;
}

.empty-state h3 {
    color: #bbb;
    font-weight: 500;
}

/* ── Sidebar Toggle — Fully Visible ── */
[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    position: fixed !important;
    left: 0 !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
    z-index: 999999 !important;
    background: linear-gradient(135deg, #2d1b69 0%, #11998e 100%) !important;
    border-radius: 0 16px 16px 0 !important;
    width: 28px !important;
    height: 64px !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 4px 0 20px rgba(45,27,105,0.5) !important;
    cursor: pointer !important;
    border: none !important;
}

[data-testid="collapsedControl"] svg {
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    fill: white !important;
    color: white !important;
    width: 16px !important;
    height: 16px !important;
    stroke: white !important;
}

[data-testid="collapsedControl"]:hover {
    width: 34px !important;
    box-shadow: 6px 0 25px rgba(45,27,105,0.7) !important;
    transition: all 0.2s ease !important;
}

[data-testid="stDownloadButton"] button {
    background: linear-gradient(135deg, #667eea, #11998e) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 0.6rem 2rem !important;
    font-weight: 600 !important;
    width: 100% !important;
    box-shadow: 0 4px 15px rgba(102,126,234,0.4) !important;
}
[data-testid="stDownloadButton"] button:hover {
    opacity: 0.9 !important;
    transform: translateY(-2px) !important;
}

/* ── Badge ── */
.badge {
    display: inline-block;
    padding: 0.2rem 0.8rem;
    border-radius: 50px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-right: 0.3rem;
}

.badge-purple { background: #f0eeff; color: #667eea; }
.badge-pink   { background: #fff0fb; color: #f093fb; }
.badge-red    { background: #fff0f2; color: #f5576c; }

/* ── Answer Key Toggle ── */
.answer-key-on {
    background: #f0fff4;
    border: 1px solid #38ef7d;
    border-radius: 10px;
    padding: 0.4rem 1rem;
    color: #11998e;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 1rem;
    display: inline-block;
}
.answer-key-off {
    background: #fff0f0;
    border: 1px solid #f5576c;
    border-radius: 10px;
    padding: 0.4rem 1rem;
    color: #f5576c;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 1rem;
    display: inline-block;
}

/* ── Print Button ── */
.print-btn {
    background: linear-gradient(135deg, #11998e, #38ef7d) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 0.6rem 2rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    width: 100% !important;
    cursor: pointer !important;
    box-shadow: 0 4px 15px rgba(17,153,142,0.4) !important;
    margin-top: 0.5rem !important;
    transition: all 0.3s ease !important;
}
.print-btn:hover {
    opacity: 0.9 !important;
    transform: translateY(-2px) !important;
}

/* ── Print Mode — hide everything except questions ── */
@media print {
    [data-testid="stSidebar"],
    [data-testid="stToolbar"],
    [data-testid="stDownloadButton"],
    .hero,
    .stats-row,
    .stTabs,
    .stButton,
    .print-btn,
    footer,
    #MainMenu { display: none !important; }

    .output-card {
        box-shadow: none !important;
        border: none !important;
        padding: 0 !important;
    }

    body { background: white !important; }
}

</style>
""", unsafe_allow_html=True)

# ─── API Setup ───────────────────────────────────────────────
GROQ_API_KEY = os.environ.get("fb_ai")
if not GROQ_API_KEY:
    st.error("⚠️ Groq API Key not found. Add it as Space Secret named 'fb_ai'.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# ─── Session State ───────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "total_generated" not in st.session_state:
    st.session_state.total_generated = 0
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "last_topic" not in st.session_state:
    st.session_state.last_topic = ""
if "show_answers" not in st.session_state:
    st.session_state.show_answers = True

# ─── Generator Function ──────────────────────────────────────
def generate_questions(topic, num_questions, difficulty, question_type, subject, language, grade_level):
    if question_type == "MCQs":
        type_instructions = """
        - Each question must have exactly 4 options labeled A), B), C), D).
        - Clearly mark the correct answer like: ✅ Correct Answer: B)
        - Make distractors plausible but clearly incorrect.
        """
    elif question_type == "True/False":
        type_instructions = """
        - Each question must be a clear True or False statement.
        - Mark the answer like: ✅ Answer: True / False
        """
    else:
        type_instructions = """
        - Each question should require a 2-5 sentence answer.
        - Provide a model answer like: 💡 Model Answer: ...
        """

    prompt = f"""
    Generate {num_questions} high-quality {difficulty} level {question_type}
    questions about "{topic}" in the subject of {subject}.
    Respond in {language}.
    Adjust complexity and vocabulary for {grade_level} students.
    - Number questions properly (1., 2., 3.)
    - Be clear and educational
    - Avoid repetition
    {type_instructions}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an expert teacher and exam paper setter."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return re.sub(r'\n{3,}', '\n\n',
                  response.choices[0].message.content.strip())

def export_pdf(content, topic):
    import re

    def clean(text):
        # Remove emojis and non-latin characters
        return re.sub(
            r'[^\x00-\x7F\u00C0-\u024F]+', 
            '', 
            text
        ).strip()

    pdf = FPDF()
    pdf.add_page()

    # Header
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, clean(f"Questions: {topic}"), ln=True, align="C")
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)

    # Content
    pdf.set_font("Helvetica", "", 11)
    for line in content.split("\n"):
        cleaned = clean(line)
        if cleaned:
            pdf.multi_cell(0, 8, cleaned)
            pdf.ln(1)

    path = os.path.join(tempfile.gettempdir(), f"questions_{topic.replace(' ', '_')}.pdf")
    pdf.output(path)
    return path

def strip_answers(content):
    lines = content.split("\n")
    cleaned = []
    for line in lines:
        if re.search(
            r'(correct answer|answer key|model answer'
            r'|answer:|true|false|✅|💡)',
            line.strip(),
            re.IGNORECASE
        ):
            continue
        cleaned.append(line)
    return "\n".join(cleaned)

# ─── Sidebar ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div style="font-size:3rem">🎓</div>
        <h2>Question Generator</h2>
        <p>Powered by Groq AI</p>
    </div>
    """, unsafe_allow_html=True)

    topic = st.text_input("📚 Topic", placeholder="e.g. Photosynthesis")

    subject = st.selectbox("🎯 Subject", [
        "General", "Science", "Mathematics",
        "History", "Programming", "Business",
        "Medicine", "Literature", "Geography"
    ])

    grade_level = st.selectbox("🎒 Grade Level", [
        "Grade 1-5 (Primary)",
        "Grade 6-8 (Middle School)",
        "Grade 9-10 (High School)",
        "Grade 11-12 (A Level / FSc)",
        "University",
        "Professional"
    ])

    language = st.selectbox("🌍 Language", [
        "English", "Urdu", "Arabic", "French", "Spanish"
    ])

    col1, col2 = st.columns(2)
    with col1:
        difficulty = st.selectbox("📊 Level", ["Easy", "Medium", "Hard"])
    with col2:
        question_type = st.selectbox("📝 Type", [
            "MCQs", "True/False", "Short Descriptive"
        ])

    num_questions = st.slider("🔢 Questions", 1, 20, 5)

    generate_btn = st.button("✨ Generate Questions")

    st.markdown("---")
    st.markdown(
        "<p style='text-align:center; color:rgba(255,255,255,0.5);"
        "font-size:0.75rem'>Built with ❤️ Muhammad Tayyab</p>",
        unsafe_allow_html=True
    )

# ─── Main Panel ──────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🎓 AI Question Generator</h1>
    <p>Create professional exam questions for your classroom in seconds</p>
</div>
""", unsafe_allow_html=True)

# Stats Row
total = st.session_state.total_generated
sessions = len(st.session_state.history)
st.markdown(f"""
<div class="stats-row">
    <div class="stat-card purple">
        <div class="stat-number">{total}</div>
        <div class="stat-label">Questions Generated</div>
    </div>
    <div class="stat-card pink">
        <div class="stat-number">{sessions}</div>
        <div class="stat-label">Sessions</div>
    </div>
    <div class="stat-card red">
        <div class="stat-number">5</div>
        <div class="stat-label">Question Types</div>
    </div>
    <div class="stat-card teal">
        <div class="stat-number">3</div>
        <div class="stat-label">Difficulty Levels</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2 = st.tabs(["✨  Generate", "📋  History"])

with tab1:
    if generate_btn:
        if not topic.strip():
            st.warning("⚠️ Please enter a topic in the sidebar first.")
        else:
            with st.spinner("🤖 Generating your questions..."):
                try:
                    result = generate_questions(
                        topic, num_questions, difficulty,
                        question_type, subject, language, grade_level
                    )
                    st.session_state.last_result = result
                    st.session_state.last_topic = topic
                    st.session_state.total_generated += num_questions
                    st.session_state.history.append({
                        "topic": topic,
                        "type": question_type,
                        "difficulty": difficulty,
                        "subject": subject,
                        "grade": grade_level,
                        "count": num_questions,
                        "content": result
                    })
                    st.session_state.show_answers = True
                    st.success("✅ Questions generated successfully!")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

    if st.session_state.last_result:
        st.markdown(f"""
        <div class="output-card">
            <div class="output-header">
                <span>📄</span>
                <h3>{st.session_state.last_topic}</h3>
                <span class="badge badge-purple">{difficulty}</span>
                <span class="badge badge-pink">{question_type}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_toggle1, col_toggle2 = st.columns([1, 3])
        with col_toggle1:
            show_answers = st.toggle(
                "Show Answer Key",
                value=st.session_state.show_answers,
                key="answer_toggle"
            )
            st.session_state.show_answers = show_answers
        with col_toggle2:
            if show_answers:
                st.markdown(
                    '<span class="answer-key-on">'
                    '✅ Answer Key Visible — Teacher Mode'
                    '</span>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    '<span class="answer-key-off">'
                    '📝 Answers Hidden — Student Mode'
                    '</span>',
                    unsafe_allow_html=True
                )

        display_content = (
            st.session_state.last_result
            if show_answers
            else strip_answers(st.session_state.last_result)
        )

        st.markdown(display_content)

        st.divider()
        col_dl1, col_dl2, col_dl3 = st.columns(3)
        with col_dl1:
            st.download_button(
                label="📥 Download TXT",
                data=display_content,
                file_name=f"questions_{topic.replace(' ','_')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        with col_dl2:
            pdf_path = export_pdf(
                display_content,
                st.session_state.last_topic
            )
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📄 Download PDF",
                    data=f,
                    file_name=f"questions_{st.session_state.last_topic.replace(' ','_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        with col_dl3:
            _content_js = json.dumps(display_content)
            _topic_js = json.dumps(st.session_state.last_topic)
            components.html(f"""
<style>
button {{
    background: linear-gradient(135deg, #11998e, #38ef7d);
    color: white;
    border: none;
    border-radius: 50px;
    padding: 0.6rem 2rem;
    font-size: 1rem;
    font-weight: 600;
    width: 100%;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(17,153,142,0.4);
    transition: all 0.3s ease;
    font-family: 'Poppins', sans-serif;
}}
button:hover {{ opacity: 0.9; transform: translateY(-2px); }}
</style>
<button onclick="doPrint()">🖨️ Print</button>
<script>
var content = {_content_js};
var topic = {_topic_js};
function doPrint() {{
    var w = window.open('', '_blank');
    w.document.write('<!DOCTYPE html><html><head><title>' + topic + '</title>'
        + '<style>body{{font-family:Arial,sans-serif;padding:2rem;line-height:1.8;color:#1a1a1a}}'
        + 'h2{{color:#2d1b69;margin-bottom:1rem}}pre{{white-space:pre-wrap;word-wrap:break-word}}'
        + '</style></head><body>'
        + '<h2>Questions: ' + topic + '</h2>'
        + '<pre>' + content + '</pre>'
        + '</body></html>');
    w.document.close();
    w.focus();
    w.print();
}}
</script>
""", height=55)
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="icon">📝</div>
            <h3>No questions yet</h3>
            <p>Fill in the settings on the left and hit Generate</p>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    if not st.session_state.history:
        st.markdown("""
        <div class="empty-state">
            <div class="icon">📋</div>
            <h3>No history yet</h3>
            <p>Your generated question sets will appear here</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(
                f"**{len(st.session_state.history)} session(s)** in history"
            )
        with col2:
            if st.button("🗑️ Clear All"):
                st.session_state.history = []
                st.rerun()

        for i, item in enumerate(reversed(st.session_state.history)):
            with st.expander(
                f"📄 {item['topic']} | "
                f"{item['type']} | "
                f"{item['difficulty']} | "
                f"{item.get('grade', 'N/A')} | "
                f"{item['count']} questions"
            ):
                st.markdown(item["content"])
                st.download_button(
                    label="📥 Download",
                    data=item["content"],
                    file_name=f"questions_{item['topic'].replace(' ','_')}.txt",
                    mime="text/plain",
                    key=f"dl_{i}"
                )