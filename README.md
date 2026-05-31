<div align="center">
#🤖 AI Question Generator
</div> 
<div align="center">
**Generate high-quality quiz questions instantly using AI — powered by LLaMA 3.3 70B via Groq**
 
[![Live Demo](https://img.shields.io/badge/🤗%20Hugging%20Face-Live%20Demo-yellow?style=for-the-badge)]((https://huggingface.co/spaces/RTAAI/ai-question-generator))
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Gradio](https://img.shields.io/badge/Gradio-6.14-orange?style=for-the-badge&logo=gradio&logoColor=white)](https://www.gradio.app/)
[![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3%2070B-412991?style=for-the-badge)](https://groq.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
 
</div>
---
 
## 📌 Overview
 
**AI Question Generator** is an intelligent web application that allows educators, students, and content creators to instantly generate customized questions on any topic. It uses the **LLaMA 3.3 70B** model via the **Groq API** for ultra-fast inference, wrapped in an intuitive **Gradio** interface.
 
Whether you're preparing an exam, a quiz night, or self-study material — just enter a topic and get well-structured questions in seconds.
 
---
 
## ✨ Features
 
| Feature | Description |
|---|---|
| 🧠 **3 Question Types** | MCQs (with 4 options), True/False statements, and Short Descriptive questions |
| 🎯 **Difficulty Control** | Choose between Easy, Medium, and Hard levels |
| 🔢 **Custom Count** | Generate anywhere from 1 to 20 questions at a time |
| ⚡ **Fast Inference** | Powered by Groq's ultra-low latency LLaMA 3.3 70B model |
| ✅ **Auto Answer Keys** | MCQs and True/False include correct answers; Descriptive includes model answers |
| 🌐 **Live Web App** | Deployed on Hugging Face Spaces — no installation required |
 
---
 
## 🖥️ Demo
 
> Try it live: **[Hugging Face Space →](https://huggingface.co/spaces/rta-ai/ai-question-generator)**
 
**Example Input:**
- Topic: `Photosynthesis`
- Type: `MCQs`
- Difficulty: `Medium`
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
 
```
Frontend & UI  →  Gradio 6.14 (Python-native web UI)
LLM Backend    →  LLaMA 3.3 70B Versatile (via Groq API)
Language       →  Python 3.9+
Deployment     →  Hugging Face Spaces
```
 
---
 
## 📁 Project Structure
 
```
ai-question-generator/
│
├── app.py              # Main application — Gradio UI + Groq API logic
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```
 
---
 
## 🚀 Run Locally
 
### 1. Clone the repository
```bash
git clone https://github.com/rta-ai/ai-question-generator.git
cd ai-question-generator
```
 
### 2. Install dependencies
```bash
pip install -r requirements.txt
```
 
### 3. Set your Groq API key
 
Get your free API key from [console.groq.com](https://console.groq.com)
 
```bash
# Linux / macOS
export fb_ai="your_groq_api_key_here"
 
# Windows (Command Prompt)
set fb_ai=your_groq_api_key_here
 
# Windows (PowerShell)
$env:fb_ai="your_groq_api_key_here"
```
 
### 4. Launch the app
```bash
python app.py
```
 
Open your browser at `http://localhost:7860`
 
---
 
## ☁️ Deploy to Hugging Face Spaces
 
1. Create a new Space at [huggingface.co/new-space](https://huggingface.co/new-space)
2. Set SDK to **Gradio**
3. Push your code:
   ```bash
   git remote add space https://huggingface.co/spaces/rta-ai/ai-question-generator
   git push space main
   ```
4. Go to **Settings → Variables and Secrets** → add `fb_ai` as a secret with your Groq API key
---
 
## ⚙️ How It Works
 
```
User Input (topic + settings)
        ↓
Gradio Interface (app.py)
        ↓
Prompt Engineering (question type + difficulty instructions)
        ↓
Groq API → LLaMA 3.3 70B Versatile
        ↓
Formatted Output (numbered questions + answer keys)
        ↓
Displayed in Gradio Textbox
```
 
---
 
## 📄 License
 
This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
 
---
 
## 🙋‍♂️ Author
 
**Muhammd Tayyab**
- GitHub: [@rta-ai](https://github.com/rta-ai)
- Hugging Face: [@rtaai](https://huggingface.co/rtaai)
---
 
<div align="center">
⭐ **If you found this useful, please star the repository!** ⭐
 
</div>
