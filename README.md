# 🎓 NEXUS AI: Advanced Hybrid RAG Assistant

**NEXUS AI** is a professional-grade Retrieval-Augmented Generation (RAG) platform. It allows users to chat with complex PDF datasets while offering a seamless fallback to the live web when local data is insufficient.

---

## 🚀 Key Capabilities

* **⚡ Hybrid Intelligence:** Queries local vectorized PDF data first, with an automated fallback to **DuckDuckGo Web Search** for real-time information.
* **🧠 Enterprise-Grade LLMs:** Powered by **Llama 3.3 70B** via Groq Cloud.
* **🎨 Modern SaaS Interface:** Built with Streamlit, featuring custom chat bubbles and a real-time status dashboard.

---

## 🛠️ Technology Stack

* **Core Framework:** LangChain
* **Model Provider:** Groq Cloud (Llama 3.3 70B Versatile)
* **Vector Database:** ChromaDB
* **Embeddings:** HuggingFace (`all-MiniLM-L6-v2`)
* **Frontend:** Streamlit

---

## 📂 Project Architecture

```plaintext
Nexus-AI-RAG-Chatbot/
├── app.py               # Main application logic & Modern UI
├── ingest.py            # Document processing & Vector indexing script
├── requirements.txt     # Dependency management
├── .env.example         # Template for environment variables
├── .gitignore           # Security filters for secrets and cache
├── data/                # Source PDF repository
└── db/                  # Persistent ChromaDB vector store



⚡ Quick Start
1. Installation
Bash
git clone [https://github.com/ehsankhann11/Nexus-AI-RAG-Chatbot.git](https://github.com/ehsankhann11/Nexus-AI-RAG-Chatbot.git)
cd Nexus-AI-RAG-Chatbot
python -m venv .venv
# On Windows: .venv\Scripts\activate
source .venv/bin/activate 
pip install -r requirements.txt
2. Configuration
Create a .env file in the root directory:

Plaintext
GROQ_API_KEY=your_groq_api_key_here
3. Execution
Place PDFs in /data, then run:

Bash
python ingest.py
streamlit run app.py
👨‍💻 About the Developer
Ehsan Ud Din Atta Final Year BS Computer Science Student COMSATS University Islamabad (Attock Campus) Expected Graduation: May 2026
