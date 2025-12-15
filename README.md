# 🤖 Agentic CMS Portfolio

> A self-updating portfolio website powered by **LangChain** and **Google Gemini**.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.3-black?style=for-the-badge&logo=flask)
![LangChain](https://img.shields.io/badge/LangChain-🦜️🔗-green?style=for-the-badge)
![Gemini](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-8E75B2?style=for-the-badge)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?style=for-the-badge&logo=bootstrap)

## 📖 Overview

This is not a static portfolio. It is an **Agentic Content Management System**. 

Instead of manually writing HTML for every new project or blog post, I utilize a **LangChain-based AI Agent**. Through a secure Admin Dashboard, I provide natural language prompts (e.g., *"Add a project about Leaf Disease Detection using CNNs"*), and the Agent:
1.  **Analyzes** the intent (Blog vs. Project vs. Bio).
2.  **Generates** structured content (HTML, Tags, Links).
3.  **Formats** it for the frontend.
4.  **Saves** it to the SQLite database upon approval.

---
## ✨ Key Features

* **🧠 Intelligent Orchestrator:** Uses `LangChain` and `Pydantic` to enforce strict JSON schemas, ensuring the AI never breaks the UI layout.
* **🎤 Voice Command Integration:** Integrated **Web Speech API** in the Admin Dashboard, allowing you to dictate prompts and manage content hands-free.
* **🎨 Monochrome Premium UI:** A sleek, high-contrast dark theme built with Bootstrap 5, custom CSS gradients, and technical grid backgrounds.
* **🔐 Secure Admin Panel:** Protected route with session-based authentication to manage content.
* **📂 Dynamic Content:**
    * **Smart Project Parsing:** Paste raw `README.md` text, and the Agent converts Markdown into clean HTML cards with "Read More" modals and floating GitHub links.
    * **Blogs:** Technical articles structured with HTML headers, code blocks, and lists.
    * **About Me:** AI-generated bio updates based on skills and experience.
* **📜 History Logging:** Automatically logs all generated content to a local `history.txt` file (UTF-8 supported) for backup.

---
## 🛠️ Tech Stack

* **Backend:** Flask (Python)
* **Database:** SQLite (Native JSON storage)
* **AI Logic:** LangChain, Google Generative AI (Gemini 1.5 Flash)
* **Frontend:** HTML5, Jinja2, Bootstrap 5, Custom CSS, **Web Speech API**
* **Validation:** Pydantic (for structured AI output)

---
## 🚀 Installation & Setup

### 1. Clone the Repository
git clone [https://github.com/yourusername/agentic-portfolio.git](https://github.com/yourusername/agentic-portfolio.git)
cd agentic-portfolio


---
### 2. Create Virtual Environment

python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Configure Environment Variables
Create a .env file in the root directory:

Ini, TOML

GEMINI_API_KEY=your_google_api_key_here
FLASK_SECRET_KEY=your_random_secret_key
ADMIN_PASSWORD=your_secure_password

### 5. Run the Application

python app.py
Visit http://127.0.0.1:5000 in your browser.

## 🕹️ How to Use the Agent
### Navigate to /admin and log in.

To Add a Project:

Prompt: "It's a project called 'ClinicBook'. It uses Flask and Gemini to help patients book appointments. The link is https://www.google.com/search?q=github.com/user/clinicbook."

Result: The Agent categorizes it as a Project, extracts the tech stack, formats the description into HTML, and adds the GitHub link.

To Write a Blog:

Prompt: "Write a blog post about the importance of Vector Databases in RAG applications."

Result: The Agent writes a structured article with headings and bullet points.

To Update Bio:

Prompt: "Update my about section. I am now focusing on Agentic Workflows and Generative AI."

Result: The Agent rewrites the bio and updates the skills tags.

📂 Project Structure
```bash
Portfolio/
├── data/               # SQLite DB and History logs
├── src/
│   ├── agent.py        # LangChain logic & Pydantic models
│   ├── db.py           # Database connection & setup
│   ├── logg.py         # Logging configuration
├── static/
│   └── style.css       # Custom dark theme & animations
├── templates/
│   ├── base.html       # Master layout (Navbar/Footer)
│   ├── index.html      # Public Portfolio View
│   ├── admin.html      # Private AI Dashboard
│   └── login.html      # Auth Page
├── app.py              # Main Flask Application
├── requirements.txt    # Dependencies
└── README.md           # Documentation
```
🤝 Contributing
Feel free to fork this repository and customize the system_prompt in src/agent.py to give the AI your own unique writing style!

