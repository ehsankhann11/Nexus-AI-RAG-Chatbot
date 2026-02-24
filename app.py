import streamlit as st
import os
from dotenv import load_dotenv

# --- Load Environment Variables ---
load_dotenv()

# --- Imports ---
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.tools import DuckDuckGoSearchRun

st.set_page_config(
    page_title="NEXUS AI", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Better UI ---
st.markdown("""
    <style>
    /* Global Styles */
    .stApp {
        background-color: #f0f2f6;
    }
    
    /* Header Styling */
    .main-header {
        font-family: 'Inter', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0px;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }

    /* Chat Bubble Styling */
    .stChatMessage {
        border-radius: 20px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        border: 1px solid #eef0f2;
    }
    
    /* Assistant Bubble (White/Clean) */
    [data-testid="stChatMessageAssistant"] {
        background-color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    /* User Bubble (Blue/Gradient) */
    [data-testid="stChatMessageUser"] {
        background: linear-gradient(135deg, #007aff 0%, #005bb5 100%) !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(0,122,255,0.2);
    }

    /* Source Badge Styling */
    .source-badge {
        display: inline-flex;
        align-items: center;
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 8px;
    }
    .source-rag { background-color: #e3f2fd; color: #1976d2; border: 1px solid #bbdefb; }
    .source-web { background-color: #f3e5f5; color: #7b1fa2; border: 1px solid #e1bee7; }

    /* Hide Streamlit Footer & Menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<h1 class="main-header">NEXUS AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Chat with Your Documents & Explore the Web in Real-Time</p>', unsafe_allow_html=True)

# --- Groq API Configuration ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")

if not GROQ_API_KEY:
    st.error("⚠️ GROQ_API_KEY not found! Please set it in your environment variables.")
    st.stop()

# --- Web Search Setup ---
search = DuckDuckGoSearchRun()

def search_web(query):
    """Function to perform web search"""
    try:
        return search.run(query)
    except Exception as e:
        return f"Search error: {str(e)}"

# --- Sidebar ---
# --- Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80) # Aik chota icon
    st.title("Settings")
    
    # Model selection with a nice label
    model_option = st.selectbox(
        "🧠 Intelligence Level",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
        index=0
    )
    
    st.markdown("---")
    
    # Search settings
    use_web_search = st.toggle("🌐 Web Search Fallback", value=True)
    
    st.markdown("---")
    
    # Database status
    st.subheader("📚 Knowledge Status")
    if os.path.exists("db"):
        st.success("Vector DB: Online")
    else:
        st.error("Vector DB: Offline")
    
    if os.path.exists("data"):
        pdf_count = len([f for f in os.listdir("data") if f.endswith('.pdf')])
        st.info(f"Loaded: {pdf_count} Documents")

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- Load resources ---
@st.cache_resource
def load_resources():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    vectordb = Chroma(
        persist_directory="db", 
        embedding_function=embeddings
    )
    return vectordb

try:
    vectordb = load_resources()
    retriever = vectordb.as_retriever(search_kwargs={"k": 10})
    db_loaded = True
except Exception as e:
    st.error(f"❌ Error loading vector database: {e}")
    st.info("Please run `python ingest.py` first to create the database.")
    db_loaded = False
    retriever = None

# --- Chat interface ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        # Show source badge if present
        if "source" in msg:
            badge_class = "source-rag" if msg["source"] == "RAG" else "source-web"
            st.markdown(f'<span class="source-badge {badge_class}">📚 {msg["source"]}</span>', 
                       unsafe_allow_html=True)

user_input = st.chat_input("ask anything")

if user_input and db_loaded:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    try:
        # --- LLM Setup ---
        llm = ChatGroq(
            temperature=0.7,
            groq_api_key=GROQ_API_KEY,
            model_name=model_option,
            max_tokens=1024,
        )
        
        with st.spinner("🦙 Thinking..."):
            # First try RAG
            system_prompt = (
    "When asked about a specific quarter (like Q3), you MUST ignore data from other quarters. Verify the document title or header to ensure the data belongs to the requested time period."
    "\n\n"
    "Context: {context}"
)
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", "{input}"),
            ])
            
            combine_docs_chain = create_stuff_documents_chain(llm, prompt)
            rag_chain = create_retrieval_chain(retriever, combine_docs_chain)
            
            response = rag_chain.invoke({"input": user_input})
            answer = response["answer"]
            source = "RAG"
            
            # Check if we need web search fallback
            needs_web_search = (
                "NOT_IN_CONTEXT" in answer or 
                any(phrase in answer.lower() for phrase in [
                    "don't have", "does not contain", "no information", 
                    "not provided", "not mentioned", "context does not",
                    "i don't know", "not found"
                ])
            )
            
            # Web Search Fallback
            if needs_web_search and use_web_search:
                with st.spinner("🔍 Searching web for more info..."):
                    web_results = search_web(user_input)
                    
                    if "error" not in web_results.lower() and len(web_results) > 50:
                        # Use LLM directly with web results
                        web_messages = [
                            SystemMessage(content=(
                                "You are UniPath AI. Answer based on this web search result. "
                                "Be accurate and cite the information clearly.\n\n"
                                f"Web Search Results:\n{web_results[:3000]}"  # Limit context
                            )),
                            HumanMessage(content=user_input)
                        ]
                        web_response = llm.invoke(web_messages)
                        answer = web_response.content
                        source = "Web"
            
            # Add assistant message with source tracking
            message_data = {
                "role": "assistant", 
                "content": answer,
                "source": source
            }
            st.session_state.messages.append(message_data)
            
            # Display response
            with st.chat_message("assistant"):
                st.markdown(answer)
                badge_class = "source-rag" if source == "RAG" else "source-web"
                source_icon = "📚" if source == "RAG" else "🌐"
                st.markdown(
                    f'<span class="source-badge {badge_class}">{source_icon} {source}</span>', 
                    unsafe_allow_html=True
                )
            
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        st.error(error_msg)
        st.session_state.messages.append({"role": "assistant", "content": error_msg})

elif user_input and not db_loaded:
    st.error("⚠️ Please run `python ingest.py` first to create the vector database!")