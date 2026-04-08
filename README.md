# 🤖 AI Chat Assistant with Ollama & Streamlit

A high-performance, local-first AI chat interface built with **Python**, **Streamlit**, and **Ollama**. This application features real-time response streaming, session persistence, and a clean UI/UX designed for rapid AI interaction.

## ✨ Features

* **Real-time Streaming:** Smooth "typing" effect using Streamlit's `write_stream`.
* **Local LLM Integration:** Powered by Ollama for privacy and offline capability.
* **Context Management:** Maintains full conversation history during the session.
* **Professional UI:** Modern layout with a responsive chat interface and instant-reset functionality.

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **AI Engine:** [Ollama](https://ollama.com/)
* **Language:** Python 3.10+
* **Architecture:** Agentic Chat Loop with Session State management.

## 🚀 Getting Started

### Prerequisites

1.  **Install Ollama:** [Download here](https://ollama.com/) and ensure it is running on your machine.
2.  **Pull a Model:**
    ```cmd
    ollama pull llama3.1:8b
    ```

### Installation

1.  **Clone the repository:**
    ```cmd
    git clone [https://github.com/johnasad09/chatbot-local-llm-streamlit.git](https://github.com/johnasad09/chatbot-local-llm-streamlit.git)
    cd chatbot-local-llm-streamlit
    ```

2.  **Install dependencies:**
    ```cmd
    pip install -r requirements.txt
    ```

3.  **Run the app:**
    ```cmd
    streamlit run app.py
    ```
---
*Developed by Asad Ullah – AI Engineer & Automation Specialist*
