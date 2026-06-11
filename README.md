---
title: AI Question Generator
emoji: 🎓
colorFrom: purple
colorTo: pink
sdk: streamlit
sdk_version: "1.45.0"
app_file: app.py
pinned: false
---

# 🎓 AI Question Generator

### Generate high-quality quiz questions instantly using AI — powered by LLaMA 3.3 70B via Groq

[![Live Demo](https://img.shields.io/badge/🤗%20Hugging%20Face-Live%20Demo-yellow?style=for-the-badge)](https://huggingface.co/spaces/RTAAI/ai-question-generator)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.45-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3%2070B-412991?style=for-the-badge)](https://groq.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## 📌 Overview

**AI Question Generator** is an intelligent web application that allows educators, students, and content creators to instantly generate customized questions on any topic. It uses the **LLaMA 3.3 70B** model via the **Groq API** for ultra-fast inference, wrapped in a polished **Streamlit** interface.

Whether you're preparing an exam, a quiz night, or self-study material — just enter a topic and get well-structured questions in seconds.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 **3 Question Types** | MCQs (with 4 options), True/False statements, and Short Descriptive questions |
| 🎯 **Difficulty Control** | Choose between Easy, Medium, and Hard levels |
| 🎒 **Grade Level Selector** | Adjust complexity for Primary, Middle School, High School, A Level/FSc, University, or Professional |
| 📚 **Subject Selection** | Choose from General, Science, Mathematics, History, Programming, Business, Medicine, Literature, or Geography |
| 🌍 **Multi-language Support** | Generate questions in English, Urdu, Arabic, French, or Spanish |
| 🔢 **Custom Count** | Generate anywhere from 1 to 20 questions at a time |
| ⚡ **Fast Inference** | Powered by Groq's ultra-low latency LLaMA 3.3 70B model |
| ✅ **Auto Answer Keys** | MCQs and True/False include correct answers; Descriptive includes model answers |
| 📋 **Session History** | All generated sets are saved in-session with full content, grade, and metadata |
| 📥 **TXT Export** | Download any question set as a plain text file |
| 📄 **PDF Export** | Download any question set as a formatted PDF |
| 📊 **Live Stats** | Dashboard shows total questions generated and session count |
| 🌐 **Live Web App** | Deployed on Hugging Face Spaces — no installation required |

---

## 🖥️ Demo

> 🚀 Try it live: **[Open on Hugging Face →](https://huggingface.co/spaces/RTAAI/ai-question-generator)**

**Example Input:**
- Topic: `Photosynthesis`
- Subject: `Science`
- Grade Level: `Grade 9-10 (High School)`
- Type: `MCQs`
- Difficulty: `Medium`
- Language: `English`
- Count: `5`

**Example Output:**
```
1. What is the primary pigment responsible for capturing light energy in photosynthesis?
   A) Carotenoid   B) Chlorophyll   C) Xanthophyll   D) Anthocyanin
   ✅ Correct Answer: B)

2. In which part of the chloroplast does the Calvin cycle take place?
   A) Thylakoid membrane   B) Outer membrane   C) Stroma   D) Granum
   ✅ Correct Answer: C)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend & UI | Streamlit 1.45 |
| LLM Backend | LLaMA 3.3 70B Versatile via Groq API |
| PDF Generation | FPDF2 |
| Language | Python 3.9+ |
| Deployment | Hugging Face Spaces |

---

## 📁 Project Structure

```
ai-question-generator/
│
├── app.py              # Main application — Streamlit UI + Groq API logic
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## 🚀 Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/rta-ai/ai-question-generator.git
cd ai-question-generator
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set your Groq API key**

Get your free API key from [console.groq.com](https://console.groq.com)

```bash
# Linux / macOS
export fb_ai="your_groq_api_key_here"

# Windows (Command Prompt)
set fb_ai=your_groq_api_key_here

# Windows (PowerShell)
$env:fb_ai="your_groq_api_key_here"
```

Or create a `.env` file in the project root:
```
fb_ai=your_groq_api_key_here
```

**4. Launch the app**
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`

---

## ☁️ Deploy to Hugging Face Spaces

1. Create a new Space at [huggingface.co/new-space](https://huggingface.co/new-space)
2. Set SDK to **Streamlit**
3. Push your code:
```bash
git remote add space https://huggingface.co/spaces/RTAAI/ai-question-generator
git push space main
```
4. Go to **Settings → Variables and Secrets** → add `fb_ai` as a secret with your Groq API key

---

## ⚙️ How It Works

```
User Input (topic + subject + grade level + settings)
        ↓
Streamlit Sidebar (app.py)
        ↓
Prompt Engineering (type + difficulty + grade-level instructions)
        ↓
Groq API → LLaMA 3.3 70B Versatile
        ↓
Formatted Output (numbered questions + answer keys)
        ↓
Displayed in Streamlit UI
        ↓
Export as TXT or PDF
```

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙋 Author

**Muhammad Tayyab**
- GitHub: [@rta-ai](https://github.com/rta-ai)
- Hugging Face: [@RTAAI](https://huggingface.co/RTAAI)

---

> ⭐ If you found this useful, please **star the repository!**
