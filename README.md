🎓 NEXUS AI: Advanced Hybrid RAG Assistant
NEXUS AI is a professional-grade Retrieval-Augmented Generation (RAG) platform designed to bridge the gap between static document analysis and real-time web intelligence. Built with a focus on precision and performance, it allows users to chat with complex PDF datasets while offering a seamless fallback to the live web when local data is insufficient.

🚀 Key Capabilities
⚡ Hybrid Intelligence: Orchestrates a dual-layer search strategy—querying local vectorized PDF data first, with an automated fallback to DuckDuckGo Web Search for real-time information.

🧠 Enterprise-Grade LLMs: Powered by Llama 3.3 70B and Mixtral via Groq Cloud, delivering ultra-low latency and high-reasoning capabilities.

📊 Temporal Precision: Optimized system prompting ensures the model accurately distinguishes between similar data points across different time periods (e.g., Q1 vs. Q4 financial updates).

🎨 Modern SaaS Interface: A clean, glassmorphic UI built with Streamlit and Custom CSS, featuring intuitive chat bubbles, source-tracking badges, and a real-time system status dashboard.

🔒 Secure & Scalable: Implements environment-based secret management and optimized vector indexing using ChromaDB.

🛠️ Technology Stack
Core Framework: LangChain

Model Provider: Groq Cloud

Inference Engine: Llama 3.3 70B Versatile

Vector Database: ChromaDB

Embeddings: sentence-transformers/all-MiniLM-L6-v2 (HuggingFace)

Frontend: Streamlit

Search API: DuckDuckGo Search

📂 Project Architecture
Plaintext
Nexus-AI-RAG-Chatbot/
├── app.py               # Main application logic & Modern UI
├── ingest.py            # Document processing & Vector indexing script
├── requirements.txt     # Dependency management
├── .env.example         # Template for environment variables
├── .gitignore           # Security filters for secrets and cache
├── data/                # Source PDF repository (e.g., Tesla 2025 Updates)
└── db/                  # Persistent ChromaDB vector store
⚡ Quick Start
1. Installation
Bash
git clone https://github.com/ehsankhann11/Nexus-AI-RAG-Chatbot.git
cd Nexus-AI-RAG-Chatbot
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
2. Configuration
Create a .env file in the root directory:

Plaintext
GROQ_API_KEY=your_groq_api_key_here
3. Data Ingestion
Place your PDF files in the data/ folder, then run:

Bash
python ingest.py
4. Run Nexus AI
Bash
streamlit run app.py
🎥 User Interface Preview
NEXUS AI features a professional control panel where users can toggle web search, switch between intelligence models, and monitor the health of the Vector Database in real-time.

👨‍💻 About the Developer
Ehsan Ud Din Atta  BS Computer Science  COMSATS University Islamabad (Attock Campus)
